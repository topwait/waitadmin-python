<template>
    <div class="material">
        <!-- 左侧 -->
        <div class="material__left">
            <el-scrollbar>
                <el-tree
                    ref="treeRef"
                    node-key="id"
                    empty-text=""
                    :class="mode"
                    :data="cateLists"
                    :highlight-current="true"
                    :expand-on-click-node="false"
                    :current-node-key="cateId"
                    @node-click="handleSwitchCate"
                >
                    <template v-slot="{ data }">
                        <div class="group-item">
                            <img class="icon" src="@/assets/images/icon_folder.png" alt="icon"/>
                            <span class="name">{{ data.name }}</span>
                            <el-dropdown v-if="data.id > 0" :hide-on-click="false">
                                <span class="more">···</span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <popover-input
                                            @confirm="handleRenameCate($event, data.id)"
                                            size="default"
                                            width="400px"
                                            :value="data.name"
                                            :limit="20"
                                            show-limit
                                            teleported
                                        >
                                            <el-dropdown-item>命名分组</el-dropdown-item>
                                        </popover-input>
                                        <el-dropdown-item @click="handleDeleteCate(data.id)">删除分组</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </div>
                    </template>
                </el-tree>
            </el-scrollbar>
            <div class="grouping">
                <popover-input
                    @confirm="handleAddCate"
                    size="default"
                    width="400px"
                    :limit="20"
                    show-limit
                    teleported
                >
                    <el-button>添加分组</el-button>
                </popover-input>
            </div>
        </div>
        <!-- 中间 -->
        <div class="material__center">
            <div class="material-center__header">
                <div class="flex">
                    <upload
                        class="mr-3"
                        :data="{ cid: cateId, ...data }"
                        :type="type"
                        :show-file-list="false"
                        @end="resetPaging"
                    >
                        <el-button type="primary">本地上传</el-button>
                    </upload>
                    <el-button :disabled="!select.length" @click="handleDeleteFile()">删除</el-button>
                    <el-button :disabled="!select.length" @click="movePo = true">移动</el-button>
                    <el-dialog
                        v-model="movePo"
                        title="移动文件"
                        width="400px"
                        :center="false"
                        :append-to-body="true"
                        :destroy-on-close="false"
                        :close-on-click-modal="false"
                    >
                        <div class="flex items-center">
                            <span class="mr-3 w-[100px]">移动文件至</span>
                            <el-select v-model="moveId" placeholder="请选择">
                                <template v-for="item in cateLists" :key="item.id">
                                    <el-option
                                        v-if="item.id !== ''"
                                        :label="item.name"
                                        :value="item.id"
                                    />
                                </template>
                            </el-select>
                        </div>
                        <template #footer>
                            <div class="dialog-footer">
                                <el-button @click="movePo = false">取消</el-button>
                                <el-button type="primary" @click="handleMoveFile()">确定</el-button>
                            </div>
                        </template>
                    </el-dialog>
                </div>
                <div>
                    <el-input
                        class="w-60"
                        placeholder="请输入名称"
                        v-model="searchParams.keyword"
                        @keyup.enter="resetPaging"
                    >
                        <template #append>
                            <el-button @click="resetPaging">
                                <template #icon>
                                    <icon name="el-icon-search" />
                                </template>
                            </el-button>
                        </template>
                    </el-input>
                </div>
            </div>
            <div class="material-center__content">
                <el-scrollbar>
                    <ul>
                        <li v-for="(item, index) in pager.lists" :key="index">
                            <hover-close @close="handleDeleteFile(item.id)">
                                <file-item
                                    :url="item.url"
                                    :type="type"
                                    :size="size"
                                    @click="selectFile(item)"
                                >
                                    <div v-if="isSelect(item.id)" class="selected">
                                        <icon :size="24" name="el-icon-Check" color="#fff" />
                                    </div>
                                </file-item>
                            </hover-close>
                            <div class="title">
                                <el-tooltip placement="top" :content="item.name">
                                    {{ item.name }}
                                </el-tooltip>
                            </div>
                            <div class="operate">
                                <el-button
                                    type="primary"
                                    link
                                    @click="handleRenameFile(item.id, item.name)">重命名</el-button>
                                <el-button
                                    v-if="['packs', 'docs'].includes(type)"
                                    type="primary"
                                    link
                                    @click="handlePreview(item.url, item.name)">下载</el-button>
                                <el-button
                                    v-else
                                    type="primary"
                                    link
                                    @click="handlePreview(item.url, item.name)">查看</el-button>
                            </div>
                        </li>
                    </ul>
                </el-scrollbar>
            </div>
            <div class="material-center__footer">
                <paging
                    v-model="pager"
                    size="small"
                    layout="total, prev, pager, next, jumper"
                />
            </div>
        </div>
        <!-- 右侧 -->
        <div v-if="mode === 'picker'" class="material__right">
            <div class="flex justify-between p-2">
                <div>
                    <span>已选择</span>
                    <span>/{{ limit }}</span>
                </div>
                <el-button type="primary" link>清空</el-button>
            </div>
            <div class="flex-1 min-h-0">
                <el-scrollbar>
                    <ul class="flex flex-col p-t-3">
                        <li v-for="item in select" :key="item.id">
                            <hover-close @close="selectCancel(item.id)">
                                <file-item
                                    size="100px"
                                    :type="type"
                                    :url="item.url"
                                />
                            </hover-close>
                        </li>
                    </ul>
                </el-scrollbar>
            </div>
        </div>
        <!-- 预览 -->
        <preview v-model="showPreview" :url="previewUrl" :type="type" />
    </div>
