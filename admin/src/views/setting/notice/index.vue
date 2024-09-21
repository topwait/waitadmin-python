<template>
    <div>
        <!-- 表格栏 -->
        <el-card class="!border-none" shadow="never">
            <el-tabs v-model="tabsActive" @tab-change="queryNoticeLists">
                <el-tab-pane
                    v-for="(item, index) in tabsMap"
                    :key="index"
                    :label="item.name"
                    :name="item.type"
                    lazy
                />
            </el-tabs>
            <el-table :data="dataLists" size="large" class="mt-4">
                <el-table-column label="ID" prop="id" min-width="30" />
                <el-table-column label="通知场景" prop="name" min-width="140" />
                <el-table-column label="场景编号" prop="scene" min-width="80" />
                <el-table-column label="通知类型" prop="type" min-width="80" />
                <el-table-column label="系统通知" prop="sys_status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.sys_status === 1">启用</el-tag>
                        <el-tag v-else-if="row.sys_status === 0" type="danger">停用</el-tag>
                        <span v-else>-</span>
                    </template>
                </el-table-column>
                <el-table-column label="邮件通知" prop="ems_status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.ems_status === 1">启用</el-tag>
                        <el-tag v-else-if="row.ems_status === 0" type="danger">停用</el-tag>
                        <span v-else>-</span>
                    </template>
                </el-table-column>
                <el-table-column label="短信通知" prop="sms_status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.sms_status === 1">启用</el-tag>
                        <el-tag v-else-if="row.sms_status === 0" type="danger">停用</el-tag>
                        <span v-else>-</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="75" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['setting:notice:save']"
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
        <editor v-if="showEdit" ref="editorRef" @success="queryNoticeLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import noticeApi from '@/api/setting/notice'
import Editor from './editor.vue'

enum NoticeEnums {
    USER = 1,
    PLATFORM = 2
}

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()
const dataLists = ref<Array<any>>([])

// 激活的选项
const tabsActive = ref(NoticeEnums.USER)
// 选项卡数组
const tabsMap = [
    {
        name: '通知用户',
        type: NoticeEnums.USER
    },
    {
        name: '通知平台',
        type: NoticeEnums.PLATFORM
    }
]

/**
 * 查询通知渠道列表
 */
const queryNoticeLists = async (): Promise<void> => {
    dataLists.value = await noticeApi.lists()
}

/**
 * 处理通知参数编辑
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
    await queryNoticeLists()
})
</script>
