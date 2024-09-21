<template>
    <div class="layout-header">
        <div class="header-navbar-wrapper">
            <ul class="navbar-left">
                <li><stretch /></li>
                <li v-if="!isMobile && isBreadcrumb" class="breadcrumb">
                    <breadcrumbs  />
                </li>
            </ul>
            <ul class="navbar-right">
                <li><refresh /></li>
                <li v-if="!isMobile"><screens /></li>
                <li><user-dropdown /></li>
                <li><system-setting /></li>
            </ul>
        </div>

        <tags-view v-if="isTabMultiple" />
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import useConfStore from '@/stores/modules/conf'
import Refresh from './Refresh.vue'
import Stretch from './Stretch.vue'
import Screens from './Screens.vue'
import Breadcrumbs from './WBreadcrumbs.vue'
import UserDropdown from './UserDropdown.vue'
import SystemSetting from './SystemSetting.vue'
import TagsView from '../components/TagsView.vue'

const appStore = useAppStore()
const confStore = useConfStore()

const isMobile = computed<boolean>(() => appStore.isMobile)
const isBreadcrumb = computed<boolean>(() => confStore.isBreadcrumb)
const isTabMultiple = computed<boolean>(() => confStore.isTabMultiple)
</script>

<style scoped lang="scss">
.header-navbar-wrapper {
    display: flex;
    justify-content: space-between;
    height: 50px;
    padding: 0 10px;
    background-color: var(--wa-header-bg-color);
    border-bottom: 1px solid var(--wa-header-border-color);
    ul {
        display: flex;
        align-items: center;
        li {
            display: flex;
            align-items: center;
            height: 100%;
            cursor: pointer;
            &.breadcrumb:hover {
                background: none;
            }
            &:hover {
                background: var(--el-bg-color-light, #f8f8f8);;
            }
        }
    }
}
</style>
