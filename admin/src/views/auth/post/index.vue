<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="岗位编号" prop="username">
                    <el-input
                        v-model="queryParams.code"
                        class="w-[250px]"
                        placeholder="请输入岗位编号"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="岗位名称">
                    <el-input
                        v-model="queryParams.name"
                        class="w-[250px]"
                        placeholder="请输入岗位名称"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="岗位状态">
                    <el-select v-model="queryParams.status" class="w-[250px]">
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
            <el-button type="primary" v-perms="['auth:post:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-Plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="ID" prop="id" min-width="60" />
                <el-table-column label="岗位编号" prop="code" min-width="100" />
                <el-table-column label="岗位名称" prop="name" min-width="100" />
                <el-table-column label="岗位备注" prop="remarks" min-width="150" show-tooltip-when-overflow />
                <el-table-column label="排序" prop="sort" min-width="100" />
                <el-table-column label="状态" prop="is_disable" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_disable === 0">正常</el-tag>
                        <el-tag v-else type="danger">禁用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time" min-width="170" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['auth:post:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-perms="['auth:post:delete']"
                            type="danger"
                            link
                            @click="handleDelete(row.id)"
                        >
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="flex justify-end mt-4">
                <paging v-model="pager" @change="queryLists" />
            </div>
        </el-card>

        <!-- 编辑器 -->
        <editor v-if="showEdit" ref="editorRef" @success="queryLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import { usePaging } from '@/hooks/usePaging'
import feedback from '@/utils/feedback'
import authPostApi from '@/api/auth/post'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()

// 查询参数
const queryParams = reactive({
    code: '',
    name: '',
    status: ''
})

// 分页参数
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: authPostApi.lists,
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
            await authPostApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
})
</script>
