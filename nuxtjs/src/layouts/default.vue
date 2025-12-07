<template>
    <ElContainer class="layout-default">
        <layout-account />
        <layout-header />
        <el-main>
            <slot></slot>
            <template v-if="$slots?.container">
                <div class="container">
                    <slot name="container"></slot>
                </div>
            </template>
        </el-main>
        <layout-footer />
    </ElContainer>
</template>

<script setup lang="ts">
import LayoutAccount from '@/layouts/components/account/index.vue'
import LayoutHeader from '@/layouts/components/header/index.vue'
import LayoutFooter from '@/layouts/components/footer/index.vue'
</script>

<style scoped lang="scss">
.layout-default {
    flex-direction: column;
    min-height: 100vh;
    background-color: var(--el-bg-color-page);
    --el-footer-height: 36px;
    .el-main {
        display: flex;
        flex-direction: column;
        padding: 0;
        .container {
            display: flex;
            flex: 1;
            width: 1200px;
            padding: 0;
            margin: 0 auto;
        }
    }
}
</style>
