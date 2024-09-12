import { defineStore } from 'pinia'
import {
    LocationQuery,
    RouteLocationNormalized,
    RouteLocationNormalizedLoaded,
    RouteParamsRaw,
    Router,
    RouteRecordName
} from 'vue-router'

interface TabsSate {
    isAnimation: boolean,
    tagsViewList: TabItem[],
    currRouteName: RouteRecordName
}

interface TabItem {
    fullPath: string
    path: string
    name: RouteRecordName
    title: string | unknown | undefined
    query?: LocationQuery
    params?: RouteParamsRaw
}

// 查找标签下标
const __findTabsIndexNum = (fullPath: string, tabList: TabItem[]) => {
    return tabList.findIndex((item: TabItem): boolean => item.fullPath === fullPath)
}

const useTabsStore = defineStore({
    id: 'tabs',
    state: (): TabsSate => ({
        isAnimation: false,
        tagsViewList: [],
        currRouteName: ''
    }),
    getters: {
        getTagsViewList(): TabItem[] {
            return this.tagsViewList
        }
    },
    actions: {
        /**
         * 重置状态
         */
        resetState(): void {
            this.tagsViewList = []
            this.currRouteName = ''
        },
        /**
         * 添加标签
         */
        addTab(route: RouteLocationNormalizedLoaded): void {
            // 路由参数
            const {
                fullPath,
                path,
                name,
                meta,
                query,
                params
            } = route

            // 标签参数
            const tabItem: TabItem = {
                fullPath,
                path,
                query,
                params,
                name: name!,
                title: meta?.title
            }

            // 查找标签
            const tagIndex: number = __findTabsIndexNum(fullPath, this.tagsViewList)
            if (tagIndex !== -1) {
                this.isAnimation = false
                return
            }

            // 加入标签
            this.isAnimation = true
            this.tagsViewList.push(tabItem)
        },
        /**
         * 移除当前标签
         */
        removeTab(router: Router, fullPath: string): void {
            // 获取路由
            const { push, currentRoute } = router

            // 移除标签
            const tagIndex: number = __findTabsIndexNum(fullPath, this.tagsViewList)
            if (this.tagsViewList.length > 1) {
                tagIndex !== -1 && this.tagsViewList.splice(tagIndex, 1)
            }

            // 验证路由
            if (fullPath !== currentRoute.value.fullPath) {
                return
            }

            // 上个标签
            let toTab: TabItem | null = null
            if (tagIndex === 0) {
                toTab = this.tagsViewList[tagIndex]
            } else {
                toTab = this.tagsViewList[tagIndex - 1]
            }

            // 跳转路由
            const toRoute: any = {
                path: toTab.path,
                query: toTab.query || {},
                params: toTab.params || {}
            }
            push(toRoute).then((): void => { })
        },
        /**
         * 移除所有标签
         */
        removeAllTab(router: Router): void {
            // 路由参数
            const { push, currentRoute } = router
            const { name } = unref(currentRoute)

            // 移除标签
            if (name === this.currRouteName) {
                this.removeOtherTab(currentRoute.value)
                return
            }

            // 清空数据
            this.tagsViewList = []

            // 跳转首页
            push('/').then((): void => { })
        },
        /**
         * 移除其它标签
         */
        removeOtherTab(route: RouteLocationNormalized): void {
            // 保留当前标签
            this.tagsViewList = this.tagsViewList.filter((item: TabItem): boolean => item.fullPath === route.fullPath)
        },
        /**
         * 设置当前路由名称
         */
        setCurrRouteName(name: RouteRecordName): void {
            this.currRouteName = name
        }
    }
})

export default useTabsStore
