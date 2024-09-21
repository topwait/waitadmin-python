<template>
    <frames-classic v-if="layout === 'classic'" />
    <frames-columns v-if="layout === 'columns'" />
    <frames-regular v-if="layout === 'regular'" />
    <frames-roomier v-if="layout === 'roomier'" />
</template>

<script setup lang="ts">
import useConfStore from '@/stores/modules/conf'
import FramesClassic from './Frames/Classic/index.vue'
import FramesColumns from './Frames/Columns/index.vue'
import FramesRegular from './Frames/Regular/index.vue'
import FramesRoomier from './Frames/Roomier/index.vue'

const confStore = useConfStore()

const layout = computed<string>(() => confStore.layout)
</script>
