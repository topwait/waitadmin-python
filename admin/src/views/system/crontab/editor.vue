<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="680px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="任务名称" prop="name">
                    <el-input v-model="formData.name" placeholder="请输入任务名称" maxlength="64" />
                </el-form-item>
                <el-form-item label="执行命令" prop="command">
                    <el-input v-model="formData.command" placeholder="请输入执行命令" maxlength="64" />
                </el-form-item>
                <el-form-item label="触发条件" prop="rules" required>
                    <el-select v-model="formData.trigger" @change="changeTrigger">
                        <el-option label="固定间隔触发" value="interval"/>
                        <el-option label="特定周期触发" value="cron"/>
                        <el-option label="特定时间触发" value="date"/>
                    </el-select>
                </el-form-item>
                <el-form-item label="触发规则" required>
                    <div class="w-full" v-for="(item, index) in formData.rules" :key="index">
                        <template v-if="formData.trigger == 'interval'">
                            <hover-close @close="handleDelRules(index)">
                                <div class="flex">
                                    <div class="mr-2 mb-[8px] w-[150px]">
                                        <el-select v-model="item.key" >
                                            <el-option label="间隔几周" value="weeks"/>
                                            <el-option label="间隔几天" value="days"/>
                                            <el-option label="间隔几小时" value="hours"/>
                                            <el-option label="间隔几分钟" value="minutes"/>
                                            <el-option label="间隔多少秒" value="seconds"/>
                                            <el-option label="开始日期" value="start_date"/>
                                            <el-option label="结束日期" value="end_date"/>
                                        </el-select>
                                    </div>
                                    <div class="flex-1 mb-[8px]">
                                        <el-date-picker
                                            v-if="item.key === 'start_date' || item.key === 'end_date'"
                                            type="datetime"
                                            v-model="item.value"
                                            placeholder="请选择日期"
                                        />
                                        <el-input v-else
                                                  type="number"
                                                  v-model="item.value"
                                                  :min="1"
                                                  :max="9999999999"
                                                  placeholder="请输入规则"
                                        />
                                    </div>
                                </div>
                            </hover-close>
                        </template>
                        <template v-if="formData.trigger === 'cron'">
                            <hover-close @close="handleDelRules(index)">
                                <div class="flex">
                                    <div class="mr-2" style="width: 150px; margin-bottom: 5px;">
                                        <el-select v-model="item.key">
                                            <el-option label="4位数的年份" value="year"/>
                                            <el-option label="月份(1-12)" value="month"/>
                                            <el-option label="日期(1-31)" value="day"/>
                                            <el-option label="ISO周(1-53)" value="week"/>
                                            <el-option label="星期几(0-6)" value="day_of_week"/>
                                            <el-option label="小时(0-23)" value="hour"/>
                                            <el-option label="分钟(0-59)" value="minute"/>
                                            <el-option label="最早触发的时间" value="start_date"/>
                                            <el-option label="最晚触发的时间" value="end_date"/>
                                        </el-select>
                                    </div>
                                    <div style="flex: 1; margin-bottom: 5px;">
                                        <el-input v-model="item.value" :min="1" :max="9999999999" placeholder="请输入规则" />
                                    </div>
                                </div>
                            </hover-close>
                        </template>
                        <template v-if="formData.trigger === 'date'">
                            <el-date-picker
                                type="datetime"
                                v-model="item.value"
                                placeholder="请选择运行日期"
                            />
                        </template>
                    </div>
                    <el-button v-if="formData.trigger !== 'date'" class="w-full" @click="handleAddRules">添加</el-button>
                </el-form-item>
                <el-form-item label="附带参数" prop="params">
                    <el-input v-model="formData.params" placeholder='请输入参数，如: {"name": "wa"}' maxlength="64" />
                </el-form-item>
                <el-form-item label="并发数量" prop="concurrent">
                    <el-select
                        v-model="formData.concurrent"
                        placeholder="请选择并发数量"
                        clearable
                    >
                        <el-option
                            v-for="(item, index) in 10"
                            :key="index"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="备注信息" prop="remarks">
                    <el-input
                        type="textarea"
                        :rows="4"
                        v-model.trim="formData.remarks"
                        show-word-limit
                    />
                </el-form-item>
                <el-form-item label="运行状态" prop="status">
                    <el-radio-group v-model="formData.status">
                        <el-radio :value="1">立即启动</el-radio>
                        <el-radio :value="0">暂停执行</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="任务列表" v-if="formData.tasks.length > 0">
                    <el-table :data="formData.tasks" size="large">
                        <el-table-column label="名称" prop="id" min-width="150" show-tooltip-when-overflow />
                        <el-table-column label="下次执行时间" prop="next_run_time" min-width="175" show-tooltip-when-overflow />
                    </el-table>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import crontabApi from '@/api/system/crontab'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑任务' : '新增任务'
})

