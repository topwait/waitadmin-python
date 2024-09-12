<template>
    <div class="layout-container">
        <drawers />
        <layout-header />
        <tags-view v-if="isTabMultiple" />
        <div class="layout-main">
            <layout-main />
        </div>
    </div>
</template>

<script setup lang="ts">
import useConfStore from '@/stores/modules/conf'
import TagsView from '../../components/TagsView.vue'
import LayoutHeader from './Header.vue'
import LayoutMain from '../AppMain.vue'
import Drawers from '../Drawers.vue'

const confStore = useConfStore()
const isTabMultiple = computed(() => confStore.isTabMultiple)
</script>

<style scoped lang="scss">
.layout-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    .layout-main {
        display: flex;
        flex: 1 1 0;
        overflow: hidden;
    }
}
</style>
