<template>
    <div v-if="showType === 'avatar'" class="avatar">
        <el-avatar :size="70" :src="url"/>
        <div class="change">
            <upload-cropper @change="handleChange">
                <span class="text-xs text-white">{{ tipsText }}</span>
            </upload-cropper>
        </div>
    </div>

    <upload-cropper v-if="showType === 'default'" @change="handleChange">
        <div class="upload" :style="{ width: size, height: size }">
            <template v-if="url">
                <img class="rounded-md w-full h-full" :src="url" alt="img" />
                <div v-if="closeButton" class="close" @click.stop="url = ''">
                    <icon name="el-icon-CircleCloseFilled" :size="20" />
                </div>
            </template>
            <template v-else>
                <div class="flex flex-col items-center justify-center h-full">
                    <icon name="el-icon-Plus" :size="20" />
                    <div class="text-info mt-2 text-sm" style="line-height: 1">{{ tipsText }}</div>
                </div>
            </template>
        </div>
    </upload-cropper>
</template>

<script setup lang="ts">
const emits = defineEmits(['update:modelValue', 'change'])

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    // 显示类型: [avatar, default]
    showType: {
        type: String,
        default: 'avatar'
    },
    // 上传文本提示
    tipsText: {
        type: String,
        default: '修改'
    },
    // 显示关闭按钮
    closeButton: {
        type: Boolean,
        default: true
    },
    // 上传显示尺寸
    size: {
        type: String,
        default: '90px'
    }
})

const url = ref('')

const handleChange = (event: any) => {
    url.value = event
    emits('update:modelValue', event)
    emits('change', event)
}

watch(
    () => props.modelValue,
    (val) => {
        url.value = val
    },
    { immediate: true }
)
</script>

<style scoped lang="scss">
.avatar {
    position: relative;
    display: flex;
    cursor: pointer;
    .change {
        position: absolute;
        bottom: 0;
        display: none;
        width: 100%;
        height: 50%;
        line-height: 33px;
        text-align: center;
        background-color: #00000080;
        border-bottom-right-radius: 9999px;
        border-bottom-left-radius: 9999px;
    }
    &:hover {
        .change {
            display: block;
        }
    }
}

.upload {
    position: relative;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--el-text-color-secondary);
    border-color: var(--el-border-color);
    border-style: dashed;
    border-width: 1px;
    border-radius: 0.25rem;
    .close {
        position: absolute;
        top: -10px;
        right: -10px;
        opacity: 0;
        transition: all 0.2s linear;
    }
    &:hover {
        .close {
            opacity: 1;
        }
    }
}
</style>
