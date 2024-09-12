<template>
    <div class="layout-container">
        <drawers />
        <layout-header :defaultIndex="menusIndex" @change="onOpenSubmenu" />
        <div class="layout-main">
            <layout-asides
                v-if="subRouters?.length > 0 && !isMobile"
                :firstsMenu="firstsMenu"
                :subRouters="subRouters"
            />
            <div class="w-full">
                <tags-view v-if="isTabMultiple" />
                <layout-main />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouteRecordRaw } from 'vue-router'
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import useConfStore from '@/stores/modules/conf'
import validateUtil from '@/utils/validate'
import TagsView from '../../components/TagsView.vue'
import LayoutAsides from './Asides.vue'
import LayoutHeader from './Header.vue'
import LayoutMain from '../AppMain.vue'
import Drawers from '../Drawers.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

const routes = computed(() => userStore.routes)
const isMobile = computed(() => appStore.isMobile)
const isTabMultiple = computed(() => confStore.isTabMultiple)

const subRouters = ref([])
const firstsMenu: Ref<string> = ref('')
const menusIndex: Ref<number> = ref(0)
const activeMenu = computed<string>(() => route.path)

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
            subRouters.value = routes.value[i].children
            if (isJump) {
                router.push(activeMenu.value)
            }
            break
        }
    }
}

/**
 * 打开指定子菜单
 *
 * @param {RouteRecordRaw} route (路由对象)
 * @param {number} index (一级菜单下标)
 */
const onOpenSubmenu = (route: RouteRecordRaw, index: number): void => {
    if (!validateUtil.isExternal(route.path)) {
        menusIndex.value = index
        firstsMenu.value = route.path + '/'
        router.push(firstRoutes(route))
        subRouters.value = routes.value[index].children
    } else {
        window.open(route.path, '_blank')
    }
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
    }
)

initChoiceMenu()
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
