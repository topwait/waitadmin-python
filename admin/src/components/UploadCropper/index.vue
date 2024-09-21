<template>
    <div>
        <el-upload
            class="flex flex-col"
            ref="uploadRef"
            :limit="1"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleChange"
            accept=".jpg,.png,.gif,.jpeg"
        >
            <slot></slot>
        </el-upload>
        <el-dialog
            v-model="state.cropperVisible"
            :append-to-body="true"
            :close-on-click-modal="false"
            :width="600"
            @close="state.cropperVisible = false"
        >
            <div class="h-[400px]">
                <VueCropper
                    ref="vueCropperRef"
                    :img="state.imagePath"
                    :auto-crop="true"
                    :auto-crop-height="200"
                    :auto-crop-width="200"
                    output-type="png"
                />
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleConfirmCropper">
                        确认裁剪
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import 'vue-cropper/dist/index.css'
import { ElUpload, ElDialog, ElButton } from 'element-plus'
import { VueCropper } from 'vue-cropper'
import appApi from '@/api/app'

const emits = defineEmits(['change'])

const vueCropperRef = shallowRef()
const uploadRef = shallowRef<InstanceType<typeof ElUpload>>()

const state = reactive({
    cropperVisible: false,
    imagePath: ''
})

const handleChange = (rawFile: any) => {
    const URL = window.URL || window.webkitURL
    state.imagePath = URL.createObjectURL(rawFile.raw)
    state.cropperVisible = true
}

const handleConfirmCropper = () => {
    vueCropperRef.value?.getCropBlob(async (file: any) => {
        const fileName = `file.${file.type.split('/')[1]}`
        const imgFile = new window.File([file], fileName, {
            type: file.type
        })

        const data = await appApi.upload({
            file: imgFile,
            data: {
                scene: 'image',
                is_attach: 0
            }
        }, null)

        state.cropperVisible = false
        emits('change', data.url)
        uploadRef.value?.clearFiles()
    })
}
</script>

<style scoped lang="scss">
:deep(.el-upload__input) {
    display: none;
}
</style>
