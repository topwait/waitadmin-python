<template>
    <el-breadcrumb separator="/">
        <el-breadcrumb-item v-for="(item, index) in breadcrumbData" :key="item.path">
            <span
                v-if="index === breadcrumbData.length - 1"
                class="no-redirect"
            >
                {{ item.meta?.title }}
            </span>

            <span v-else class="redirect">
                {{ item.meta?.title }}
            </span>
        </el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script setup lang="ts">
import { RouteLocationMatched, useRoute  } from 'vue-router'

const breadcrumbData: Ref<RouteLocationMatched[]> = ref([])
const getBreadcrumbData = () => {
    breadcrumbData.value = route.matched.filter(
        item => item.meta && item.meta.title
    )
}

const route = useRoute()
watch(
    route,
    () => {
        getBreadcrumbData()
    },
    {
        immediate: true
    }
)
</script>

<style scoped lang="scss">
.el-breadcrumb {
    padding: 0 10px;
    cursor: text;
}
</style>
