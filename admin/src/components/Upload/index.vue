<template>
    <div class="upload">
        <el-upload
            v-model:file-list="fileList"
            ref="uploadRefs"
            v-bind="$attrs"
            :multiple="multiple"
            :limit="limit"
            :show-file-list="showFileList"
            :on-progress="handleProgress"
            :on-success="handleSuccess"
            :on-exceed="handleExceed"
            :on-error="handleError"
            :accept="getAccept"
            :on-change="handleChange"
            :on-remove="handleRemove"
            :http-request="httpRequest"
        >
            <template v-for="(_slot, key) in $slots" #[key]="slotData">
                <slot :name="key" v-bind="slotData"></slot>
            </template>
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
                <template v-for="(item, _index) in fileList" :key="_index">
                    <div class="mb-5">
                        <div>{{ item.name }}</div>
                        <div class="flex-1">
                            <el-progress :percentage="parseInt(String(item.percentage))" />
                        </div>
                    </div>
                </template>
            </div>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import type { PropType } from 'vue'
import type { ElUpload, UploadRequestOptions, UploadUserFile } from 'element-plus'
import feedback from '@/utils/feedback'
import appApi from '@/api/app'

const props = defineProps({
    files: {
        type: Array as PropType<UploadUserFile[]>,
        default: () => []
    },
    // 上传文件类型
    type: {
        type: String,
        default: 'image'
    },
    // 是否支持多选
    multiple: {
        type: Boolean,
        default: true
    },
    // 多选时最多选择几条
    limit: {
        type: Number,
        default: 10
    },
    // 上传时的额外参数
    data: {
        type: Object,
        default: () => ({})
    },
    // 上传文件的字段名
    name: {
        type: String,
        default: 'file'
    },
    // 上传请求头额外参数
    header: {
        type: Object,
        default: () => ({})
    },
    // 是否显示列表进度条
    showFileList: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['end', 'change', 'error', 'success', 'update:files'])
const uploadRefs = shallowRef<InstanceType<typeof ElUpload>>()

const visible = ref(false)
const fileList = ref<UploadUserFile[]>([])

const handleProgress = () => {
    visible.value = true
}

const handleChange = (file: any) => {
    emit('change', file)
    if (fileList.value.length === 0) {
        emit('end')
    }
}

const handleSuccess = (response: any, file: any) => {
    handleChange(file)
    emit('success', response)
    emit('update:files', [
        ...props.files,
        {
            url: response.uri,
            name: response.name
        }
    ])
    const fileIndex = fileList.value.indexOf(file)
    !props.showFileList && fileList.value.splice(fileIndex, 1)
}

const handleRemove = (file: any) => {
    const fileIndex = fileList.value.indexOf(file)
    const newFiles = props.files
    newFiles.splice(fileIndex, 1)
    emit('update:files', [...newFiles])
}

const handleError = (_event: any, file: any) => {
    handleChange(file)
    feedback.msgError(`${file.name}文件上传失败`)
    uploadRefs.value?.abort(file)
    visible.value = false
    emit('error', file)
}

const handleExceed = () => {
    feedback.msgError(`超出上传上限${props.limit},请重新上传`)
}

const handleClose = () => {
    fileList.value = []
    visible.value = false
}

const getAccept = computed(() => {
    switch (props.type) {
        case 'image':
            return '.jpg,.jpeg,.png,.gif,.bmp,.svg,.webp,.ico'
        case 'video':
            return '.wmv,.avi,.mpg,.mpeg,.3gp,.mov,.mp4,.m4v,.flv,.rmvb,.mkv'
        case 'audio':
            return '.mp3,.wav,.aac,.ogg,.flac,.m4a,.amr,.wma,.mid,.midi,.ape,.ac3'
        case 'packs':
            return '.zip,.rar,.7z,.tar,.gz,.bz2,.tgz,.tar.gz,.tbz2,.tar.bz2,.iso,.cab'
        case 'docs':
            return '.doc,.docx,.xls,.xlsx,.ppt,.pptx,.pdf,.txt,.html,.htm,.csv,.md,.pem'
        default:
            return '*'
    }
})

const httpRequest = (options: UploadRequestOptions) => {
    return appApi.upload(
        {
            file: options.file,
            name: props.name,
            header: props.header,
            data: {scene: props.type, ...props.data}
        },
        (evt: any) => {
            const progressEvt = evt
            progressEvt.percent = evt.total > 0 ? evt.loaded / evt.total * 100 : 0
            options.onProgress(progressEvt)
        }
    )
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
