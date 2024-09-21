<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="充值金额" prop="money">
                    <el-input type="number" v-model="formData.money" placeholder="请输入充值金额" />
                </el-form-item>
                <el-form-item label="赠送金额" prop="give_money">
                    <el-input type="number" v-model="formData.give_money" placeholder="请输入赠送金额" />
                </el-form-item>
                <el-form-item label="排序" prop="sort" label-width="100px">
                    <el-input-number v-model="formData.sort" :min="0" :max="9999" />
                </el-form-item>
                <el-form-item label="状态">
                    <el-radio-group v-model="formData.is_disable">
                        <el-radio :value="0">正常</el-radio>
                        <el-radio :value="1">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import rechargePackApi from '@/api/market/recharge'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑套餐' : '新增套餐'
})

// 表单数据
const loading = ref<boolean>(false)
const formData: any = reactive({
    id: 0,           // 套餐ID
    money: '',       // 充值金额
    give_money: '',  // 赠送金额
    sort: 0,        // 排序编号
    is_show: 0       // 是否显示:[0=否, 1=是]
})

// 表单规则
const formRules: any = reactive({
    money: [
        { required: true, message: '请填写充值金额', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await rechargePackApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await rechargePackApi.add(formData)
            .finally(() => {
                loading.value = false
            })
    }

    feedback.msgSuccess('操作成功')
    emits('close')
    emits('success')
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
        const data = await rechargePackApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
            }
        }
    }
}

defineExpose({
    open
})
</script>

<style scoped lang="scss">
.avatar {
    position: relative;
    display: flex;
    cursor: pointer;
    .change {
        position: absolute;
        bottom: 0;
        display: none;
        width: 100%;
        height: 50%;
        line-height: 33px;
        text-align: center;
        background-color: #00000080;
        border-bottom-right-radius: 9999px;
        border-bottom-left-radius: 9999px;
    }
    &:hover {
        .change {
            display: block;
        }
    }
}
</style>
