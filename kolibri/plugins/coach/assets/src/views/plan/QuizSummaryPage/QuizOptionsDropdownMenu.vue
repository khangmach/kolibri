<template>

  <KDropdownMenu
    :text="coachStrings.$tr('optionsLabel')"
    :options="options"
    appearance="raised-button"
    :primary="false"
    @select="$emit('select', $event.value)"
  />

</template>


<script>

  import KDropdownMenu from 'kolibri.coreVue.components.KDropdownMenu';
  import { coachStringsMixin } from '../../common/commonCoachStrings';

  export default {
    name: 'QuizOptionsDropdownMenu',
    components: {
      KDropdownMenu,
    },
    mixins: [coachStringsMixin],
    props: {
      // Should be either 'report' or 'plan',
      optionsFor: {
        type: String,
        required: true,
      },
    },
    computed: {
      options() {
        const editDetails = {
          label: this.coachStrings.$tr('editDetailsAction'),
          value: 'EDIT_DETAILS',
        };
        if (this.optionsFor === 'plan') {
          return [
            editDetails,
            {
              label: this.$tr('copyQuizAction'),
              value: 'COPY',
            },
            { label: this.coachStrings.$tr('deleteAction'), value: 'DELETE' },
          ];
        }
        return [
          {
            label: this.coachStrings.$tr('previewAction'),
            value: 'PREVIEW',
          },
          editDetails,
        ];
      },
    },
    $trs: {
      copyQuizAction: 'Copy quiz',
    },
  };

</script>


<style lang="scss" scoped></style>
