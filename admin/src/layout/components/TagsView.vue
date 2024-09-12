<template>
    <div class="header-tabs-wrapper">
        <div class="tab-control-prev" @click="onScrollTo('left')">
            <icon name="el-icon-DArrowLeft" :size="16" />
        </div>
        <el-scrollbar ref="scrollbarRef" @wheel.passive="wheelScroll" @scroll="touchScroll">
            <div ref="scrollbarContentRef" class="tab-vessels-wrap">
                <router-link
                    ref="tagsRefs"
                    v-for="(tag) in tabsStore.getTagsViewList"
                    :key="tag.fullPath"
                    :class="`tags-style-${tagsStyle}${isActive(tag) ? ' active' : ''}`"
                    :to="{ path: tag.fullPath }"
                >
                    <span>{{ tag.title }}</span>
                    <icon
                        name="el-icon-close"
                        :color="isActive(tag) ? '' : '#c2c2c2'"
                        :size="12"
                        @click.prevent.stop="onRemoveTab(tag.fullPath)"
                    />
                </router-link>
            </div>
        </el-scrollbar>
        <div class="tab-control-next" @click="onScrollTo('right')">
            <icon name="el-icon-DArrowRight" :size="16" />
        </div>
        <div class="tab-control-down">
            <el-dropdown @command="onCommands">
                <span class="flex items-center px-3">
                    <icon :size="16" name="el-icon-ArrowDown" />
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="closeCurrent"> 关闭当前标签页 </el-dropdown-item>
                        <el-dropdown-item command="closeOther"> 关闭其它标签页 </el-dropdown-item>
                        <el-dropdown-item command="closeAll"> 关闭全部标签页 </el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouteLocationNormalizedLoaded, RouterLink } from 'vue-router'
import { ElScrollbar } from 'element-plus'
import useTabsStore from '@/stores/modules/tabs'
import useConfStore from '@/stores/modules/conf'

const route = useRoute()
const router = useRouter()
const tabsStore = useTabsStore()
const confStore = useConfStore()

// 标签风格
const tagsStyle = computed(() => confStore.tagsStyle)
// 标签页元素的引用数组
const tagsRefs = ref<InstanceType<typeof RouterLink>[]>([])
// 滚动条组件元素的引用
const scrollbarRef = ref<InstanceType<typeof ElScrollbar>>()
// 滚动条内容元素的引用
const scrollbarContentRef = ref<HTMLDivElement>()
// 每次滚动条滚动的距离
const translateDistance: number = 200
// 当前滚动条距离左边的距离
let currentScrollLeft: number = 0

/** 是否激活 */
const isActive = (tag: any) => {
    return tag.path === route.path
}

/** 关闭标签 */
const onRemoveTab = (fullPath: string) => {
    tabsStore.removeTab(router, fullPath)
}

/** 处理指令 */
const onCommands = (command: any) => {
    const fullPath = route.fullPath
    switch (command) {
        case 'closeCurrent':
            tabsStore.removeTab(router, fullPath)
            break
        case 'closeAll':
            tabsStore.removeAllTab(router)
            break
        case 'closeOther':
            tabsStore.removeOtherTab(route)
            break
    }
}

/** 移动到目标的位置 */
const onMoveTo = () => {
    const tagRefs = tagsRefs.value
    for (let i = 0; i < tagRefs.length; i++) {
        // @ts-ignore
        if (route.path === tagRefs[i].$props.to.path) {
            // @ts-ignore
            const el: HTMLElement = tagRefs[i].$el
            const offsetWidth = el.offsetWidth
            const offsetLeft = el.offsetLeft
            const { scrollbarRefWidth } = getScrollWidth()
            // 当前Tag在可视区域左边时
            if (offsetLeft < currentScrollLeft) {
                const distance = currentScrollLeft - offsetLeft
                onScrollTo('left', distance)
                return
            }
            // 当前Tag在可视区域右边时
            const width = scrollbarRefWidth + currentScrollLeft - offsetWidth
            if (offsetLeft > width) {
                const distance = offsetLeft - width
                onScrollTo('right', distance)
                return
            }
        }
    }
}

/** 控制标签左右滚动 */
const onScrollTo = (direction: 'left' | 'right', distance: number = translateDistance) => {
    let scrollLeft = 0
    const { scrollbarContentRefWidth, scrollbarRefWidth, lastDistance } = getScrollWidth()
    // 没有横向滚动条(直接结束)
    if (scrollbarRefWidth > scrollbarContentRefWidth) {
        return
    }
    if (direction === 'left') {
        scrollLeft = Math.max(0, currentScrollLeft - distance)
    } else {
        scrollLeft = Math.min(currentScrollLeft + distance, currentScrollLeft + lastDistance)
    }
    scrollbarRef.value!.setScrollLeft(scrollLeft)
}

/** 滚动条滚动时触发 */
const touchScroll = ({ scrollLeft }: { scrollLeft: number }) => {
    currentScrollLeft = scrollLeft
}

