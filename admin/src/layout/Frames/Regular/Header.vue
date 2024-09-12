<template>
    <div class="layout-header">
        <logo v-if="!isMobile && isLayoutLogo" />

        <ul class="navbar-left" v-if="isMobile">
            <li><stretch /></li>
        </ul>

        <el-scrollbar v-if="!isMobile">
            <ul class="navbar-menus">
                <li v-for="(route, index) in routes"
                    :key="index"
                    :class="menusIndex === index ? 'active' : ''"
                    @click="onSwitchMenu(route, index)"
                >
                    <div class="vertical">
                        <icon v-if="route.meta.icon" :name="route.meta.icon" :size="15" />
                        <cite>{{ route.meta.title }}</cite>
                    </div>
                </li>
            </ul>
        </el-scrollbar>

        <ul class="navbar-right">
            <li><refresh /></li>
            <li><screens /></li>
            <li><user-dropdown /></li>
            <li><system-setting /></li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { RouteRecordRaw } from 'vue-router'
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import useConfStore from '@/stores/modules/conf'
import validateUtil from '@/utils/validate'
import Logo from '../../components/Logo.vue'
import Stretch from '@/layout/Header/Stretch.vue'
import Refresh from '@/layout/Header/Refresh.vue'
import Screens from '@/layout/Header/Screens.vue'
import UserDropdown from '@/layout/Header/UserDropdown.vue'
import SystemSetting from '@/layout/Header/SystemSetting.vue'

const emit = defineEmits(['change'])

interface Props {
    defaultIndex: number
}

const props = defineProps<Props>()

const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

const routes = computed(() => userStore.routes)
const isMobile = computed<boolean>(() => appStore.isMobile)
const isLayoutLogo = computed<boolean>(() => confStore.isLayoutLogo)

const menusIndex: Ref<number> = ref(props.defaultIndex)

/**
 * 切换一级菜单
 *
 * @param {RouteRecordRaw} route (路由对象)
 * @param {number} index (一级菜单下标)
 */
const onSwitchMenu = (route: RouteRecordRaw, index: number): void => {
    if (!validateUtil.isExternal(route.path)) {
        menusIndex.value = index
        emit('change', route, index)
    } else {
        window.open(route.path, '_blank')
    }
}

watch(
    () => props.defaultIndex,
    (value) => {
        menusIndex.value = value
    }
)
</script>

<style scoped lang="scss">
.layout-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 65px;
    background-color: var(--wa-menu-regular-m-bg-color);
    border-bottom: 1px solid var( --wa-header-border-color);

    // 菜单滚动
    :deep(.el-scrollbar) {
        flex: 1;
        white-space: nowrap;
        .el-scrollbar__view {
            height: 100%;
        }
    }

    // 导航菜单
    .navbar-menus {
        display: flex;
        height: 100%;
        li {
            position: relative;
            display: flex;
            flex-shrink: 0;
            height: 100%;
            margin: 0 20px;
            font-size: 14px;
            font-weight: 400;
            color: var(--wa-menu-regular-m-text-color);
            cursor: pointer;
            transition: all .2s ease-in-out;
            &.active {
                .vertical {
                    color: var(--wa-menu-regular-m-active-text-color);
                    background: var(--wa-menu-regular-m-active-bg-color);
                }
                .vertical::after {
                    width: 100%;
                }
            }
            .vertical {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                height: 100%;
                i {
                    padding-top: 1px;
                    margin-right: 3px;
                }
                cite {
                    position: relative;
                    display: block;
                    padding-top: 2px;
                    font-size: 14px;
                    font-style: normal;
                    line-height: 14px;
                }
                &::after {
                    position: absolute;
                    bottom: 2px;
                    left: 0;
                    width: 0;
                    height: 2px;
                    content: "";
                    background-color: var(--wa-menu-regular-m-active-br-color);
                    border-radius: 0;
                    transition: all 0.31s;
                }
            }

            &:not(.active):hover {
                color: var(--wa-menu-regular-m-hover-text-color);
                background-color: var(--wa-menu-regular-m-hover-bg-color);
                transition: all .2s ease-in-out;
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
            color: var(--wa-menu-regular-m-text-color);
            cursor: pointer;
            :deep(.el-dropdown) {
                .el-tooltip__trigger > i {
                    color: var(--wa-menu-regular-m-text-color);
                }
            }
            &:hover {
                background: hsl(0deg 0% 100% / 5%);
            }
        }
    }
}
</style>
