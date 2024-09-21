<template>
    <div class="aside-menus-container" :class="`menu-style-${menuLightStyle}`">
        <logo v-if="isLayoutLogo"  />
        <el-scrollbar>
            <el-menu
                mode="vertical"
                :collapse="isCollapsed"
                :default-active="activeMenu"
                :unique-opened="isUniqueOpened"
                text-color="var(--wa-menu-text-color)"
                active-text-color="var(--wa-menu-active-text-color)"
                background-color="var(--wa-menu-bg-color)"
                router
            >
                <menu-item
                    v-for="route in routes"
                    :key="route.path"
                    :route="route"
                    :route-path="route.path"
                />
            </el-menu>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import useConfStore from '@/stores/modules/conf'
import Logo from '../../components/Logo.vue'
import MenuItem from '../../components/MenuItem.vue'

const route = useRoute()
const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

const routes = computed(() => userStore.routes)
const activeMenu  = computed<string>(() => (route.meta?.activeMenu || route.path) + '')
const isCollapsed = computed<boolean>(() => appStore.isCollapsed)
const isLayoutLogo = computed<boolean>(() => confStore.isLayoutLogo)
const isUniqueOpened = computed<boolean>(() => !confStore.isUniqueOpened)
const menuLightStyle = computed<boolean>(() => confStore.menuLightStyle)
</script>

<style scoped lang="scss">
.aside-menus-container {
    position: relative;
    z-index: 999;
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: var(--wa-menu-bg-color);
    border-right: 1px solid var(--wa-menu-border-color);

    // 默认风格菜单
    :deep(.el-menu) {
        border: none;

        // 菜单宽度
        &:not(.el-menu--collapse) {
            width: var(--aside-width, 180px);
        }

        // 鼠标经过
        .el-sub-menu__title:hover,
        .el-menu-item:hover:not(.is-active) {
            color: var(--wa-menu-hover-text-color);
            background-color: var(--wa-menu-hover-bg-color);
        }

        // 激活样式
        .el-menu-item.is-active,
        &.el-menu--collapse .el-sub-menu.is-active,
        &.el-menu--collapse .el-sub-menu.is-active .el-sub-menu__title:hover {
            color: var(--wa-menu-active-text-color);
            background-color: var(--wa-menu-active-bg-color);
        }

        // 子级菜单
        ul.el-menu--inline {
            ul.el-menu--inline {
                --el-menu-icon-width: 16px;
                --el-menu-level-padding: 20px;
            }
        }
    }

    // 圆角风格菜单
    &.menu-style-round :deep(.el-menu) {
        --el-menu-item-height: 46px;
        --el-menu-sub-item-height: 46px;
        --el-menu-base-level-padding: 13px;
        &.el-menu--collapse {
            margin: 0 5px;
            .el-menu-item,
            .el-sub-menu__title {
                margin-bottom: 5px;
                border-radius: 6px;
            }
            .el-sub-menu {
                border-radius: 6px;
            }
        }
        &:not(.el-menu--collapse) {
            .el-sub-menu__title {
                margin-right: 5px;
                margin-left: 5px;
                border-radius: 6px;
            }
            .el-menu-item {
                margin: 0 5px 5px;
                border-radius: 6px;
            }
        }
    }
}
</style>
