<template>
    <div
        class="h-full cursor-pointer flex items-center px-2"
        @click="refreshView"
    >
        <icon name="el-icon-refresh-right" :size="16" />
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'

const appStore = useAppStore()

const refreshView = () => {
    appStore.refreshView()
}
</script>
