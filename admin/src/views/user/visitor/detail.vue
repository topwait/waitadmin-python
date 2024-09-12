<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :async-close="true"
        width="800px"
        :confirmButtonText="false"
        :cancelButtonText="false"
        @close="emits('close')"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" label-width="80px">
                <el-form-item label="操作人：">
                    <span>{{ formData.nickname || '-' }} | {{ formData.username || '-' }}</span>
                </el-form-item>
                <el-form-item label="请求信息：">
                    <span>{{ formData.method }} | {{ formData.ip }} | {{ formData.ua }}</span>
                </el-form-item>
                <el-form-item label="请求地址：" prop="url">
                    <span>{{ formData.url }}</span>
                </el-form-item>
                <el-form-item label="请求UA：" prop="user_agent">
                    <span>{{ formData.user_agent }}</span>
                </el-form-item>
                <el-form-item label="请求参数：" prop="params">
                    <span>{{ formData.params || '-' }}</span>
                </el-form-item>
                <el-form-item label="调用函数：" prop="endpoint">
                    <span>{{ formData.endpoint }}</span>
                </el-form-item>
                <el-form-item label="记录时间：" prop="create_time">
                    <span>{{ formData.create_time }}</span>
                </el-form-item>
                <el-form-item label="执行开始：" prop="start_time">
                    <span>{{ formData.start_time }}</span>
                </el-form-item>
                <el-form-item label="执行结束：" prop="end_time">
                    <span>{{ formData.end_time }}</span>
                </el-form-item>
                <el-form-item label="执行耗时：" prop="task_time">
                    <span>{{ formData.task_time }}ms</span>
                </el-form-item>
                <el-form-item label="执行状态：" prop="status">
                    <el-tag v-if="formData.status === 1">成功</el-tag>
                    <el-tag v-else type="danger">失败</el-tag>
                </el-form-item>
                <el-form-item v-if="formData.error" label="错误信息：" prop="error">
                    <span>{{ formData.error  }}</span>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import journalApi from '@/api/system/journal'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('detail')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'detail' ? '详情' : ''
})

// 表单数据
const formData = reactive({
    id: '',         // 主键ID
    nickname: '',   // 操作昵称
    username: '',   // 操作账号
    method: '',     // 请求方法
    url: '',        // 请求路由
    ip: '',         // 请求IP
    ua: '',         // 请求UA
    user_agent: '', // UA详情
    endpoint: '',   // 执行函数
    params: '',     // 请求参数
    error: '',      // 错误信息
    trace: '',      // 错误异常
    status: 1,      // 执行状态: [1=成功, 2=失败]
    start_time: '', // 开始时间: 毫秒
    end_time: '',   // 结束时间: 毫秒
    task_time: '',  // 耗时时间: 毫秒
    create_time: '' // 操作时间
})

/**
 * 打开表单
 *
 * @param {string} type
 * @param {any} row
 * @returns {Promise<void>}
 */
const open = async (type: string, row?: any): Promise<void> => {
    showMode.value = type
    showEdit.value = true

    if (type === 'detail') {
        const data = await journalApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                // @ts-ignore
                formData[key] = data[key]
            }
        }
    }
}

defineExpose({
    open
})
</script>
