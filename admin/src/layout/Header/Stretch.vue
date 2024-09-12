<template>
    <div
        class="h-full cursor-pointer flex items-center px-2"
        @click="toCollapsed"
    >
        <icon
            :name="`svg-icon-stretch-${isCollapsed ? 'right' : 'left'}`"
            :size="16"
        />
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'

const appStore = useAppStore()

const isCollapsed = computed(() => appStore.isCollapsed)

const toCollapsed = () => {
    appStore.toCollapsed()
}
</script>
