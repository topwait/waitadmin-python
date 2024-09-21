<template>
    <div class="aside-menu-container" :class="`menu-style-${menuLightStyle}`">

        <div class="column-menus-main">
            <logo v-if="isLayoutLogo" size="small"/>
            <el-scrollbar>
                <ul>
                    <li v-for="(route, index) in routes"
                        :key="index"
                        :class="menusIndex === index ? 'active' : ''"
                        @click="onSwitchMenu(route, index)"
                    >
                        <icon :name="route.meta.icon" :size="14" />
                        <cite>{{  route.meta.title }}</cite>
                    </li>
                </ul>
            </el-scrollbar>
        </div>

        <div
            v-if="routes[menusIndex].children"
            class="column-menus-sub"
            :class="isCollapsed ? 'shrink' : ''"
        >
            <div class="title">{{ routes[menusIndex]?.meta?.title }}</div>
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
                        v-for="route in routes[menusIndex].children"
                        :key="resolvePath(route.path)"
                        :route="route"
                        :route-path="resolvePath(route.path)"
                    />
                </el-menu>
            </el-scrollbar>
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouteRecordRaw } from 'vue-router'
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import useConfStore from '@/stores/modules/conf'
import validateUtil from '@/utils/validate'
import Logo from '@/layout/components/Logo.vue'
import MenuItem from '@/layout/components/MenuItem.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

const firstsMenu: Ref<string> = ref('')
const menusIndex: Ref<number> = ref(0)

const routes = computed(() => userStore.routes)
const activeMenu = computed<string>(() => route.path)
const isCollapsed = computed<boolean>(() => appStore.isCollapsed)
const isLayoutLogo = computed<boolean>(() => confStore.isLayoutLogo)
const isUniqueOpened = computed<boolean>(() => !confStore.isUniqueOpened)
const menuLightStyle = computed<boolean>(() => confStore.menuLightStyle)

/**
 * 初始菜单选中
 *
 * @param {boolean} isJump (是否跳转: true=是, false=否)
 * @returns {void}
 */
const initChoiceMenu = (isJump: boolean = true): void => {
    for (let i = 0; i < routes.value.length; i++) {
        const path = routes.value[i].path
        if (activeMenu.value.startsWith(path)) {
            menusIndex.value = i
            firstsMenu.value = path + '/'
            if (isJump) {
                router.push(activeMenu.value)
            }
            break
        }
    }
}

/**
 * 切换一级菜单
 *
 * @param {RouteRecordRaw} route (路由对象)
 * @param {number} index (一级菜单下标)
 */
const onSwitchMenu = (route: RouteRecordRaw, index: number): void => {
    if (!validateUtil.isExternal(route.path)) {
        menusIndex.value = index
        firstsMenu.value = route.path + '/'
        appStore.isCollapsed = false
        router.push(firstRoutes(route))
    } else {
        window.open(route.path, '_blank')
    }
}

/**
 * 处理路由路径
 *
 * @param {string} path (页面路径)
 * @returns {string}
 */
const resolvePath = (path: string): string => {
    const isExternal = validateUtil.isExternal(path)
    if (isExternal) {
        return path
    }
    path = firstsMenu.value + path
    return path
}

/**
 * 首个有效路径
 *
 * @param route (路由对象)
 * @param path  (页面路径)
 */
const firstRoutes = (route: any, path: string = ''): any => {
    if (route.path) {
        path += path ? '/' + route.path : route.path
    }

    if (route.children && route.children.length > 0) {
        return firstRoutes(route.children[0], path)
    }

    return path
}

watch(
    () => activeMenu.value,
    () => {
        initChoiceMenu(false)
        appStore.isCollapsed = false
    }
)

initChoiceMenu()
</script>

<style scoped lang="scss">
.aside-menu-container  {
    box-sizing: border-box;
    display: flex;
    height: 100%;
    overflow: hidden;

    // 主菜单
    .column-menus-main {
        width: 66px;
        background-color: var(--wa-menu-col-m-bg-color);
        border-right: 1px solid var(--wa-menu-border-color);
        li {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 50px;
            margin: 3px 0;
            color: var(--wa-menu-col-m-text-color);
            text-align: center;
            cursor: pointer;
            background-color: transparent;
            transition: background-color 0.3s ease;
            i {
                margin-bottom: 2px;
            }
            cite {
                display: block;
                margin-top: 5px;
                font-size: 12px;
                font-style: normal;
                line-height: 12px;
            }
            &.active {
                color: var(--wa-menu-col-m-active-text-color);
                background: var(--wa-menu-col-m-active-bg-color);
                transition: .3s ease-in-out;
            }
            &:not(.active):hover {
                color: var(--wa-menu-col-m-hover-text-color);
                background: var(--wa-menu-col-m-hover-bg-color);
                &::after {
                    height: 100%;
                }
            }
            &::after {
                position: absolute;
                top: 0;
                left: 0;
                width: 3px;
                height: 0;
                content: "";
                background-color: var(--wa-menu-col-m-active-bg-color);
                border-radius: 1px;
                transition: all 0.31s;
            }
        }
    }

    // 子菜单
    .column-menus-sub {
        display: flex;
        flex-direction: column;
        width: 160px;
        background-color: var(--wa-menu-col-s-bg-color);
        border-right: 1px solid var(--wa-header-border-color);
        transition: width .2s ease;
        .title {
            height: 50px;
            padding-left: 20px;
            margin-bottom: 5px;
            font-size: 14px;
            font-weight: 500;
            line-height: 50px;
            color: var(--wa-menu-col-s-text-color);
            border-bottom: 1px solid var(--wa-header-border-color);
        }
        &.shrink {
            width: 0 !important;
        }
        :deep(.el-menu) {
            border: none;
            --el-menu-icon-width: 16px;
            --el-menu-item-height: 46px;
            --el-menu-sub-item-height: 46px;
            --el-menu-level-padding: 10px;
            --el-menu-text-color: var(--wa-menu-col-s-text-color);
            .el-menu-item.is-active {
                color: var(--wa-menu-col-s-active-text-color);
                background-color: var(--wa-menu-col-s-active-bg-color);
            }
            .el-menu-item:hover:not(.is-active),
            .el-sub-menu__title:hover {
                color: var(--wa-menu-col-s-hover-text-color);
                background-color: var(--wa-menu-col-s-hover-bg-color);
            }
            .el-icon {
                margin-right: 3px;
            }
            span {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
        }
    }

    // 圆角风
    &.menu-style-round {
        .column-menus-main {
            ul {
                padding: 0 5px;
                li {
                    border-radius: 6px;
                }
                li::after {
                    left: -5px;
                }
            }
        }
        .column-menus-sub {
            :deep(.el-menu) {
                .el-sub-menu__title,
                .el-menu-item {
                    margin: 0 5px;
                    border-radius: 6px;
                }
            }
        }
    }
}
</style>
