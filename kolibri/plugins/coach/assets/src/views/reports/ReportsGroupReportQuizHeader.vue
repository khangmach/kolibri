<template>

  <div>

    <p>
      <BackLink
        :to="classRoute('ReportsGroupReportPage')"
        :text="group.name"
      />
    </p>
    <h1>
      <KLabeledIcon>
        <KIcon slot="icon" quiz />
        {{ exam.title }}
      </KLabeledIcon>
    </h1>

    <HeaderTable>
      <HeaderTableRow>
        <template slot="key">
          {{ coachStrings.$tr('statusLabel') }}
        </template>
        <QuizActive slot="value" :active="exam.active" />
      </HeaderTableRow>
      <HeaderTableRow>
        <template slot="key">
          {{ coachStrings.$tr('avgScoreLabel') }}
        </template>
        <Score slot="value" :value="avgScore" />
      </HeaderTableRow>
      <!-- TODO COACH
      <HeaderTableRow>
        <template slot="key">{{ coachStrings.$tr('questionOrderLabel') }}</template>
        <template slot="value">{{ coachStrings.$tr('orderRandomLabel') }}</template>
      </HeaderTableRow>
       -->
    </HeaderTable>

    <HeaderTabs>
      <HeaderTab
        :text="coachStrings.$tr('reportLabel')"
        :to="classRoute('ReportsGroupReportQuizLearnerListPage')"
      />
      <HeaderTab
        :text="coachStrings.$tr('difficultQuestionsLabel')"
        :to="classRoute('ReportsGroupReportQuizQuestionListPage')"
      />
    </HeaderTabs>

  </div>

</template>


<script>

  import commonCoach from '../common';

  export default {
    name: 'ReportsGroupReportQuizHeader',
    components: {},
    mixins: [commonCoach],
    computed: {
      avgScore() {
        return this.getExamAvgScore(this.$route.params.quizId, this.recipients);
      },
      group() {
        return this.groupMap[this.$route.params.groupId];
      },
      exam() {
        return this.examMap[this.$route.params.quizId];
      },
      recipients() {
        return this.getLearnersForGroups([this.$route.params.groupId]);
      },
    },
    $trs: {
      back: 'All quizzes',
      quizPerformanceLabel: "'{quiz}' performance",
    },
  };

</script>


<style lang="scss" scoped>

  .stats {
    margin-right: 16px;
  }

</style>
