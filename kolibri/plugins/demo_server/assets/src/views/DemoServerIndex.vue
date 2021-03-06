<template>

  <div
    class="banner"
    :style="{ background: $coreBgLight }"
    :tabindex="0"
    role="dialog"
  >
    <div class="banner-inner">
      <div v-if="!bannerClosed">
        <h1>{{ $tr('demoServerHeader') }}</h1>
        <p>{{ $tr('demoServerP1') }}</p>
        <ul>
          <li>{{ $tr('demoServerL1', {user: 'learnerdemo', pass: 'pass'} ) }}</li>
          <li>{{ $tr('demoServerL2', {user: 'coachdemo', pass: 'pass'} ) }}</li>
          <li>{{ $tr('demoServerL3', {user: 'admindemo', pass: 'pass'} ) }}</li>
        </ul>
        <p>{{ $tr('demoServerP2') }}</p>
        <p>{{ $tr('demoServerP3') }}</p>
        <ul>
          <li>
            <KExternalLink
              href="https://learningequality.org/documentation/"
              :text="$tr('demoServerA1')"
              target="_blank"
            />
          </li>
          <li>
            <KExternalLink
              href="https://learningequality.org/download/"
              :text="$tr('demoServerA2')"
              target="_blank"
            />
          </li>
        </ul>
        <KButton
          class="close-button"
          :text="'Close'"
          appearance="flat-button"
          :primary="true"
          @click="toggleBannerState"
        />
      </div>
      <div v-else>
        <h1>
          Welcome to the Kolibri demo site!
          <KButton
            class="open-button"
            :text="'More info'"
            appearance="flat-button"
            :primary="true"
            @click="toggleBannerState"
          />
        </h1>
      </div>

    </div>
  </div>

</template>


<script>

  import themeMixin from 'kolibri.coreVue.mixins.themeMixin';
  import KButton from 'kolibri.coreVue.components.KButton';
  import KExternalLink from 'kolibri.coreVue.components.KExternalLink';

  export default {
    name: 'DemoServerIndex',
    components: {
      KButton,
      KExternalLink,
    },
    mixins: [themeMixin],
    data() {
      return {
        bannerClosed: false,
      };
    },
    methods: {
      toggleBannerState(event) {
        this.bannerClosed = !this.bannerClosed;
        event.target.blur();
        return false;
      },
    },
    $trs: {
      demoServerHeader: 'Welcome to the Kolibri demo site!',
      demoServerP1: 'You are welcome to explore with any of the three primary user types:',
      demoServerL1: "Learner (username: '{user}', password: '{pass}') or access as a guest",
      demoServerL2: "Coach (username: '{user}', password: '{pass}')",
      demoServerL3: "Admin (username: '{user}', password: '{pass}')",
      demoServerP2:
        'This online demo site includes the features and functionalities of the latest version, but only holds a sample of the content that has been made available for offline use in Kolibri. It is intended for demonstration purposes and any user data on here may be cleared periodically.',
      demoServerP3:
        'To learn more about using Kolibri in an offline context and better understand the platform:',
      demoServerA1: 'Read the documentation',
      demoServerA2: 'Download and install the latest release',
    },
  };

</script>


<style lang="scss" scoped>

  .banner {
    position: absolute;
    top: 0%;
    left: 0%;
    width: 100%;
    margin: 0 auto;
    overflow-y: auto;
    box-shadow: 0 2px 50px rgba(0, 0, 0, 1);
  }

  .banner-inner {
    max-width: 1000px;
    padding-top: 0;
    padding-right: 12px;
    padding-left: 12px;
    margin: 0 auto;
    h1 {
      font-weight: bold;
    }
  }

  .close-button {
    float: right;
    margin-bottom: 24px;
  }

  .open-button {
    float: right;
    margin-top: 0;
  }

</style>
