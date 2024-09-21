<template>
    <el-card class="!border-none h-full" shadow="never">
        <el-tabs v-model="tabIndex" type="card">
            <el-tab-pane v-loading="pager.loading" label="收藏文章" name="collect">
                <el-table :data="pager.lists" size="large" class="mt-4">
                    <el-table-column label="封面图" prop="image" min-width="100">
                        <template #default="{ row }">
                            <photos
                                v-if="row?.image"
                                :src="row?.image"
                                :width="60"
                                :height="45"
                                :preview-src-list="[row?.image]"
                                :preview-teleported="true"
                                fit="contain"
                            />
                        </template>
                    </el-table-column>
                    <el-table-column label="文章标题" prop="title" min-width="200" show-tooltip-when-overflow  />
                    <el-table-column label="阅读量" prop="browse" min-width="80" />
                    <el-table-column label="收藏量" prop="collect" min-width="80" />
                    <el-table-column label="收藏时间" prop="create_time" min-width="175" />
                    <el-table-column label="操作" width="80" fixed="right">
                        <template #default="{ row }">
                            <el-button
                                type="danger"
                                link
                                @click="handleDelete(row?.id)"
                            >
                                删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div v-if="pager.lists.length > 0" class="flex justify-end my-4">
                    <paging
                        v-model="pager"
                        layout="prev, pager, next"
                        @change="queryLists"
                    />
                </div>
            </el-tab-pane>
        </el-tabs>
    </el-card>
</template>

<script setup lang="ts">
import { usePaging } from '@/composables/usePaging'
import articleApi from '~/api/article'
import userApi from '~/api/user'

const tabIndex: Ref<string> = ref('collect')

// 分页查询
const { pager, queryLists } = usePaging<UserCollectResponse>({
    fetchFun: userApi.collect
})

/**
 * 处理删除
 *
 * @param {number} id
 * @returns {Promise<void>}
 */
const handleDelete = async (id: number): Promise<void> => {
    feedback.confirm('确定要删除此项数据吗?')
        .then(async () => {
            await articleApi.collect(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
})
</script>

<style scoped lang="scss">
:deep(.el-tabs) {
    .el-tabs__item.is-active,
    .el-tabs__item:hover {
        color: var(--el-text-color-regular);
    }
}
</style>