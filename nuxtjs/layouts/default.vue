<template>
    <ElContainer class="layout-default">
        <layout-account />
        <layout-header />
        <ElMain>
            <slot></slot>
            <template v-if="$slots?.container">
                <div class="container">
                    <slot name="container"></slot>
                </div>
            </template>
        </ElMain>
        <layout-footer />
    </ElContainer>
</template>

<script setup lang="ts">
import LayoutAccount from '~/layouts/components/Account/index.vue'
import LayoutHeader from '~/layouts/components/Header/index.vue'
import LayoutFooter from '~/layouts/components/Footer/index.vue'
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