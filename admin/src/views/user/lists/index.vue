<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="用户信息">
                    <el-input
                        v-model="queryParams.keyword"
                        class="w-[250px]"
                        placeholder="请输入用户编号/昵称/手机"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="用户状态">
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
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="编号" prop="sn" min-width="100" />
                <el-table-column label="头像" prop="avatar" min-width="80">
                    <template #default="{ row }">
                        <el-avatar :src="row.avatar" :size="50" />
                    </template>
                </el-table-column>
                <el-table-column label="昵称" prop="nickname" min-width="120" />
                <el-table-column label="联系电话" prop="mobile" min-width="110" />
                <el-table-column label="电子邮箱" prop="email" min-width="120" />
                <el-table-column label="分组" prop="group" min-width="120" />
                <el-table-column label="状态" prop="is_disable" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_disable === 0">正常</el-tag>
                        <el-tag v-else type="danger">禁用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time" min-width="175" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link @click="handleEditor('detail', row)">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="flex justify-end mt-4">
                <paging v-model="pager" @change="queryLists" />
            </div>
        </el-card>

        <!-- 编辑器 -->
        <detail v-if="showDetail" ref="detailRef" @success="queryLists" @close="showDetail = false" />
    </div>
</template>

<script setup lang="ts">
import { usePaging } from '@/hooks/usePaging'
import userApi from '@/api/users/user'
import Detail from './detail.vue'

const showDetail = ref(false)
const detailRef = shallowRef<InstanceType<typeof Detail>>()

// 查询参数
const queryParams = reactive({
    keyword: '',
    is_disable: ''
})

// 分页查询
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: userApi.lists,
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
    showDetail.value = true
    await nextTick()
    detailRef.value?.open(type, row)
}

onMounted(async () => {
    await queryLists()
})
</script>
