<template>
    <div v-loading="loading" element-loading-text="上传中...">
        <el-upload
            ref="uploadRef"
            v-model:file-list="fileList"
            v-bind="$attrs"
            class="upload"
            :class="fileList.length >= limit ? 'upload-hide': ''"
            :limit="limit"
            :multiple="multiple"
            :show-file-list="showFileList"
            :on-progress="handleProgress"
            :on-success="handleSuccess"
            :on-exceed="handleExceed"
            :on-error="handleError"
            :accept="getAccept"
            :on-remove="handleRemove"
            :http-request="httpRequest"
            :before-upload="handelBeforeUpload"
            :on-preview="handlePictureCardPreview"
        >
            <slot name="default">
                <div class="flex flex-col items-center justify-center">
                    <icon name="el-icon-Plus" :size="20" />
                    <div class="text-info mt-1 text-sm">{{ tipsText }}</div>
                </div>
            </slot>
            <slot name="trigger"></slot>
            <slot name="tip"></slot>
            <slot name="file"></slot>
        </el-upload>

        <el-dialog
            v-if="!showFileList && fileList.length"
            v-model="visible"
            title="上传进度"
            :close-on-click-modal="false"
            width="500px"
            :modal="false"
            @close="handleClose"
        >
            <div class="file-list p-4">
                <template v-for="(item, index) in fileList" :key="index">
                    <div class="mb-5">
                        <div>{{ item.name }}</div>
                        <div class="flex-1">
                            <el-progress :percentage="parseInt(String(item.percentage))" />
                        </div>
                    </div>
                </template>
            </div>
        </el-dialog>

        <el-dialog v-model="dialogVisible" width="50vw">
            <img :src="dialogImageUrl" class="w-full" alt="Preview Image" />
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import type { ElUpload, UploadRequestOptions, UploadUserFile, UploadRawFile } from 'element-plus'
import type { PropType } from 'vue'
import appApi from '~/api/app/index'

const emits = defineEmits(['end', 'start', 'change', 'error', 'success', 'update:modelValue', 'update:files'])
const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    files: {
        type: Array as PropType<UploadUserFile[]>,
        default: () => []
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
    // 是否支持多选
    multiple: {
        type: Boolean,
        default: true
    },
    // 最多可选几条
    limit: {
        type: Number,
        default: 10
    },
    // 上传额外参数
    data: {
        type: Object,
        default: () => ({})
    },
    // 上传的字段名
    name: {
        type: String,
        default: 'file'
    },
    // 上传的请求头
    header: {
        type: Object,
        default: () => ({})
    },
    // 是否显示进度
    showFileList: {
        type: Boolean,
        default: true
    }
})

// 预览数据
const dialogVisible = ref<boolean>(false)
const dialogImageUrl = ref<string>('')

// 上传状态
const visible = ref(false)
const loading = ref(false)
const fileList = ref<UploadUserFile[]>([])
const uploadRefs = shallowRef<InstanceType<typeof ElUpload>>()

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

const handleProgress = () => {
    visible.value = true
}

const handleChange = (file: any) => {
    emits('change', file)
    if (fileList.value.length === 0) {
        loading.value = false
        emits('end')
    }
}

const handleSuccess = (response: any, file: any) => {
    emits('success', response)
    emits('update:modelValue', response.url)
    emits('update:files', [
        ...props.files,
        {
            url: response.url,
            name: response.name
        }
    ])
    const fileIndex = fileList.value.indexOf(file)
    if (!props.showFileList) {
        fileList.value.splice(fileIndex, 1)
    }
    handleChange(file)
}

const handleRemove = (file: any) => {
    const fileIndex = fileList.value.indexOf(file)
    const newFiles = props.files
    newFiles.splice(fileIndex, 1)
    emits('update:files', [...newFiles])
}

const handleError = (event: any, file: any) => {
    feedback.msgError(`${file.name}文件上传失败`)
    uploadRefs.value?.abort(file)
    visible.value = false
    emits('error', file)
    handleChange(file)
}

const handleExceed = () => {
    feedback.msgError(`超出上传上限${props.limit}，请重新上传`)
}

const handleClose = () => {
    fileList.value = []
    visible.value = false
}

const httpRequest = (options: UploadRequestOptions) => {
    return appApi.upload({
        file: options.file,
        name: props.name,
        data: props.data
    })
}

const handelBeforeUpload = (rawFile: UploadRawFile) => {
    loading.value = true
    emits('start', rawFile)
}

const handlePictureCardPreview = (uploadFile: any) => {
    dialogImageUrl.value = uploadFile.url!
    dialogVisible.value = true
}

watch(
    () => props.files,
    (value) => {
        if (!fileList.value.length && value?.length) {
            fileList.value = [...value]
        }
    },
    {
        immediate: true
    }
)
</script>

<style scoped lang="scss">
.upload {
    display: flex;
    :deep(.el-upload-list--picture-card)  {
        --el-upload-list-picture-card-size: 100px;
        .el-upload-list__item {
            margin-bottom: 2px;
        }
        .el-upload-list__item .el-icon--close-tip {
            visibility: hidden;
        }
    }
    :deep(.el-upload) {
        &.el-upload--picture-card {
            --el-upload-picture-card-size: 100px;
            margin: 0 8px 2px 0;
        }
    }
}

.upload-hide {
    :deep(.el-upload--picture-card) {
      display: none;
    }
}
</style>
