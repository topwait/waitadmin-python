<template>
    <template v-if="!route.meta?.hidden">
        <el-sub-menu v-if="isRouteChildren" :index="routePath">
            <template #title>
                <icon
                    v-if="route.meta?.icon"
                    :name="route.meta?.icon + ''"
                    :size="16"
                />
                <i v-else class="ml-[8px] mr-[5px]"></i>
                <span>{{ route.meta?.title }}</span>
            </template>
            <menu-item
                v-for="item in route.children"
                :key="makeResolvePath(item.path)"
                :route-path="makeResolvePath(item.path)"
                :route="item"
            />
        </el-sub-menu>

        <template v-else>
            <app-link v-if="checkIsExternal(routePath)" :to="`${routePath}?${queryStr}`">
                <el-menu-item index="">
                    <icon
                        v-if="route.meta?.icon"
                        :name="route.meta?.icon + ''"
                        :size="16"
                    />
                    <i v-else class="ml-[8px] mr-[5px]"></i>
                    <template #title>
                        <span>{{ route.meta?.title }}</span>
                    </template>
                </el-menu-item>
            </app-link>

            <el-menu-item v-else :index="routePath">
                <icon
                    v-if="route.meta?.icon"
                    :name="route.meta?.icon + ''"
                    :size="16"
                />
                <i v-else class="ml-[8px] mr-[5px]"></i>
                <template #title>
                    <span>{{ route.meta?.title }}</span>
                </template>
            </el-menu-item>
        </template>
    </template>
</template>

<script setup lang="ts">
import { RouteRecordRaw } from 'vue-router'
import toolsUtil from '@/utils/tools'
import AppLink from './Link.vue'

interface Props {
    route: RouteRecordRaw,
    routePath: string
}

const props = defineProps<Props>()

// 计算是否存在子级
const isRouteChildren = computed(() => {
    const children: RouteRecordRaw[] = props.route.children ?? []
    return !!children.filter((item) => !item.meta?.hidden).length
})

// 计算对象为Query
const queryStr = computed<string>(() => {
    const query = props.route.meta?.query as string
    try {
        const queryObj = JSON.parse(query)
        return toolsUtil.objectToQuery(queryObj)
    } catch (error) {
        return query
    }
})

/**
 * 处理生成正确路径
 *
 * @param {string} path (路径)
 * @returns {string}
 */
const makeResolvePath = (path: string): string => {
    if (!path || checkIsExternal(path)) {
        return path
    }

    const pathStr = `${props.routePath}/${path}`
    const newPath = pathStr.replace('//', '/')
    const lengths = newPath.length
    if (newPath[lengths - 1] === '/') {
        return newPath.slice(0, lengths - 1)
    }

    return newPath
}

/**
 * 验证是否外部链接
 *
 * @param path (路径)
 * @returns {boolean}
 */
const checkIsExternal = (path: string): boolean => {
    return /^(https?:|mailto:|tel:)/.test(path)
}
</script>
