<template>
    <div>
        <!-- 搜索栏 -->
        <el-card class="!border-none mb-4" shadow="never">
            <el-form class="mb-[-16px]" :model="queryParams" :inline="true">
                <el-form-item label="文章标题" prop="title">
                    <el-input
                        v-model="queryParams.title"
                        class="w-[250px]"
                        placeholder="请输入文章标题"
                        clearable
                        @keyup.enter="resetPaging"
                    />
                </el-form-item>
                <el-form-item label="文章状态">
                    <el-select v-model="queryParams.status" class="w-[250px]">
                        <el-option value="" label="全部" />
                        <el-option value="1" label="显示" />
                        <el-option value="0" label="隐藏" />
                    </el-select>
                </el-form-item>
                <el-form-item label="创建时间">
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
            <el-button type="primary" v-perms="['content:article:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="封面" prop="image" min-width="80">
                    <template #default="{ row }">
                        <photos
                            v-if="row.image"
                            :src="row.image"
                            :width="60"
                            :height="45"
                            :preview-src-list="[row.image]"
                            :preview-teleported="true"
                            fit="contain"
                        />
                    </template>
                </el-table-column>
                <el-table-column label="文章标题" prop="title" min-width="250" show-tooltip-when-overflow />
                <el-table-column label="所属类目" prop="category" min-width="120" show-tooltip-when-overflow />
                <el-table-column label="浏览数" prop="browse" min-width="100" />
                <el-table-column label="收藏数" prop="collect" min-width="100" />
                <el-table-column label="排序" prop="sort" min-width="100" />
                <el-table-column label="置顶" prop="is_topping" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_topping === 1">是</el-tag>
                        <el-tag v-else type="danger">否</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="推荐" prop="is_recommend" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_recommend === 1">是</el-tag>
                        <el-tag v-else type="danger">否</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="状态" prop="is_show" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.is_show === 1">显示</el-tag>
                        <el-tag v-else type="danger">隐藏</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time" min-width="170" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['content:article:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-perms="['content:article:delete']"
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
import articleApi from '@/api/content/article'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()

// 查询参数
const queryParams = reactive({
    title: '',
    status: '',
    start_time: '',
    end_time: ''
})

// 分页查询
const { pager, queryLists, resetParams, resetPaging } = usePaging({
    fetchFun: articleApi.lists,
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
            await articleApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
})
</script>
