<template>
    <div class="layout-header">
        <logo v-if="!isMobile && isLayoutLogo" />

        <ul class="navbar-left" v-if="isMobile">
            <li><stretch /></li>
        </ul>

        <div class="navbar-menus" v-if="!isMobile">
            <el-scrollbar >
                <el-menu
                    mode="horizontal"
                    :ellipsis="false"
                    :default-active="activeMenu"
                    :unique-opened="isUniqueOpened"
                    text-color="var(--wa-menu-roomier-text-color)"
                    active-text-color="var(--wa-menu-roomier-active-text-color)"
                    background-color="var(--wa-menu-roomier-bg-color)"
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

        <ul class="navbar-right">
            <li><refresh /></li>
            <li><screens /></li>
            <li><user-dropdown /></li>
            <li><system-setting /></li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import useConfStore from '@/stores/modules/conf'
import Logo from '../../components/Logo.vue'
import Stretch from '@/layout/Header/Stretch.vue'
import Refresh from '@/layout/Header/Refresh.vue'
import Screens from '@/layout/Header/Screens.vue'
import UserDropdown from '@/layout/Header/UserDropdown.vue'
import SystemSetting from '@/layout/Header/SystemSetting.vue'
import MenuItem from '@/layout/components/MenuItem.vue'

const route = useRoute()
const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

const routes = computed(() => userStore.routes)
const isMobile = computed(() => appStore.isMobile)
const activeMenu = computed<string>(() => route.path)
const isLayoutLogo = computed<boolean>(() => confStore.isLayoutLogo)
const isUniqueOpened = computed<boolean>(() => !confStore.isUniqueOpened)
</script>

<style scoped lang="scss">
.layout-header {
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 52px;
    background-color: var(--wa-menu-roomier-bg-color);
    border-bottom: 1px solid var(--wa-menu-border-color);

    // 导航菜单
    .navbar-menus {
        flex: 1;
        overflow: hidden;
        :deep(.el-menu) {
            &.el-menu--horizontal {
                box-sizing: border-box;
                display: flex;
                width: 100%;
                height: 100%;
                border-bottom: none !important;
                &>.el-menu-item.is-active,
                .el-menu-item:not(.is-disabled):focus {
                    color: var(--wa-menu-roomier-active-text-color) !important;
                    background-color: var(--wa-menu-roomier-active-bg-color) !important;
                }
                .el-sub-menu.is-active>.el-sub-menu__title {
                    color: var(--wa-menu-roomier-active-text-color) !important;
                }
                .el-menu-item:not(.is-disabled):focus {
                    background-color: var(--wa-menu-roomier-bg-active-color);
                }
            }

            // 菜单边距
            &:not(.el-menu--collapse) {
                .el-sub-menu__title {
                    padding: 0 14px;
                }
            }

            // 菜单图标
            .el-menu-item [class^="el-icon"],
            .el-sub-menu .el-icon {
                margin-right: 2px;
            }

            // 子级图标
            .el-sub-menu .el-sub-menu__icon-arrow {
                position: static;
                margin-top: -3px;
                margin-left: 8px;
            }

            // 激活边框
            .el-menu-item.is-active,
            .el-sub-menu.is-active .el-sub-menu__title {
                border-color: var(--theme-color);
            }

            // 鼠标经过
            .el-menu-item:hover,
            .el-sub-menu__title:hover {
                color: var(--wa-menu-roomier-hover-text-color) !important;
                background-color: var(--wa-menu-roomier-hover-bg-color);
            }
        }
    }

    // 导航右侧
    .navbar-left,
    .navbar-right {
        display: flex;
        align-items: center;
        height: 100%;
        padding: 0 10px;
        li {
            display: flex;
            align-items: center;
            height: 100%;
            color: var(--wa-menu-text-color);
            cursor: pointer;
            :deep(.el-dropdown) {
                .el-tooltip__trigger > i {
                    color: var(--wa-menu-text-color);
                }
            }
            &:hover {
                background: hsl(0deg 0% 100% / 5%);
            }
        }
    }
}
</style>