</template>

<script setup lang="ts">
import { ElTree } from 'element-plus'
import { useCate, useFile } from './hook'
import Preview from './preview.vue'
import FileItem from './file.vue'

const emits = defineEmits(['change'])
const props = defineProps({
    // 页面模式
    mode: {
        type: String,
        default: 'picker'
    },
    // 文件类型
    type: {
        type: String,
        default: 'image'
    },
    // 文件大小
    size: {
        type: String,
        default: '120px'
    },
    // 限制选择
    limit: {
        type: Number,
        default: 1
    },
    // 每页数量
    pageSize: {
        type: Number,
        default: 15
    },
    // 上传参数
    data: {
        type: Object,
        default: () => ({})
    }
})

const { pageSize, limit, data } = toRefs(props)
const typeValue = computed<number>(() => {
    switch (props.type) {
        case 'image':
            return 10
        case 'video':
            return 20
        case 'audio':
            return 30
        case 'packs':
            return 40
        case 'docs':
            return 50
        default:
            return 0
    }
})

const previewUrl = ref('')
const showPreview = ref(false)

const {
    treeRef,
    cateId,
    cateLists,
    getCateLists,
    handleAddCate,
    handleRenameCate,
    handleDeleteCate,
    handleSwitchCate
} = useCate(typeValue.value)

const {
    pager,
    movePo,
    moveId,
    select,
    isSelect,
    selectFile,
    selectClear,
    selectCancel,
    searchParams,
    getFileLists,
    resetPaging,
    handleMoveFile,
    handleRenameFile,
    handleDeleteFile
} = useFile(typeValue.value, cateId, limit, pageSize, data)

const getData = async () => {
    await getCateLists()
    treeRef.value?.setCurrentKey(cateId.value)
    await getFileLists()
}

const handlePreview = (url: string, name: string) => {
    if (['packs', 'docs'].includes(props.type)) {
        const link = document.createElement('a')
        link.href = url
        link.download = name
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    } else {
        previewUrl.value = url
        showPreview.value = true
    }
}

watch(cateId, () => {
    searchParams.name = ''
    resetPaging()
})

watch(
    select,
    (val: any[]) => {
        emits('change', val)
    },
    {
        deep: true
    }
)

onMounted(async () => {
    await getData()
})

defineExpose({
    selectClear
})
</script>

<style scoped lang="scss">
.material {
    display: flex;
    flex: 1 1 0;
    height: 100%;
    min-height: 0;
    background-color: var(--el-bg-color);
    &__left {
        display: flex;
        flex-direction: column;
        width: 190px;
        border-right: 1px solid var(--el-border-color-lighter);
        .group-item {
            display: flex;
            flex: 1 1 0;
            align-items: center;
            min-width: 0;
            padding-right: 10px;
            .icon {
                width: 20px;
                height: 16px;
                margin-right: 10px;
            }
            .more {
                font-size: 12px;
                color: #666666;
            }
            .name {
                flex: 1 1 0;
                margin-right: 8px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
        }
        :deep(.el-tree) {
            padding: 8px 6px 8px 0;
            &.picker {
                padding: 8px 0;
                .el-tree-node__content {
                    border-radius: 0;
                }
            }
            .el-tree-node__content {
                height: 36px;
                border-radius: 4px;
                .el-tree-node__expand-icon.is-leaf {
                    padding: 2px;
                }
                .el-tree-node__label {
                    display: flex;
                    flex: 1;
                    min-width: 0;
                }
            }
        }
        .grouping {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 6px 0;
            border-top: 1px solid var(--el-border-color-lighter);
        }
    }
    &__center {
        display: flex;
        flex: 1;
        flex-direction: column;
        min-width: 0;
        min-height: 0;
        padding-top: 16px;
        .material-center__header {
            display: flex;
            justify-content: space-between;
            padding: 0 12px;
        }
        .material-center__content {
            display: flex;
            flex: 1 1 0;
            flex-direction: column;
            min-height: 0;
            padding: 0 6px;
            ul {
                display: flex;
                flex-wrap: wrap;
                margin-top: 20px;
                li {
                    position: relative;
                    width: 120px;
                    margin: 0 6px ;
                    line-height: 1.3;
                    cursor: pointer;
                    .title {
                        height: 17px;
                        margin: 3px 2px;
                        overflow: hidden;
                        font-size: 12px;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    }
                    .operate {
                        display: flex;
                        align-items: center;
                        height: 12px;
                        margin-bottom: 8px;
                        visibility: hidden;
                        :deep(.el-button) {
                            margin: 0;
                            font-size: 12px;
                            font-weight: normal;
                        }
                    }
                    .selected {
                        position: absolute;
                        top: 0;
                        left: 0;
                        box-sizing: border-box;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 100%;
                        height: 100%;
                        background-color: rgb(0 0 0 / 50%);
                        border-radius: 4px;
                    }
                    &:hover .operate,
                    &:hover .close {
                        visibility: visible;
                    }
                }
            }
        }
        .material-center__footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding: 10px 20px;
            border-top: 1px solid var(--el-border-color-lighter);
        }
    }
    &__right {
        display: flex;
        flex-direction: column;
        width: 125px;
        border-color: var(--el-border-color-lighter);
        border-left-width: 1px;
        ul {
            padding: 10px;
            li {
                position: relative;
                width: 100px;
                height: 100px;
                margin-bottom: 14px;
            }
        }
    }
}
</style>