// 表单数据
const loading = ref(false)
const formData = reactive<any>({
    id: '',        // 主键ID
    name: '',      // 任务名称
    command: '',   // 执行命令
    params: '',    // 附带参数
    remarks: '',   // 备注信息
    concurrent: 1, // 并发数量
    status: 1,     // 运行状态: [0=否, 1=是]
    trigger: 'interval',
    rules: [
        {key: 'weeks', value: ''}
    ],
    tasks: []
})

// 表单规则
const formRules: any = reactive({
    name: [
        { required: true, message: '任务名称不能为空', trigger: ['blur'] },
        { max: 64, message: '任务名称不能大于64个字符', trigger: ['blur'] }
    ],
    command: [
        { required: true, message: '执行命令不能为空', trigger: ['blur'] },
        { max: 200, message: '执行命令不能大于200个字符', trigger: ['blur'] }
    ],
    params: [
        { max: 200, message: '附带参数不能大于200个字符', trigger: ['blur'] }
    ],
    remarks: [
        { max: 300, message: '备注信息不能大于300个字符', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    if (_checkRules() === true) {
        loading.value = true
        if (showMode.value === 'edit') {
            await crontabApi.edit(formData)
                .finally(() => {
                    loading.value = false
                })
        } else {
            await crontabApi.add(formData)
                .finally(() => {
                    loading.value = false
                })
        }

        feedback.msgSuccess('操作成功')
        emits('close')
        emits('success')
    }
}

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

    if (type === 'edit') {
        const data = await crontabApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
            }
        }
    }
}

/**
 * 添加规则
 */
const handleAddRules = (): void => {
    if (formData.trigger === 'interval') {
        formData.rules.push({key: 'weeks', value: ''})
    }
}

/**
 * 删除规则
 */
const handleDelRules = (index: number): void => {
    if (formData.rules.length <= 1) {
        return feedback.msgError('至少需保留1个规则')
    }
    formData.rules.splice(index, 1)
}

/**
 * 改变事件
 */
const changeTrigger = (value: any): void => {
    if (value === 'interval') {
        formData.rules = [{key: 'weeks', value: ''}]
    } else if (value === 'cron') {
        formData.rules = [{key: 'year', value: ''}]
    } else {
        formData.rules = [{key: 'run_date', value: ''}]
    }
}

/**
 * 验证规则
 */
const _checkRules = (): boolean|any => {
    if (formData.rules.length <= 0) {
        return feedback.msgError('之前填写一个触发规则')
    }

    let coll: string[] = []
    for (let i = 0; i < formData.rules.length; i++) {
        const rules = formData.rules[0]
        if (rules?.key === undefined || rules?.value === undefined) {
            return feedback.msgError('触发规则数据异常')
        }
        if (!rules.value) {
            return feedback.msgError('请填写完善触发规则')
        }

        if (coll.includes(rules.value)) {
            return feedback.msgError('触发规则类型不允许重复配置')
        }
        coll.push(rules.key)
    }
    return true
}

defineExpose({
    open
})
</script>

<style scoped lang="scss">
:deep(.el-date-editor.el-input) {
    width: 100%;
}
</style>
