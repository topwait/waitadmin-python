<template>
    <div>
        <!-- 表格栏 -->
        <el-card class="!border-none" shadow="never">
            <el-table :data="dataLists" size="large" class="mt-4">
                <el-table-column label="支付方式" prop="logo" min-width="135">
                    <template #default="{ row }">
                        <el-image :src="row.logo" class="w-[100px] h-[23px]" />
                    </template>
                </el-table-column>
                <el-table-column label="显示图标" prop="icon" min-width="80">
                    <template #default="{ row }">
                        <el-image :src="row.icon" class="w-[28px] h-[26px]" />
                    </template>
                </el-table-column>
                <el-table-column label="显示名称" prop="shorter" min-width="110" />
                <el-table-column label="排序" prop="sort" min-width="80" />
                <el-table-column label="状态" prop="status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.status === 1">启用</el-tag>
                        <el-tag v-else type="danger">停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="70" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['setting:payment:save']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            设置
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <!-- 编辑器 -->
        <editor v-if="showEdit" ref="editorRef" @success="queryPaymentLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import paymentApi from '@/api/setting/payment'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()
const dataLists = ref<Array<any>>([])

/**
 * 查询支付配置列表
 */
const queryPaymentLists = async (): Promise<void> => {
    dataLists.value = await paymentApi.lists()
}

/**
 * 处理支付配置编辑
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

onMounted(async () => {
    await queryPaymentLists()
})
</script>
