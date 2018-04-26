import logging as logger

from django.apps import apps
from sqlalchemy.exc import SQLAlchemyError

from .annotation import set_availability
from .channels import read_channel_metadata_from_db_file
from .paths import get_content_database_file_path
from .sqlalchemybridge import Bridge
from .sqlalchemybridge import ClassNotFoundError
from kolibri.content.apps import KolibriContentConfig
from kolibri.content.legacy_models import License
from kolibri.content.models import ChannelMetadata
from kolibri.content.models import CONTENT_SCHEMA_VERSION
from kolibri.content.models import ContentNode
from kolibri.content.models import ContentTag
from kolibri.content.models import File
from kolibri.content.models import Language
from kolibri.content.models import LocalFile
from kolibri.content.models import NO_VERSION
from kolibri.content.models import V020BETA1
from kolibri.content.models import V040BETA3
from kolibri.content.models import VERSION_1
from kolibri.content.models import VERSION_2
from kolibri.utils.time import local_now

logging = logger.getLogger(__name__)

CONTENT_APP_NAME = KolibriContentConfig.label

merge_models = [
    ContentTag,
    LocalFile,
    Language,
]

def column_not_auto_integer_pk(column):
    """
    A check for whether a column is an auto incrementing integer used for a primary key.
    """
    return not (column.autoincrement == 'auto' and column.primary_key and column.type.python_type is int)

