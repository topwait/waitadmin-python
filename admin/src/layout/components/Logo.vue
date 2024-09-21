<template>
    <div class="logo" :class="(isCollapsed || size === 'small') ? '' : 'normal'">
        <img
            v-if="isCollapsed || size === 'small'"
            :src="themeStyles === 'white' ? sysConfig.logo_black_small : sysConfig.logo_white_small"
            alt="logo"
        />

        <img v-else
             :src="themeStyles === 'white' ? sysConfig.logo_black_big : sysConfig.logo_white_big"
             alt="logo"
        />
    </div>
</template>

<script setup lang="ts">
import useAppStore from '@/stores/modules/app'
import useConfStore from '@/stores/modules/conf'

defineProps({
    size: {
        type: String,
        default: ''
    }
})

const appStore = useAppStore()
const confStore = useConfStore()

// 是否收缩
const isCollapsed = computed<boolean>(() => appStore.isCollapsed)
const sysConfig = computed(() => appStore.config)


// 颜色风格
const themeStyles = computed<string>(
    () => confStore.theme.startsWith('white') ? 'white' : 'black'
)
</script>

<style scoped lang="scss">
.logo {
    width: 60px;
    height: 50px;
    margin: auto;
    cursor: pointer;
    img {
        width: 100%;
        height: 50px;
        margin: auto;
        animation: logoAnimation 0.3s ease-in-out;
    }
    &.normal {
        width: var(--aside-width, 180px);
        transition: width .6s ease;
    }
}

@keyframes logoAnimation {
    0% {
        transform: scale(0)
    }
    80% {
        transform: scale(1.2)
    }
    100% {
        transform: scale(1)
    }
}
</style>
