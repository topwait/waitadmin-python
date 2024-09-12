<template>
    <nuxt-icon :name="symbolId" :filled="true" />
</template>

<script lang="ts">
import { SVG_ICON_PREFIX } from '~/plugins/icons'

export default defineComponent({
    props: {
        name: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const iconName = props.name.replace(SVG_ICON_PREFIX, '')
        const symbolId = computed(() => `${iconName}`)
        return { symbolId }
    }
})
</script>

<style lang="scss">
.nuxt-icon svg {
    margin-bottom: auto;
}
</style>
