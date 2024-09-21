<template>
    <svg aria-hidden="true">
        <use :xlink:href="symbolId" fill="currentColor" />
    </svg>
</template>

<script lang="ts">
export default defineComponent({
    props: {
        name: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const symbolId = computed(() => `#${props.name}`)
        return { symbolId }
    }
})
</script>
