<template>
    <div
        class="h-full cursor-pointer flex items-center px-2"
        @click="toggleFullscreen"
    >
        <icon
            :name="`el-icon-${isFullscreen ? 'crop' : 'full-screen'}`"
            :size="16"
        />
    </div>
</template>

<script setup lang="ts">
import { useFullscreen } from '@vueuse/core'

const { toggle: toggleFullscreen, isFullscreen } = useFullscreen()
</script>
