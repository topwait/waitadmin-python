<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="用户信息">
                    <el-input
                        v-model="queryParams.user"
                        class="w-[250px]"
                        placeholder="请输入用户编号/昵称/手机号"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="变动类型">
                    <el-select
                        v-model="queryParams.source_type"
                        class="w-[250px]"
                        placeholder="请选择"
                    >
                        <el-option value="" label="全部"/>
                        <el-option
                            v-for="(value, key) in pager.extend?.types"
                            :key="key"
                            :label="value"
                            :value="key"
                        />
                    </el-select>
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
            <el-table :data="pager.lists" size="large">
                <el-table-column label="用户编号" prop="user.sn" min-width="100" />
                <el-table-column label="用户信息" min-width="120">
                    <template #default="{ row }">
                        <div class="flex items-center">
                            <el-avatar :size="36" :src="row.user.avatar"/>
                            <span class="ml-2">{{ row?.user.nickname }}</span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="变动的金额" prop="change_amount" min-width="100" />
                <el-table-column label="变动类型" prop="action" min-width="100">
                    <template #default="{ row }">
                        <span v-if="row.action === 1">+{{ row?.change_amount }}</span>
                        <span v-else>-{{ row?.change_amount }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="变动前金额" prop="before_amount" min-width="100" />
                <el-table-column label="变动后金额" prop="after_amount" min-width="100"/>
                <el-table-column label="来源类型" prop="source_type" min-width="150" show-tooltip-when-overflow />
                <el-table-column label="来源单号" prop="source_sn" min-width="150" show-tooltip-when-overflow />
                <el-table-column label="记录时间" prop="create_time" min-width="180" />
            </el-table>
            <div class="flex justify-end mt-4">
                <paging v-model="pager" @change="queryLists" />
            </div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { usePaging } from '@/hooks/usePaging'
import balanceApi from '@/api/finance/balance'

// 查询参数
const queryParams = reactive({
    user: '',
    action: '',
    source_sn: '',
    source_type: '',
    start_time: '',
    end_time: ''
})

// 分页查询
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: balanceApi.lists,
    params: queryParams
})

onMounted(async () => {
    await queryLists()
})
</script>
