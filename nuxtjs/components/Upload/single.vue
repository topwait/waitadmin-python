<template>
    <div>
        <div
            v-if="!replaceUpload && value"
            class="border border-dashed border-br-darker rounded-md"
            @click="handlePreview"
        >
            <div class="preview" :style="{ width: size, height: size }">
                <img class="rounded-md w-full h-full" :src="value" alt="img" />
                <div v-if="closeButton" class="close" @click.stop="value = ''">
                    <icon name="el-icon-CircleCloseFilled" :size="20" />
                </div>
            </div>
        </div>

        <div v-else-if="replaceUpload || !value"  v-loading="loading" element-loading-text="上传中...">
            <el-upload
                ref="uploadRef"
                class="uploader"
                :limit="1"
                :auto-upload="false"
                :show-file-list="false"
                :on-change="handleChange"
                :accept="getAccept"
            >
                <slot>
                    <div :style="{ width: size, height: size }">
                        <div v-if="!value" class="flex flex-col items-center justify-center h-full">
                            <icon name="el-icon-Plus" :size="20" />
                            <div class="text-info mt-1 text-sm">{{ tipsText }}</div>
                        </div>
                        <div v-else class="preview">
                            <img class="rounded-md w-full h-full" :src="value" alt="img" />
                            <div v-if="closeButton" class="close" @click.stop="value = ''">
                                <icon name="el-icon-CircleCloseFilled" :size="20" />
                            </div>
                        </div>
                    </div>
                </slot>
            </el-upload>
        </div>

        <el-dialog v-model="dialogVisible" width="50vw">
            <img :src="dialogImageUrl" class="w-full" alt="Preview Image" />
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import appApi from '~/api/app/index'

const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    // 上传文件类型
    type: {
        type: String,
        default: 'image'
    },
    // 上传文本提示
    tipsText: {
        type: String,
        default: '上传图片'
    },
    // 显示关闭按钮
    closeButton: {
        type: Boolean,
        default: true
    },
    // 允许替换上传
    replaceUpload: {
        type: Boolean,
        default: false
    },
    // 上传显示尺寸
    size: {
        type: String,
        default: '100px'
    }
})

// 预览数据
const dialogVisible = ref<boolean>(false)
const dialogImageUrl = ref<string>('')

// 上传状态
const loading = ref<boolean>(false)
const uploadRef = shallowRef()

// 支持类型
const getAccept = computed(() => {
    switch (props.type) {
        case 'image':
            return '.jpg,.jpeg,.png,.gif,bmp,svg,webp,ico'
        case 'video':
            return '.wmv,.avi,.mpg,.mpeg,.3gp,.mov,.mp4,m4v,.flv,.rmvb,.mkv'
        case 'audio':
            return '.mp3,.wav,.aac,.ogg,.flac,.m4a,.amr,.wma,.mid,.midi,.ape,.ac3'
        case 'package':
            return '.zip,.rar,.7z,.tar,.gz,.bz2,.tgz,.tar.gz,.tbz2,.tar.bz2,.iso,.cab'
        case 'document':
            return '.doc,.docx,.xls,.xlsx,.ppt,.pptx,.pdf,.txt,.rtf,.html,.htm,.csv,.md,.pem'
        default:
            return '*'
    }
})

// 文件路径
const value = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emits('update:modelValue', value)
    }
})

/**
 * 处理上传
 * @param e
 * @author zero
 */
const handleChange = async (e: any) => {
    try {
        loading.value = true
        const data = await appApi.upload({ file: e.raw })
        loading.value = false
        value.value = data.url
        emits('change', data)
        uploadRef.value?.clearFiles()
    } catch {
        loading.value = false
        uploadRef.value?.clearFiles()
    }
}

/**
 * 处理预览
 * @author zero
 */
const handlePreview = () => {
    dialogImageUrl.value = value.value
    dialogVisible.value = true
}
</script>

<style scoped lang="scss">
.uploader {
    display: flex;
    :deep(.el-upload) {
        cursor: pointer;
        background-color: var(--el-fill-color-lighter);
        border: 1px dashed var(--el-border-color-darker);
        border-radius: 6px;
        &:hover {
            border-color: var(--el-color-primary);
        }
    }
}

.preview {
    position: relative;
    width: 100%;
    height: 100%;
    cursor: pointer;
    background-color: var(--el-fill-color-lighter);
    border-radius: 6px;
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
