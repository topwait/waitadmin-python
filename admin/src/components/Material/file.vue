<template>
    <div class="file-item" :style="{ height: size, width: size }">
        <!-- 图片 -->
        <el-image
            v-if="type == 'image'"
            class="image"
            fit="contain"
            :src="url"
        />
        <!-- 视频 -->
        <video
            v-else-if="type == 'video'"
            class="video"
            :src="url"
        ></video>
        <!-- 音频 -->
        <el-image
            v-if="type == 'audio'"
            class="image"
            fit="contain"
            :src="iconAudio"
        />
        <!-- 包装 -->
        <el-image
            v-if="type == 'packs'"
            class="image"
            fit="contain"
            :src="packIcons(url)"
        />
        <!-- 文档 -->
        <el-image
            v-if="type == 'docs'"
            class="image"
            fit="contain"
            :src="docsIcons(url)"
        />
        <!-- 插槽 -->
        <slot></slot>
    </div>
</template>

<script setup lang="ts">
import iconAudio from '@/assets/images/material/audio.png'
import icon7z from '@/assets/images/material/7z.png'
import iconGz from '@/assets/images/material/gz.png'
import iconIso from '@/assets/images/material/iso.png'
import iconRar from '@/assets/images/material/rar.png'
import iconTar from '@/assets/images/material/tar.png'
import iconZip from '@/assets/images/material/zip.png'
import iconCsv from '@/assets/images/material/csv.png'
import iconDoc from '@/assets/images/material/doc.png'
import iconDocx from '@/assets/images/material/docx.png'
import iconHtml from '@/assets/images/material/html.png'
import iconMd from '@/assets/images/material/md.png'
import iconPdf from '@/assets/images/material/pdf.png'
import iconPpt from '@/assets/images/material/ppt.png'
import iconPptx from '@/assets/images/material/pptx.png'
import iconTxt from '@/assets/images/material/txt.png'
import iconXls from '@/assets/images/material/xls.png'
import iconXlsx from '@/assets/images/material/xlsx.png'

defineProps({
    // 文件类型
    type: {
        type: String,
        default: 'image'
    },
    // 文件尺寸
    size: {
        type: String,
        default: '120px'
    },
    // 文件地址
    url: {
        type: String,
        default: ''
    }
})

const packIcons = (url: string) => {
    const suffix: string | undefined = url.split('.').pop()
    switch (suffix?.toLowerCase()) {
        case '7z':
            return icon7z
        case 'iso':
            return iconIso
        case 'rar':
            return iconRar
        case 'tar':
            return iconTar
        case 'zip':
            return iconZip
        default:
            return iconGz
    }
}

const docsIcons = (url: string) => {
    const suffix: string | undefined = url.split('.').pop()
    switch (suffix?.toLowerCase()) {
        case 'csv':
            return iconCsv
        case 'doc':
            return iconDoc
        case 'docx':
            return iconDocx
        case 'html':
            return iconHtml
        case 'md':
            return iconMd
        case 'pdf':
            return iconPdf
        case 'ppt':
            return iconPpt
        case 'pptx':
            return iconPptx
        case 'xls':
            return iconXls
        case 'xlsx':
            return iconXlsx
        default:
            return iconTxt
    }
}
</script>

<style scoped lang="scss">
.file-item {
    position: relative;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    overflow: hidden;
    background-color: var(--el-border-color-extra-light);
    border-color: var(--el-border-color-extra-light);
    border-width: 1px;
    border-radius: 4px;
    .image {
        max-width: 100%;
        max-height: 100%;
        vertical-align: middle;
        border-radius: 4px;
    }
}
</style>
