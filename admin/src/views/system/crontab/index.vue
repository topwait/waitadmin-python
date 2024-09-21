<template>
    <div>
        <!-- 描述栏 -->
        <el-card class="!border-none" shadow="never">
            <el-alert
                type="warning"
                title="任务调用框架: APscheduler (Advanced Python Scheduler)"
                :closable="false"
                show-icon
            />
        </el-card>

        <!-- 表格栏 -->
        <el-card v-loading="pager.loading" class="!border-none mt-4" shadow="never">
            <el-button type="primary" v-perms="['system:crontab:add']" @click="handleEditor('add')">
                <template #icon>
                    <icon name="el-icon-plus" />
                </template>
                <span>新增</span>
            </el-button>
            <el-table :data="pager.lists" size="large" class="mt-4">
                <el-table-column label="任务名称" prop="name" min-width="130" show-tooltip-when-overflow />
                <el-table-column label="命令" prop="command" min-width="160" show-tooltip-when-overflow />
                <el-table-column label="参数" prop="params" min-width="150" show-tooltip-when-overflow />
                <el-table-column label="备注信息" prop="remarks" min-width="130" show-tooltip-when-overflow />
                <el-table-column label="运行状态" prop="status" min-width="90">
                    <template #default="{ row }">
                        <el-tag v-if="row.status === 1">运行中</el-tag>
                        <el-tag v-else-if="row.status === 2" type="danger">已停止</el-tag>
                        <el-tooltip
                            v-else-if="row.status === 3"
                            effect="dark"
                            :content="row.error"
                        >
                            <el-tag type="danger">错误</el-tag>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="并发数" prop="concurrent" min-width="68" >
                    <template #default="{ row }">
                        <el-tag type="info">{{ row.concurrent }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="执行时长" prop="exe_time" min-width="90">
                    <template #default="{ row }">
                        {{ row.exe_time }}ms
                    </template>
                </el-table-column>
                <el-table-column label="最大时长" prop="max_time" min-width="90">
                    <template #default="{ row }">
                        {{ row.max_time }}ms
                    </template>
                </el-table-column>
                <el-table-column label="最后执行时间" prop="last_time" min-width="175" />
                <el-table-column label="操作" width="120" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['system:crontab:edit']"
                            type="primary"
                            link
                            @click="handleEditor('edit', row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            v-perms="['system:crontab:delete']"
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
import crontabApi from '@/api/system/crontab'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()

// 分页查询
const { pager, queryLists } = usePaging({
    fetchFun: crontabApi.lists
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
            await crontabApi.delete(id)
            feedback.msgSuccess('删除成功')
            await queryLists()
        }).catch(() => {})
}

onMounted(async () => {
    await queryLists()
})
</script>
