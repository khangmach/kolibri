<template>

  <div class="side-bar" :style="{ backgroundColor: $coreBgCanvas }">
    <slot></slot>
  </div>

</template>


<script>

  import themeMixin from 'kolibri.coreVue.mixins.themeMixin';

  export default {
    name: 'SideBar',
    mixins: [themeMixin],
  };

</script>


<style lang="scss" scoped>

  @import './EpubStyles';

  .side-bar {
    z-index: 6;
    width: 250px;
    padding: 16px;
    overflow-y: auto;
    word-wrap: break-word;
    box-shadow: $epub-box-shadow;
  }

</style>
