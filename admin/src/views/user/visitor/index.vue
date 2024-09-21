<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="访问方式">
                    <el-select v-model="queryParams.method" class="w-[250px]">
                        <el-option value="" label="全部" />
                        <el-option value="GET" label="GET" />
                        <el-option value="POST" label="POST" />
                        <el-option value="PUT" label="PUT" />
                        <el-option value="DELETE" label="DELETE" />
                        <el-option value="OPTION" label="OPTION" />
                    </el-select>
                </el-form-item>
                <el-form-item label="来源IP">
                    <el-input
                        v-model="queryParams.ip"
                        class="w-[250px]"
                        placeholder="请输入"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="访问链接">
                    <el-input
                        v-model="queryParams.url"
                        class="w-[250px]"
                        placeholder="请输入"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="记录时间">
                    <date-picker
                        v-model:startTime="queryParams.start_time"
                        v-model:endTime="queryParams.end_time"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="resetPaging">查询</el-button>
                    <el-button @click="resetParams">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <!-- 表格栏 -->
        <el-card v-loading="pager.loading" class="!border-none" shadow="never">
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="ID" prop="id" min-width="100" />
                <el-table-column label="操作描述" prop="summary" min-width="120" />
                <el-table-column label="操作成员" prop="admin" min-width="120" />
                <el-table-column label="请求方式" prop="method" min-width="100" />
                <el-table-column label="请求路由" prop="url" min-width="150" />
                <el-table-column label="来源IP" prop="ip" min-width="135" />
                <el-table-column label="耗时(ms)" prop="task_time" min-width="80" />
                <el-table-column label="状态" prop="status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.status === 1">成功</el-tag>
                        <el-tag v-else type="danger">失败</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="记录时间" prop="create_time" min-width="175" />
                <el-table-column label="操作" width="70" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link @click="handleDetail('detail', row)">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="flex justify-end mt-4">
                <paging v-model="pager" @change="queryLists" />
            </div>
        </el-card>

        <!-- 编辑器 -->
        <detail v-if="showEdit" ref="detailRef" @success="queryLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import { usePaging } from '@/hooks/usePaging'
import journalApi from '@/api/system/journal'
import Detail from './detail.vue'

const showEdit = ref(false)
const detailRef = shallowRef<InstanceType<typeof Detail>>()

// 查询参数
const queryParams = reactive({
    method: '',
    url: '',
    ip: '',
    start_time: '',
    end_time: ''
})

// 分页查询
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: journalApi.lists,
    params: queryParams
})

/**
 * 处理编辑
 *
 * @param {string} type
 * @param {any} row
 * @returns {Promise<void>}
 */
const handleDetail = async (type: string, row?: any): Promise<void> => {
    showEdit.value = true
    await nextTick()
    detailRef.value?.open(type, row)
}

onMounted(async () => {
    await queryLists()
})
</script>