/** 鼠标轮滚动时触发 */
const wheelScroll = ({ deltaY }: WheelEvent) => {
    if (/^-/.test(deltaY.toString())) {
        onScrollTo('left')
    } else {
        onScrollTo('right')
    }
}

/** 取可能需要的宽度 */
const getScrollWidth = () => {
    // 可滚动内容的长度
    const scrollbarContentRefWidth = scrollbarContentRef.value!.clientWidth
    // 滚动可视区的宽度
    const scrollbarRefWidth = scrollbarRef.value!.wrapRef!.clientWidth
    // 剩余可滚动的宽度
    const lastDistance = scrollbarContentRefWidth - scrollbarRefWidth - currentScrollLeft

    return { scrollbarContentRefWidth, scrollbarRefWidth, lastDistance }
}

/** 监听路由变化 */
watch(route,
    (route: RouteLocationNormalizedLoaded) => {
        tabsStore.addTab(route)
        nextTick(onMoveTo)
    }, {
        immediate: true
    }
)
</script>

<style scoped lang="scss">
.header-tabs-wrapper {
    display: flex;
    align-items: center;
    width: 100%;
    height: 36px;
    background-color: var(--wa-tags-bg-color);
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 10%);
    :deep(.el-scrollbar) {
        flex: 1;
        white-space: nowrap;
        .is-horizontal {
            height: 4px;
        }
    }
    .tab-control-down,
    .tab-control-next,
    .tab-control-prev {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 100%;
        overflow: hidden;
        cursor: pointer;
        border-left: 1px solid var(--wa-header-border-color);
        transition: all 0.3s;
        &:hover { background-color: var(--el-bg-color-light, #f6f6f6); }
        .el-dropdown {
            width: 100%;
            height: 100%;
            outline: none !important;
        }
    }
    .tab-control-prev {
        border-right: 1px solid var(--wa-header-border-color);
        border-left: none;
    }
    .tab-vessels-wrap {
        display: inline-block;
        height: 100%;

        // 风格1
        .tags-style-nimble {
            position: relative;
            display: inline-block;
            height: 36px;
            padding: 0 12px 0 15px;
            font-size: 13px;
            line-height: 36px;
            color: var(--wa-tags-text-color);
            border-right: 1px solid var(--wa-tags-nimble-active-bg-color);
            i {
                width: 16px;
                height: 16px;
                margin-bottom: 3px;
                margin-left: 8px;
                vertical-align: middle;
                border-radius: 50%;
                transition: all 0.3s;
                &:hover {
                    color: var(--wa-tags-close-hover-text-color);
                    background-color: var(--wa-tags-close-hover-bg-color);
                }
            }
            &::after {
                position: absolute;
                top: 0;
                left: 0;
                width: 0;
                height: 2px;
                content: "";
                background-color: var(--wa-tags-nimble-after-color);
                border-radius: 0;
                transition: all 0.31s;
            }
            &.active, &:hover {
                color: var(--wa-tags-nimble-active-text-color);
                background-color: var(--wa-tags-nimble-active-bg-color);
                &::after {
                    width: 100%;
                }
            }
        }

        // 风格2
        .tags-style-wedged {
            position: relative;
            display: inline-block;
            height: 26px;
            padding: 0 6px 0 8px;
            margin-top: 5px;
            margin-left: 5px;
            font-size: 12px;
            line-height: 26px;
            color: var(--wa-tags-text-color);
            cursor: pointer;
            border: 1px solid var(--wa-tags-border-color);
            border-radius: 2px;
            &.active, &:hover {
                color: var(--wa-tags-active-text-color);
                background-color: var(--wa-tags-active-bg-color);
                border-color: var(--wa-tags-active-bg-color);
            }
            i {
                width: 14px;
                height: 14px;
                margin-bottom: 2px;
                margin-left: 5px;
                font-size: 10px !important;
                vertical-align: middle;
                border-radius: 50%;
                transition: all 0.3s;
                &:hover {
                    color: var(--wa-tags-close-hover-text-color);
                    background-color: var(--wa-tags-close-hover-bg-color);
                }
            }
            &:last-child {
                margin-right: 5px;
            }
        }

        // 风格3
        .tags-style-smooth {
            position: relative;
            display: inline-block;
            height: 27px;
            padding: 0 6px 0 8px;
            margin-top: 5px;
            margin-left: 5px;
            font-size: 12px;
            line-height: 27px;
            color: var(--wa-tags-text-color);
            cursor: pointer;
            border-radius: 3px;
            transition: all 0.3s;
            &.active, &:hover {
                color: var(--wa-tags-active-text-color);
                background-color: var(--wa-tags-active-bg-color);
            }
            i {
                width: 14px;
                height: 14px;
                margin-bottom: 2px;
                margin-left: 5px;
                font-size: 10px !important;
                vertical-align: middle;
                border-radius: 50%;
                transition: all 0.3s;
                &:hover {
                    color: var(--wa-tags-close-hover-text-color);
                    background-color: var(--wa-tags-close-hover-bg-color);
                }
            }
            &:last-child {
                margin-right: 5px;
            }
        }
    }
}
</style>
