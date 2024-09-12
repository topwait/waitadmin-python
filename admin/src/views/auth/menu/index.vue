<template>
    <div>
        <!-- 表格栏 -->
        <el-card v-loading="pager.loading" class="!border-none" shadow="never">
            <div>
                <el-button type="primary" v-perms="['auth:menu:add']" @click="handleEditor('add')">
                    <template #icon>
                        <icon name="el-icon-Plus" />
                    </template>
                    <span>新增</span>
                </el-button>
                <el-button @click="handleExpand"> 展开/折叠 </el-button>
            </div>

            <el-table
                ref="tableRef"
                v-loading="pager.loading"
                class="mt-4"
                size="large"
                row-key="id"
                :data="pager.lists"
                :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
            >
                <el-table-column label="菜单名称" prop="name" min-width="150" />
                <el-table-column label="类型" prop="type" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.type === 'M'" type="primary">目录</el-tag>
                        <el-tag v-if="row.type === 'C'" type="success">菜单</el-tag>
                        <el-tag v-if="row.type === 'A'" type="info">按钮</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="图标" prop="icon" min-width="80">
                    <template #default="{ row }">
                        <div v-if="row.icon" class="flex">
                            <icon :name="row.icon" :size="20" />
                        </div>
                    </template>
                </el-table-column>
                <el-table-column
                    label="权限标识"
                    prop="perms"
                    min-width="150"
                    show-overflow-tooltip
                />
                <el-table-column label="路径" prop="path" min-width="120">
                    <template #default="{ row }">
                        <span v-if="row.type === 'M' && row.path">{{ row.path }}</span>
                        <span v-if="row.type === 'C' && row.path">{{ row.path }}</span>
                        <span v-if="row.type === 'A' && row.path" class="text-danger">{{ row.path }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="状态" prop="is_disable" min-width="100">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_disable == 0">正常</el-tag>
                        <el-tag v-else type="danger">停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="排序" prop="sort" min-width="100" />
                <el-table-column label="更新时间" prop="update_time" min-width="180" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['auth:menu:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-perms="['auth:menu:delete']"
                            type="danger"
                            link
                            @click="handleDelete(row.id)"
                        >
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <!-- 编辑器 -->
        <editor v-if="showEdit" ref="editorRef" @success="queryLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import type { ElTable } from 'element-plus'
import { usePaging } from '@/hooks/usePaging'
import feedback from '@/utils/feedback'
import authMenuApi from '@/api/auth/menu'
import Editor from './editor.vue'

let isExpand: boolean = false

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()
const tableRef = shallowRef<InstanceType<typeof ElTable>>()

// 查询菜单
const { pager, queryLists } = usePaging({
    fetchFun: authMenuApi.lists
})

/**
 * 处理编辑
 *
 * @param {string} type
 * @param {any} row
 * @returns {Promise<void>}
 */
const handleEditor = async (type: string, row?: any): Promise<void> => {
    showEdit.value = true
    await nextTick()
    editorRef.value?.open(type, row)
}

/**
 * 处理删除
 *
 * @param {number} id
 * @returns {Promise<void>}
 */
const handleDelete = async (id: number): Promise<void> => {
    feedback.confirm('确定要删除此项数据吗?')
        .then(async () => {
            await authMenuApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

/**
 * 处理展开
 *
 * @returns {void}
 * @author zero
 */
const handleExpand = (): void => {
    isExpand = !isExpand
    _toggleExpand(pager.lists, isExpand)
}

/**
 * 展开逻辑
 *
 * @param {any[]} children
 * @param {boolean} unfold
 * @returns {void}
 */
const _toggleExpand = (children: any[], unfold: boolean = true): void => {
    for (const key in children) {
        tableRef.value?.toggleRowExpansion(children[key], unfold)
        if (children[key].children) {
            _toggleExpand(children[key].children!, unfold)
        }
    }
}

onMounted(async () => {
    await queryLists()
})
</script>
