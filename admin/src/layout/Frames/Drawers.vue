<template>
    <div class="layout-aside">
        <el-drawer
            v-model="isDrawer"
            direction="ltr"
            :with-header="false"
            size="var(--aside-width)"
        >
            <sidebar-menu />
        </el-drawer>

        <slot></slot>
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app.ts'
import SidebarMenu from '@/layout/Frames/Classic/Asides.vue'

const appStore = useAppStore()

const isMobile = computed(() => appStore.isMobile)
const isDrawer = computed({
    get() {
        return !appStore.isCollapsed && isMobile.value
    },
    set(value) {
        appStore.toCollapsed(!value)
    }
})
</script>

<style scoped lang="scss">
.layout-aside {
    :deep(.el-drawer__body) {
        padding: 0 ;
    }
}
</style>
