<template>
    <div class="layout-container">
        <drawers>
            <layout-asides v-show="!isMobile" />
        </drawers>
        <div class="layout-main">
            <layout-header />
            <layout-main />
        </div>
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import LayoutHeader from '../../Header/index.vue'
import LayoutAsides from './Asides.vue'
import LayoutMain from '../AppMain.vue'
import Drawers from '../Drawers.vue'

const appStore = useAppStore()
const isMobile = computed<boolean>(() => appStore.isMobile)
</script>

<style scoped lang="scss">
.layout-container {
    display: flex;
    width: 100%;
    height: 100vh;
    .layout-main {
        display: flex;
        flex: 1 1 0;
        flex-direction: column;
        overflow: hidden;
    }
}
</style>
