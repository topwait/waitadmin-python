<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="登录账号">
                    <el-input
                        v-model="queryParams.username"
                        class="w-[250px]"
                        placeholder="请输入登录账号"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="手机号码">
                    <el-input
                        v-model="queryParams.mobile"
                        class="w-[250px]"
                        placeholder="请输入手机号码"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="所属角色">
                    <el-select
                        v-model="queryParams.role"
                        class="w-[250px]"
                        placeholder="请选择"
                    >
                        <el-option value="" label="全部"/>
                        <el-option
                            v-for="(item, index) in optionsData.role"
                            :key="index"
                            :label="item.name"
                            :value="item.id"
                        />
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
            <el-button type="primary" v-perms="['auth:admin:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-Plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="ID" prop="id" min-width="60" />
                <el-table-column label="头像" min-width="100">
                    <template #default="{ row }">
                        <el-avatar :size="50" :src="row.avatar"/>
                    </template>
                </el-table-column>
                <el-table-column label="用户昵称" prop="nickname" min-width="100" />
                <el-table-column label="登录账号" prop="username" min-width="100" />
                <el-table-column label="所属角色" prop="role" min-width="100" show-tooltip-when-overflow />
                <el-table-column label="所属部门" prop="dept" min-width="100" show-tooltip-when-overflow />
                <el-table-column label="状态" prop="is_disable" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_disable === 0">正常</el-tag>
                        <el-tag v-else type="danger">停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="联系电话" prop="mobile" min-width="100" />
                <el-table-column label="最近登录IP" prop="last_login_ip" min-width="180" />
                <el-table-column label="最近登录时间" prop="last_login_time" min-width="180" />
                <el-table-column label="创建时间" prop="create_time" min-width="180" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-if="row.id !== 1"
                            v-perms="['auth:admin:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-if="row.id !== 1"
                            v-perms="['auth:admin:delete']"
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
import { useDictOptions } from '@/hooks/useOption'
import feedback from '@/utils/feedback'
import authRoleApi from '@/api/auth/role'
import authAdminApi from '@/api/auth/admin'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()

// 查询参数
const queryParams = reactive({
    username: '',
    mobile: '',
    role: ''
})

// 分页查询
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: authAdminApi.lists,
    params: queryParams
})

// 字典选项
const { optionsData } = useDictOptions<{
    role: any[]
}>({
    role: {
        api: authRoleApi.whole
    }
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
            await authAdminApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
})
</script>
