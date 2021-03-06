import { createTranslator } from 'kolibri.utils.i18n';

const coachStrings = createTranslator('CommonCoachStrings', {
  // actions
  cancelAction: 'Cancel',
  closeAction: 'Close',
  continueAction: 'Continue',
  copyAction: 'Copy',
  createAction: 'Create',
  deleteAction: 'Delete',
  editDetailsAction: 'Edit details',
  finishAction: 'Finish',
  goBackAction: 'Go back',
  manageResourcesAction: 'Manage resources',
  newGroupAction: 'New group',
  newLessonAction: 'New lesson',
  newQuizAction: 'New quiz',
  previewAction: 'Preview',
  saveAction: 'Save',
  saveChangesAction: 'Save changes',
  renameAction: 'Rename',
  showAction: 'Show',
  showMoreAction: 'Show more',
  sortedAscendingAction: 'Sort in ascending order',
  sortedDescendingAction: 'Sort in descending order',

  // labels, phrases, titles, headers...
  activityLabel: 'Activity',
  answerLabel: 'Answer',
  answersLabel: 'Answers',
  answerHistoryLabel: 'Answer history',
  attemptLabel: 'Attempt',
  attemptsLabel: 'Attempts',
  avgScoreLabel: 'Average score',
  avgTimeSpentLabel: 'Average time spent',
  avgQuizScoreLabel: 'Average quiz score',
  channelLabel: 'Channel',
  channelsLabel: 'Channels',
  classLabel: 'Class',
  classesLabel: 'Classes',
  completedLabel: 'Completed',
  coachLabel: 'Coach',
  coachesLabel: 'Coaches',
  descriptionLabel: 'Description',
  descriptionMissingLabel: 'No description',
  detailsLabel: 'Details',
  difficultQuestionsLabel: 'Difficult questions',
  entireClassLabel: 'Entire class',
  exercisesCompletedLabel: 'Exercises completed',
  groupLabel: 'Group',
  groupNameLabel: 'Group name',
  groupsLabel: 'Groups',
  helpNeededLabel: 'Help needed',
  inProgressLabel: 'In progress',
  lastActivityLabel: 'Last activity',
  learnerLabel: 'Learner',
  learnersLabel: 'Learners',
  lessonLabel: 'Lesson',
  lessonActiveLabel: 'Active',
  lessonInactiveLabel: 'Inactive',
  lessonsLabel: 'Lessons',
  lessonsAssignedLabel: 'Lessons assigned',
  lessonsCompletedLabel: 'Lessons completed',
  masteryModelLabel: 'Completion requirement',
  membersLabel: 'Members',
  nameLabel: 'Name',
  namesLabel: 'Names',
  notEnoughInformationLabel: 'Not enough information yet',
  notStartedLabel: 'Not started',
  optionsLabel: 'Options',
  orderFixedLabel: 'Fixed',
  orderFixedLabelLong: 'Fixed: each learner sees the same question order',
  orderFixedDescription: 'Each learner sees the same question order',
  orderRandomLabel: 'Randomized',
  orderRandomLabelLong: 'Randomized: each learner sees a different question order',
  orderRandomDescription: 'Each learner sees a different question order',
  overallLabel: 'Overall',
  previewLabel: 'Preview',
  progressLabel: 'Progress',
  questionLabel: 'Question',
  questionOrderLabel: 'Question order',
  questionsCorrectLabel: 'Questions correct',
  questionsLabel: 'Questions',
  quizLabel: 'Quiz',
  quizActiveLabel: 'Active',
  quizInactiveLabel: 'Inactive',
  quizScoreLabel: 'Quiz score',
  quizzesLabel: 'Quizzes',
  quizzesAssignedLabel: 'Quizzes assigned',
  quizzesCompletedLabel: 'Quizzes completed',
  recipientLabel: 'Recipient',
  recipientsLabel: 'Recipients',
  reportLabel: 'Report',
  reportsLabel: 'Reports',
  resourceTitleLabel: 'Resource title',
  resourcesViewedLabel: 'Resources viewed',
  scoreLabel: 'Score',
  sortedAscendingLabel: '(sorted ascending)',
  sortedDescendingLabel: '(sorted descending)',
  startedLabel: 'Started',
  statusLabel: 'Status',
  titleLabel: 'Title',
  timeLabel: 'Time',
  timeSpentLabel: 'Time spent',
  ungroupedLearnersLabel: 'Ungrouped learners',
  usernameLabel: 'Username',
  viewsLabel: 'Views',

  // notifications
  updatedNotification: 'Updated',
  createdNotification: 'Created',
  deletedNotification: 'Deleted',
  savedNotification: 'Saved',

  // empty states
  activityListEmptyState: 'There is no activity',
  answerListEmptyState: 'There are no answers',
  attemptListEmptyState: 'There are no attempts',
  classListEmptyState: 'There are no classes',
  groupListEmptyState: 'There are no groups',
  learnerListEmptyState: 'There are no learners',
  lessonListEmptyState: 'There are no lessons',
  recentActivityListEmptyState: 'There is no recent activity',
  questionListEmptyState: 'There are no questions',
  quizListEmptyState: 'There are no quizzes',

  // toggles
  showCorrectAnswerLabel: 'Show correct answer',
  viewByGroupsLabel: 'View by groups',

  // formatted values
  integer: '{value, number, integer}',
  combinedLabel: '{firstItem} / {secondItem}',
  number: '{value, number}',
  numberOfClasses: '{value, number, integer} {value, plural, one {class} other {classes}}',
  numberOfCoaches: '{value, number, integer} {value, plural, one {coach} other {coaches}}',
  numberOfGroups: '{value, number, integer} {value, plural, one {group} other {groups}}',
  numberOfLearners: '{value, number, integer} {value, plural, one {learner} other {learners}}',
  numberOfQuestions: '{value, number, integer} {value, plural, one {question} other {questions}}',
  numberOfResources: '{value, number, integer} {value, plural, one {resource} other {resources}}',
  numberOfViews: '{value, number, integer} {value, plural, one {view} other {views}}',
  percentage: '{value, number, percent}',
  ratio: '{value, number, integer} out of {total, number, integer}',
  ratioShort: '{value, number, integer} of {total, number, integer}',

  // Errors
  quizDuplicateTitleError: 'A quiz with that name already exists',
  lessonDuplicateTitleError: 'A lesson with this name already exists',
});

const coachStringsMixin = {
  computed: {
    coachStrings() {
      return coachStrings;
    },
  },
};

export { coachStrings, coachStringsMixin };
