<template>
    <el-image :style="styles" v-bind="props" />
</template>

<script setup lang="ts">
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
    borderTopLeftRadius: {
        type: [String, Number],
        default: 0
    },
    borderTopRightRadius: {
        type: [String, Number],
        default: 0
    },
    borderBottomLeftRadius: {
        type: [String, Number],
        default: 0
    },
    borderBottomRightRadius: {
        type: [String, Number],
        default: 0
    },
    ...imageProps
})

const styles = computed<CSSProperties>(() => {
    let css: any = {
        width: toolsUtil.addUnit(props.width),
        height: toolsUtil.addUnit(props.height)
    }
    if (props.radius) {
        css.borderRadius = toolsUtil.addUnit(props.radius)
    }
    if (props.borderTopLeftRadius) {
        css.borderTopLeftRadius = toolsUtil.addUnit(props.borderTopLeftRadius)
    }
    if (props.borderTopRightRadius) {
        css.borderTopRightRadius = toolsUtil.addUnit(props.borderTopRightRadius)
    }
    if (props.borderBottomLeftRadius) {
        css.borderBottomLeftRadius = toolsUtil.addUnit(props.borderBottomLeftRadius)
    }
    if (props.borderBottomRightRadius) {
        css.borderBottomRightRadius = toolsUtil.addUnit(props.borderBottomRightRadius)
    }
    return css
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