class ChannelImport(object):
    """
    The ChannelImport class has two functions:

    1) it acts as the default import pattern for importing content databases that have naively compatible version
    with the current version of Kolibri (i.e. no explicit mappings are required to bring data from the content db
    into the main db, as there is a one to one correspondence in table names and column names within tables).

    2) It is also the base class for any more complex import that requires explicit schema mappings from one version
    to another.
    """

    # Specific instructions and exceptions for importing table from previous versions of Kolibri
    # Mappings can be:
    # 1) 'per_row', specifying mappings for an entire row, string can either be an attribute
    #    or a method name on the import class
    # 2) 'per_table' mapping an entire table at a time. Only a method name can be used for 'per_table' mappings.
    #
    # Both can be used simultaneously.
    #
    # See NoVersionChannelImport for an annotated example.

    # Need this on the base mapping because every tree in exported channel databases has an id of 1,
    # as it is the only tree in the db
    schema_mapping = {
        ContentNode: {
            'per_row': {
                'tree_id': 'get_tree_id',
            },
        },
    }

    def __init__(self, channel_id, channel_version=None):
        self.channel_id = channel_id
        self.channel_version = channel_version

        self.source = Bridge(sqlite_file_path=get_content_database_file_path(channel_id))

        self.destination = Bridge(app_name=CONTENT_APP_NAME)

        content_app = apps.get_app_config(CONTENT_APP_NAME)

        # Use this rather than get_models, as it returns a list of all models, including those
        # generated by ManyToMany fields, whereas get_models only returns explicitly defined
        # Model classes
        self.content_models = list(content_app.get_models(include_auto_created=True))

        # Get the next available tree_id in our database
        self.tree_id = self.find_unique_tree_id()

    def get_tree_id(self, source_object):
        return self.tree_id

    def get_all_destination_tree_ids(self):
        ContentNodeRecord = self.destination.get_class(ContentNode)
        return sorted(map(lambda x: x[0], self.destination.session.query(
            ContentNodeRecord.tree_id).distinct().all()))

    def find_unique_tree_id(self):
        tree_ids = self.get_all_destination_tree_ids()
        # If there are no pre-existing tree_ids just escape here and return 1
        if not tree_ids:
            return 1
        if len(tree_ids) == 1:
            if tree_ids[0] == 1:
                return 2
            return 1

        # Do a binary search to find the lowest unused tree_id
        def find_hole_in_list(ids):
            last = len(ids) - 1
            middle = int(last/2 + 1)
            # Check if the lower half of ids has a hole in it
            if ids[middle] - ids[0] != middle:
                # List is only two ids, so hole must be between them
                if middle == 1:
                    return ids[0] + 1
                return find_hole_in_list(ids[:middle])
            # Otherwise check if there is a hole in the second half
            if ids[last] - ids[middle] != last - middle:
                # Second half is only two ids so hole must be between them
                if last - middle == 1:
                    return ids[middle] + 1
                return find_hole_in_list(ids[middle:])
            # We should only reach this point in the first iteration, if there are no holes in either
            # the first or the last half of the list, therefore, we just take the max of the list plus 1
            # Because the list is already sorted, we can just take the last value
            return ids[-1] + 1
        return find_hole_in_list(tree_ids)

    def generate_row_mapper(self, mappings=None):
        # If no mappings, just use an empty object
        if mappings is None:
            mappings = {}

        def mapper(record, column):
            """
            A mapper function for the mappings object
            """
            if column in mappings:
                # If the column name is in our defined mappings object,
                # then we need to try to find an alternate value
                col_map = mappings.get(column)  # Get the string value for the mapping
                if hasattr(record, col_map):
                    # Is this mapping value another column of the table?
                    # If so, return it straight away
                    return getattr(record, col_map)
                elif hasattr(self, col_map):
                    # Otherwise, check to see if the import class has an attribute with this name
                    # We assume that if it is, then it is a callable method that accepts the row
                    # data as its only argument, if so, return the result of calling that method
                    # on the row data
                    return getattr(self, col_map)(record)
                else:
                    # If neither of these true, we specified a column mapping that is invalid
                    raise AttributeError('Column mapping specified but no valid column name or method found')
            else:
                # Otherwise, we can just get the value directly from the record
                return getattr(record, column, None)
        # Return the mapper function for repeated use
        return mapper

    def base_table_mapper(self, SourceRecord):
        # If SourceRecord is none, then the source table does not exist in the DB
        if SourceRecord:
            return self.source.session.query(SourceRecord).all()
        return []

    def generate_table_mapper(self, table_map=None):
        if table_map is None:
            # If no table mapping specified, just use the default
            return self.base_table_mapper
        # Can only be a method on the Import object
        if hasattr(self, table_map):
            # If it is a method of the import class return that method for later use
            return getattr(self, table_map)
        # If we got here, there is an invalid table mapping
        raise AttributeError('Table mapping specified but no valid method found')

    def table_import(self, model, row_mapper, table_mapper, unflushed_rows):
        DestinationRecord = self.destination.get_class(model)
        dest_table = DestinationRecord.__table__

        # If the source class does not exist (i.e. this table is undefined in the source database)
        # this will raise an error so we set it to None. In this case, a custom table mapper must
        # have been set up to handle the fact that this is None.
        try:
            SourceRecord = self.source.get_class(model)
        except ClassNotFoundError:
            SourceRecord = None

        # Filter out columns that are auto-incrementing integer primary keys, as these can cause collisions in the
        # database. As all of our content database models use UUID primary keys, the only tables using these
        # primary keys are intermediary tables for ManyToMany fields, and so nothing should be Foreign Keying
        # to these ids.
        # By filtering them here, the database should autoset an incremented id.
        columns = [column_name for column_name, column_obj in dest_table.columns.items() if column_not_auto_integer_pk(column_obj)]
        data_to_insert = []
        merge = model in merge_models
        for record in table_mapper(SourceRecord):
            data = {
                str(column): row_mapper(record, column) for column in columns if row_mapper(record, column) is not None
            }
            if merge:
                # Models that should be merged (see list above) need to be individually merged into the session
                # as SQL Alchemy ORM does not support INSERT ... ON DUPLICATE KEY UPDATE style queries,
                # as not available in SQLite, only MySQL as far as I can tell:
                # http://hackthology.com/how-to-compile-mysqls-on-duplicate-key-update-in-sql-alchemy.html
                self.destination.session.merge(DestinationRecord(**data))
            else:
                data_to_insert.append(data)
            unflushed_rows += 1
            if unflushed_rows == 10000:
                if not merge:
                    self.destination.session.bulk_insert_mappings(DestinationRecord, data_to_insert)
                    data_to_insert = []
                self.destination.session.flush()
                unflushed_rows = 0
        if not merge and data_to_insert:
            self.destination.session.bulk_insert_mappings(DestinationRecord, data_to_insert)
        return unflushed_rows

    def import_channel_data(self):

        unflushed_rows = 0

        try:
            for model in self.content_models:
                mapping = self.schema_mapping.get(model, {})
                row_mapper = self.generate_row_mapper(mapping.get('per_row'))
                table_mapper = self.generate_table_mapper(mapping.get('per_table'))
                logging.info('Importing {model} data'.format(model=model.__name__))
                unflushed_rows = self.table_import(model, row_mapper, table_mapper, unflushed_rows)
            self.destination.session.commit()

        except SQLAlchemyError as e:
            # Rollback the transaction if any error occurs during the transaction
            self.destination.session.rollback()
            # Reraise the exception to prevent other errors occuring due to the non-completion
            raise e

    def end(self):
        self.source.end()
        self.destination.end()


