<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <div class="text-xl font-medium mb-[20px]">充值配置</div>
            <el-form class="mb-[-16px]" label-width="100px">
                <el-form-item label="充值状态">
                    <div>
                        <el-radio-group v-model="formData.status">
                            <el-radio :value="0">开启</el-radio>
                            <el-radio :value="1">关闭</el-radio>
                        </el-radio-group>
                        <div class="form-tips">关闭充值功能后, 用户将无法进行余额充值</div>
                    </div>
                </el-form-item>
                <el-form-item label="最低充值金额">
                    <div>
                        <el-input
                            v-model="formData.min_recharge"
                            class="w-[250px]"
                            placeholder="请输入最新充值金额"
                            clearable
                            @keyup.enter="resetPaging"
                        />
                        <div class="form-tips">最低充值金额要求, 0表示不限制最低充值金额</div>
                    </div>
                </el-form-item>
                <el-form-item>
                    <el-button
                        v-perms="['market:recharge:config']"
                        :loading="loading"
                        type="primary"
                        @click="handleSubmit"
                    >保存配置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 表格栏 -->
        <el-card v-loading="pager.loading" class="!border-none" shadow="never">
            <div class="text-xl font-medium mb-[20px]">充值套餐</div>
            <el-button type="primary" v-perms="['market:recharge:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-Plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="充值金额" prop="money" min-width="100" />
                <el-table-column label="赠送金额" prop="give_money" min-width="100" />
                <el-table-column label="排序" prop="sort" min-width="100" />
                <el-table-column label="状态" prop="is_show" min-width="100">
                    <template #default="{ row }">
                        <span v-if="row.is_show">正常</span>
                        <span v-else>停用</span>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time" min-width="175" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['market:recharge:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-perms="['market:recharge:delete']"
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
import { usePaging } from '@/hooks/usePaging'
import feedback from '@/utils/feedback'
import rechargePackApi from '@/api/market/recharge'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()

const loading = ref(false)
const formData = reactive({
    status: 0,
    min_recharge: 0
})

// 分页查询
const { pager, queryLists, resetPaging } = usePaging({
    fetchFun: rechargePackApi.lists
})

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    loading.value = true
    await rechargePackApi.config(formData)
        .finally(() => {
            setTimeout(() => {
                loading.value = false
            }, 500)
        })

    feedback.msgSuccess('保存成功')
}

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
            await rechargePackApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
    formData.status = pager.extend.status
    formData.min_recharge = pager.extend.min_recharge
})
</script>
