<template>
    <component :is="linkType" v-bind="linkProps">
        <slot></slot>
    </component>
</template>

<script setup lang="ts">
const props = defineProps({
    to: {
        type: String,
        default: '',
        require: true
    }
})

// 计算是否外部链接
const isExternal = computed(() => {
    const external = /^(https?:|mailto:|tel:)/.test(props.to)
    return typeof props.to !== 'object' && external
})

// 计算链接类型标签
const linkType = computed(() => {
    if (isExternal.value) {
        return 'a'
    }
    return 'router-link'
})

// 计算链接跳转属性
const linkProps = computed(() => {
    if (isExternal.value) {
        return {
            href: props.to,
            target: '_blank'
        }
    }
    return props
})
</script>
