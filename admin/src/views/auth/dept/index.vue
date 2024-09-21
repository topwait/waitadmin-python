<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="部门名称" prop="name">
                    <el-input
                        v-model="queryParams.name"
                        class="w-[250px]"
                        placeholder="请输入部门名称"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="部门电话">
                    <el-input
                        v-model="queryParams.mobile"
                        class="w-[250px]"
                        placeholder="请输入部门电话"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="部门状态">
                    <el-select v-model="queryParams.is_disable" class="w-[250px]">
                        <el-option value="" label="全部" />
                        <el-option value="0" label="正常" />
                        <el-option value="1" label="禁用" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="resetPaging">查询</el-button>
                    <el-button @click="resetParams">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 表格栏 -->
        <el-card v-loading="pager.loading" class="!border-none" shadow="never">
            <el-button type="primary" v-perms="['auth:dept:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-Plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-button @click="handleExpand"> 展开/折叠 </el-button>
            <el-table
                v-loading="pager.loading"
                :data="pager.lists"
                size="large"
                class="mt-4"
                row-key="id"
                :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
            >
                <el-table-column label="部门名称" prop="name" min-width="150" show-overflow-tooltip />
                <el-table-column label="部门电话" prop="mobile" min-width="120" />
                <el-table-column label="负责人" prop="duty" min-width="100" show-tooltip-when-overflow />
                <el-table-column label="排序" prop="sort" min-width="80" />
                <el-table-column label="状态" prop="is_disable" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_disable === 0">正常</el-tag>
                        <el-tag v-else type="danger">禁用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time" min-width="175" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['auth:dept:edit']"
                            type="primary" 
                            link 
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button 
                            v-perms="['auth:dept:delete']"
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
import authDeptApi from '@/api/auth/dept'
import Editor from './editor.vue'

let isExpand = false
const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()
const tableRef = shallowRef<InstanceType<typeof ElTable>>()

// 查询参数
const queryParams = reactive({
    name: '',
    mobile: '',
    is_disable: ''
})

// 分页参数
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: authDeptApi.lists,
    params: queryParams
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
            await authDeptApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

/**
 * 处理展开
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