class NoVersionChannelImport(ChannelImport):
    """
    Class defining the schema mapping for importing old content databases (i.e. ones produced before the
    ChannelImport machinery was implemented). The schema mapping below defines how to bring in information
    from the old version of the Kolibri content databases into the database for the current version of Kolibri.
    """

    schema_mapping = {
        # The top level keys of the schema_mapping are the Content Django Models that are to be imported
        ContentNode: {
            # For each model's mappings, can defined both 'per_row' and 'per_table' mappings.
            'per_row': {
                # The key of the 'per_row' mapping object is the table column that we are populating
                # In the case of Django ForeignKey fields, this will be the field name plus _id
                # The value is a string that refers either to a table column on the source data
                # or a method on this import class that will be passed the row data and should return
                # the mapped value.
                'channel_id': 'infer_channel_id_from_source',
                'tree_id': 'get_tree_id',
                'available': 'get_none',
                'license_name': 'get_license_name',
                'license_description': 'get_license_description',
            },
        },
        File: {
            'per_row': {
                # If we didn't want to encode the Django _id convention here, we could reference the field
                # attname in order to set it.
                File._meta.get_field('local_file').attname: 'checksum',
                'available': 'get_none',
            },
        },
        LocalFile: {
            # Because LocalFile does not exist on old content databases, we have to override the table that
            # we are drawing from, the generate_local_file_from_file method overrides the default mapping behaviour
            # and instead reads from the File model table
            # It then uses per_row mappers to get the require model fields from the File model to populate our
            # new LocalFiles.
            'per_table': 'generate_local_file_from_file',
            'per_row': {
                'id': 'checksum',
                'extension': 'extension',
                'file_size': 'file_size',
                'available': 'get_none',
            },
        },
        ChannelMetadata: {
            'per_row': {
                ChannelMetadata._meta.get_field('min_schema_version').attname: 'set_version_to_no_version',
                'root_id': 'root_pk',
            },
        },
    }

    licenses = {}

    def get_none(self, source_object):
        return None

    def infer_channel_id_from_source(self, source_object):
        return self.channel_id

    def generate_local_file_from_file(self, SourceRecord):
        SourceRecord = self.source.get_class(File)
        checksum_record = set()
        # LocalFile objects are unique per checksum
        for record in self.source.session.query(SourceRecord).all():
            if record.checksum not in checksum_record:
                checksum_record.add(record.checksum)
                yield record
            else:
                continue

    def set_version_to_no_version(self, source_object):
        return NO_VERSION

    def get_license(self, SourceRecord):
        license_id = SourceRecord.license_id
        if not license_id:
            return None
        if license_id not in self.licenses:
            LicenseRecord = self.source.get_class(License)
            license = self.source.session.query(LicenseRecord).get(license_id)
            self.licenses[license_id] = license
        return self.licenses[license_id]

    def get_license_name(self, SourceRecord):
        license = self.get_license(SourceRecord)
        if not license:
            return None
        return license.license_name

    def get_license_description(self, SourceRecord):
        license = self.get_license(SourceRecord)
        if not license:
            return None
        return license.license_description


# Dict that maps from schema versions to ChannelImport classes
# The channel import class defines all the operations required in order to import data
# from a content database with this content schema, into the schema being used by this
# version of Kolibri. When a new schema version is added
mappings = {
    V020BETA1: NoVersionChannelImport,
    V040BETA3: NoVersionChannelImport,
    NO_VERSION: NoVersionChannelImport,
    VERSION_1: ChannelImport,
    VERSION_2: ChannelImport,
}


class FutureSchemaError(Exception):
    pass


class InvalidSchemaVersionError(Exception):
    pass


def initialize_import_manager(channel_id):
    channel_metadata = read_channel_metadata_from_db_file(get_content_database_file_path(channel_id))
    # For old versions of content databases, we can only infer the schema version
    min_version = getattr(channel_metadata, 'min_schema_version', getattr(channel_metadata, 'inferred_schema_version'))

    try:
        ImportClass = mappings.get(min_version)
    except KeyError:
        try:
            version_number = int(min_version)
            if version_number > int(CONTENT_SCHEMA_VERSION):
                raise FutureSchemaError('Tried to import schema version, {version}, which is not supported by this version of Kolibri.'.format(
                    version=min_version,
                ))
            elif version_number < int(CONTENT_SCHEMA_VERSION):
                # If it's a valid integer, but there is no schema for it, then we have stopped supporting this version
                raise InvalidSchemaVersionError('Tried to import unsupported schema version {version}'.format(
                    version=min_version,
                ))
        except ValueError:
            raise InvalidSchemaVersionError('Tried to import invalid schema version {version}'.format(
                version=min_version,
            ))
    return ImportClass(channel_id, channel_version=channel_metadata.version)


def import_channel_from_local_db(channel_id):
    import_manager = initialize_import_manager(channel_id)

    try:
        existing_channel = ChannelMetadata.objects.get(id=channel_id)
    except ChannelMetadata.DoesNotExist:
        existing_channel = None

    if existing_channel:
        if existing_channel.version < import_manager.channel_version:
            # We have an older version of this channel, so let's clean out the old stuff first
            logging.info(('Older version {channel_version} of channel {channel_id} already exists in database; removing old entries ' +
                          'so we can upgrade to version {new_channel_version}').format(
                channel_version=existing_channel.version, channel_id=channel_id, new_channel_version=import_manager.channel_version))
            existing_channel.delete_content_tree_and_files()
        else:
            # We have previously loaded this channel, with the same or newer version, so our work here is done
            logging.warn(('Version {channel_version} of channel {channel_id} already exists in database; cancelling import of ' +
                          'version {new_channel_version}').format(
                channel_version=existing_channel.version, channel_id=channel_id, new_channel_version=import_manager.channel_version))
            return

    import_manager.import_channel_data()

    import_manager.end()

    set_availability(channel_id)

    channel = ChannelMetadata.objects.get(id=channel_id)
    channel.last_updated = local_now()
    try:
        assert channel.root
    except ContentNode.DoesNotExist:
        node_id = channel.root_id
        ContentNode.objects.create(
            id=node_id,
            title=channel.name,
            content_id=node_id,
            channel_id=channel_id,
        )
    channel.save()
