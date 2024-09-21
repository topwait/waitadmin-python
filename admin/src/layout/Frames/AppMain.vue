<template>
    <main ref="mainRef">
        <el-scrollbar>
            <div class="router-view-main">
                <router-view v-if="isRouteShow" v-slot="{ Component, route }">
                    <transition :name="(isAnimation || !isKeepAlive) ? pagesAnimation : ''" mode="out-in" appear>
                        <keep-alive :include="!isKeepAlive ? [] : undefined">
                            <component :is="Component" :key="route.fullPath" />
                        </keep-alive>
                    </transition>
                </router-view>
            </div>
        </el-scrollbar>
    </main>
</template>

<script setup lang="ts">
import {useElementSize, watchThrottled} from '@vueuse/core'
import useAppStore from '@/stores/modules/app'
import useTabsStore from '@/stores/modules/tabs'
import useConfStore from '@/stores/modules/conf'

const appStore = useAppStore()
const tabsStore = useTabsStore()
const confStore = useConfStore()

const mainRef = shallowRef<HTMLDivElement>()
const isAnimation = computed(() => tabsStore.isAnimation)
const isRouteShow = computed<boolean>(() => appStore.isRouteShow)
const isKeepAlive = computed<boolean>(() => confStore.isKeepAlive)
const pagesAnimation = computed<string>(() => confStore.pagesAnimation)

const { height } = useElementSize(mainRef)
watchThrottled(height, (val) => {
    appStore.layoutHeight = val
})
</script>

<style scoped lang="scss">
main {
    width: 100%;
    height: 100%;
    margin-top: 0.5px;
    overflow: hidden;
    .router-view-main {
        position: relative;
        box-sizing: border-box;
        padding: 15px;
    }
}

// 左滑动画
.slide-left {
    &-enter-active,
    &-leave-active {
        transition: opacity 0.5s ease-out, transform 0.5s ease-out;
        will-change: opacity, transform;
    }

    &-enter-from,
    &-leave-to {
        opacity: 0;
        transform: translateX(2%);
    }

    &-enter-to,
    &-leave-from {
        opacity: 1;
        transform: translateX(0%);
    }
}

// 右滑动画
.slide-right {
    &-enter-active {
        transition: opacity 0.5s ease-out, transform 0.5s ease-out;
        will-change: opacity, transform;
    }

    &-leave-active {
        transition: opacity 0.3s ease-out, transform 0.3s ease-out;
        will-change: opacity, transform;
    }

    &-leave-from,
    &-enter-to {
        opacity: 1;
        transform: translateX(0%);
    }

    &-enter-from,
    &-leave-to {
        opacity: 0;
        transform: translateX(2%);
    }
}

// 渐显动画
.slide-fade {
    &-enter-active {
        transition: opacity 0.5s ease-out;
        will-change: opacity;
    }

    &-leave-active {
        transition: opacity 0.3s ease-out;
        will-change: opacity;
    }

    &-leave-from,
    &-enter-to {
        opacity: 1;
    }

    &-enter-from,
    &-leave-to {
        opacity: 0;
    }
}
</style>
