<template>
    <div>
        <!-- 表格栏 -->
        <el-card class="!border-none" shadow="never">
            <el-table :data="dataLists" size="large" class="mt-4">
                <el-table-column label="图标" prop="image" min-width="135">
                    <template #default="{ row }">
                        <el-image :src="row.image" class="w-[100px] h-[23px]" />
                    </template>
                </el-table-column>
                <el-table-column label="短信渠道" prop="name" min-width="110" />
                <el-table-column label="渠道描述" prop="desc" min-width="180" />
                <el-table-column label="状态" prop="status" min-width="80">
                    <template #default="{ row }">
                        <el-tag v-if="row.status === 1">启用</el-tag>
                        <el-tag v-else type="danger">停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="70" fixed="right">
                    <template #default="{ row }">
                        <el-button
                            v-perms="['setting:sms:save']"
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
        <editor v-if="showEdit" ref="editorRef" @success="querySmsLists" @close="showEdit = false" />
    </div>
</template>

<script setup lang="ts">
import smsApi from '@/api/setting/sms'
import Editor from './editor.vue'

const showEdit = ref(false)
const editorRef = shallowRef<InstanceType<typeof Editor>>()
const dataLists = ref<Array<any>>([])

/**
 * 查询短信渠道列表
 */
const querySmsLists = async (): Promise<void> => {
    dataLists.value = await smsApi.lists()
}

/**
 * 处理短信渠道编辑
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
    await querySmsLists()
})
</script>
