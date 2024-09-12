<template>
    <div class="column-menus-sub" :class="`menu-style-${menuLightStyle}`">
        <el-scrollbar>
            <el-menu
                mode="vertical"
                :default-active="activeMenu"
                :unique-opened="isUniqueOpened"
                text-color="var(--wa-menu-regular-s-text-color)"
                active-text-color="var(--wa-menu-regular-s-active-text-color)"
                background-color="var(--wa-menu-regular-s-bg-color)"
                router
            >
                <menu-item
                    v-for="route in subRouters"
                    :key="resolvePath(route.path)"
                    :route="route"
                    :route-path="resolvePath(route.path)"
                />
            </el-menu>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import { RouteRecordRaw } from 'vue-router'
import useConfStore from '@/stores/modules/conf'
import validateUtil from '@/utils/validate'
import MenuItem from '@/layout/components/MenuItem.vue'

interface Props {
    firstsMenu: string,
    subRouters: RouteRecordRaw[]
}

const props = defineProps<Props>()

const route = useRoute()
const confStore = useConfStore()

const activeMenu = computed<string>(() => route.path)
const isUniqueOpened = computed<boolean>(() => !confStore.isUniqueOpened)
const menuLightStyle = computed<boolean>(() => confStore.menuLightStyle)

/**
 * 处理路由路径
 *
 * @param {string} path
 * @returns {string}
 */
const resolvePath = (path: string): string => {
    const isExternal = validateUtil.isExternal(path)
    if (isExternal) {
        return path
    }
    path = props.firstsMenu + path
    return path
}
</script>

<style scoped lang="scss">
.column-menus-sub {
    flex: none;
    width: 180px;
    padding-top: 8px;
    background-color: var(--wa-menu-regular-s-bg-color);
    border-right: 1px solid var(--wa-header-border-color);
    :deep(.el-menu) {
        // 垂直菜单
        &.el-menu--vertical {
            box-sizing: border-box;
            width: 100%;
            border-right: none !important;
        }

        // 激活样式
        .el-menu-item.is-active {
            color: var(--wa-menu-regular-s-active-text-color);
            background-color: var(--wa-menu-regular-s-active-bg-color);
            transition: all .2s ease-in-out;
        }

        // 鼠标经过
        .el-sub-menu__title:hover,
        .el-menu-item:hover:not(.is-active) {
            color: var(--wa-menu-regular-s-hover-text-color);
            background-color: var(--wa-menu-regular-s-hover-bg-color);
            transition: all .2s ease-in-out;
        }
    }

    // 圆角风格
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
                margin: 5px;
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
