<template>
    <div class="hover-close">
        <slot></slot>
        <div v-if="showClose" class="close" @click.stop="handleClose">
            <icon :size="12" name="el-icon-CloseBold" />
        </div>
    </div>
</template>

<script setup lang="ts">
const emits = defineEmits(['close'])

defineProps({
    showClose: {
        type: Boolean,
        default: true
    }
})

const handleClose = () => {
    emits('close')
}
</script>

<style scoped lang="scss">
.hover-close {
    position: relative;
    .close {
        position: absolute;
        top: -7px;
        right: -7px;
        display: none;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        color: #ffffff;
        cursor: pointer;
        background-color: rgb(0 0 0 / 30%);
        border-radius: 50%;
        &:hover {
            background-color: rgb(0 0 0 / 50%);
        }
    }
    &:hover > .close {
        display: flex;
    }
}
</style>
