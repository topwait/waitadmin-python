<template>
    <!-- 选择显示 -->
    <div v-if="!uploadHidden" class="material-select">
        <draggable class="draggable" v-model="urlsList" animation="300" item-key="id">
            <template v-slot:item="{ element, index }">
                <div
                    @click="showPopup(index)"
                    class="material-preview"
                    :class="{
                        'is-disabled': disabled,
                        'is-one': limit === 1
                    }"
                >
                    <hover-close @close="handleDelete(index)">
                        <file-item :url="element" :size="size" :type="type" />
                    </hover-close>

                    <div class="operation">
                        <span>修改</span>
                        |
                        <span @click.stop="handlePreview(element)">查看</span>
                    </div>
                </div>
            </template>
        </draggable>
        <div
            v-show="showUpload"
            @click="showPopup(-1)"
            class="material-upload"
            :class="{
                'is-disabled': disabled,
                'is-one': limit == 1,
                [uploadClass]: true
            }"
        >
            <slot name="upload">
                <div
                    class="upload-btn"
                    :style="{
                        width: size,
                        height: size
                    }"
                >
                    <icon :size="25" name="el-icon-plus" />
                    <span>{{ tipsBtn }}</span>
                </div>
            </slot>
        </div>
    </div>

    <!-- 选择弹窗 -->
    <popup
        :show="fileShow"
        :title="'选择' + tipsText"
        :footerBorder="true"
        width="860px"
        @close="handleClose"
        @confirm="handleConfirm"
    >
        <el-scrollbar>
            <div class="material-wrap">
                <material
                    ref="materialRef"
                    size="120px"
                    :type="type"
                    :limit="limit"
                    :filterParams="filterParams"
                    @change="handleChange"
                />
            </div>
        </el-scrollbar>
    </popup>

    <!-- 预览素材 -->
    <preview v-model="previewShow" :url="previewUrls" :type="type" />
</template>

<script lang="ts">
import { useThrottleFn } from '@vueuse/core'
import Draggable from 'vuedraggable'
import FileItem from './file.vue'
import Material from './index.vue'
import Preview from './preview.vue'

export default defineComponent({
    components: {
        Draggable,
        FileItem,
        Material,
        Preview
    },
    props: {
        // 默认初始内容
        modelValue: {
            type: [String, Array],
            default: () => []
        },
        // 文件显示类型
        type: {
            type: String,
            default: 'image'
        },
        // 选择器的尺寸
        size: {
            type: String,
            default: '100px'
        },
        // 选择数量限制
        limit: {
            type: Number,
            default: 1
        },
        // 禁用选择状态
        disabled: {
            type: Boolean,
            default: false
        },
        // 筛选条件参数
        filterParams: {
            type: Object,
            default: () => ({})
        },
        // 上传的类样式
        uploadClass: {
            type: String,
            default: ''
        },
        // 隐藏上传框 (富文本用到)
        uploadHidden: {
            type: Boolean,
            default: false
        },
        // 提示文本
        tipsBtn: {
            type: String,
            default: '添加'
        }
    },
    emits: ['change', 'update:modelValue'],
    setup(props, { emit }) {
        const { disabled, limit, modelValue } = toRefs(props)
        const materialRef = ref<InstanceType<typeof Material>>()

        // 素材预览
        const previewUrls = ref<string>('')
        const previewShow = ref<boolean>(false)

        // 素材文件
        const urlsList = ref<any[]>([])
        const fileList = ref<any[]>([])
        const fileShow = ref<boolean>(false)

        // 素材选择
        const selected = ref<any[]>([])
        const curIndex = ref(-1)

        // 显示上传
        const showUpload = computed(() => {
            return props.limit - urlsList.value.length > 0
        })

        // 提示文字
        const tipsText = computed(() => {
            switch (props.type) {
                case 'image':
                    return '图片'
                case 'video':
                    return '视频'
                case 'audio':
                    return '音频'
                case 'package':
                    return '压缩'
                case 'document':
                    return '文档'
                default:
                    return ''
            }
        })

        /**
         * 打开弹窗
         */
        const showPopup = (index: number) => {
            if (disabled.value) {
                return
            }
            curIndex.value = index
            fileShow.value = true
        }

        /**
         * 关闭弹窗
         */
        const handleClose = () => {
            nextTick(() => {
                if (props.uploadHidden) {
                    fileList.value = []
                }
                fileShow.value = false
                materialRef.value?.selectClear()
            })
        }

        /**
         * 选择变动
         */
        const handleChange = (val: any[]) => {
            selected.value = val
        }

        /**
         * 选择删除
         */
        const handleDelete = (index: number) => {
            urlsList.value.splice(index, 1)
            fileList.value.splice(index, 1)

            const valueImg = limit.value !== 1 ? urlsList.value : urlsList.value[0] || ''
            emit('update:modelValue', valueImg)
            emit('change', fileList.value)
            handleClose()
        }

        /**
         * 确认选择
         */
        const handleConfirm = useThrottleFn(
            () => {
                const urls = selected.value.map((item) => {
                    return item.url
                })

                fileList.value = selected.value.map((item) => {
                    return {
                        name: item.name,
                        size: item.size,
                        path: item.path,
                        url: item.url,
                        ext: item.ext
                    }
                })

                if (curIndex.value >= 0) {
                    fileList.value.splice(curIndex.value, 1, urls.shift())
                } else {
                    urlsList.value = [...urlsList.value, ...urls]
                }

                const valueImg = limit.value !== 1 ? urls : urls[0] || ''
                emit('update:modelValue', valueImg)
                emit('change', fileList.value)
                handleClose()
            },
            1000,
            false
        )

        /**
         * 预览素材
         */
        const handlePreview = (url: string) => {
            previewUrls.value = url
            previewShow.value = true
        }

        watch(
            modelValue,
            (val: any[] | string) => {
                urlsList.value = Array.isArray(val) ? val : val === '' ? [] : [val]
            },
            {
                immediate: true
            }
        )

        return {
            materialRef,
            showUpload,
            tipsText,
            urlsList,
            fileList,
            fileShow,
            previewUrls,
            previewShow,
            showPopup,
            handleClose,
            handleChange,
            handleDelete,
            handleConfirm,
            handlePreview
        }
    }
})
</script>

<style scoped lang="scss">
.material-select {
    display: flex;
    align-items: center;
    :deep(.draggable) {
        display: flex;
        align-items: center;
    }
    .material-upload,
    .material-preview {
        position: relative;
        box-sizing: border-box;
        display: flex;
        margin-right: 8px;
        margin-bottom: 8px;
        cursor: pointer;
        border-radius: 4px;
        .operation {
            position: absolute;
            bottom: 0;
            display: none;
            width: 100%;
            font-size: 12px;
            line-height: 2;
            color: #ffffff;
            text-align: center;
            background-color: rgb(0 0 0 / 30%);
            border-radius: 4px;
        }
        &.is-disabled {
            cursor: not-allowed;
        }
        &.is-one {
            margin-bottom: 0;
        }
        &:hover .operation {
            display: block;
        }
    }
    .material-upload {
        :deep(.upload-btn) {
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--el-text-color-secondary);
            border-color: var(--el-border-color);
            border-style: dashed;
            border-width: 1px;
            border-radius: .25rem;
        }
    }
}

.material-wrap {
    min-width: 720px;
    height: 600px;
}
</style>
