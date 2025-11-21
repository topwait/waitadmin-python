<template>
    <el-image :style="styles" v-bind="props" />
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { CSSProperties } from 'vue'
import { imageProps } from 'element-plus'
import toolsUtil from '@/utils/tools'

const props = defineProps({
    width: {
        type: [String, Number],
        default: 'auto'
    },
    height: {
        type: [String, Number],
        default: 'auto'
    },
    radius: {
        type: [String, Number],
        default: 0
    },
    ...imageProps
})

const styles = computed<CSSProperties>(() => {
    return {
        width: toolsUtil.addUnit(props.width),
        height: toolsUtil.addUnit(props.height),
        borderRadius: toolsUtil.addUnit(props.radius)
    }
})
</script>

<style lang="scss" scoped>
.el-image {
    display: block;
    :deep(.el-image__error) {
        font-size: 12px;
    }
}
</style>
