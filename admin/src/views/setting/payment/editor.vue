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
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="90px">
                <el-form-item label="支付名称" prop="name" required>
                    <el-radio :label="formData.name" :model-value="formData.name" />
                </el-form-item>
                <el-form-item label="支付图标" prop="icon">
                    <material-picker
                        v-model="formData.icon"
                        :limit="1"
                    />
                </el-form-item>
                <el-form-item label="显示名称" prop="shorter">
                    <el-input v-model="formData.shorter" clearable />
                </el-form-item>
                <template v-if="formData.channel === PayWayEnum.WXPAY">
                    <el-form-item  label="商户类型" prop="params.merchant_type" required>
                        <el-radio-group v-model="formData.params.merchant_type">
                            <el-radio value="ordinary_merchant">普通商户</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="接口版本" prop="params.interface_version" required>
                        <el-radio-group v-model="formData.params.interface_version">
                            <el-radio value="v3">v3</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="商户编号" prop="params.mch_id">
                        <el-input v-model="formData.params.mch_id" clearable />
                        <span class="form-tips">微信支付商户号</span>
                    </el-form-item>
                    <el-form-item label="支付密钥" prop="params.secret_key">
                        <el-input v-model="formData.params.secret_key" clearable />
                        <span class="form-tips">微信支付密钥 (paySignKey)</span>
                    </el-form-item>
                    <el-form-item label="支付证书私钥" prop="params.apiclient_key">
                        <el-input
                            type="textarea"
                            :rows="3"
                            v-model="formData.params.apiclient_key"
                            clearable
                        />
                        <span class="form-tips">微信商户证书私钥 (apiclient_key.pem)</span>
                    </el-form-item>
                    <el-form-item label="微信支付证书" prop="params.apiclient_cert">
                        <el-input
                            type="textarea"
                            :rows="3"
                            v-model="formData.params.apiclient_cert"
                            clearable
                        />
                        <span class="form-tips">微信商户支付证书 (apiclient_cert.pem)</span>
                    </el-form-item>
                </template>
                <template v-if="formData.channel === PayWayEnum.ALIPAY">
                    <el-form-item label="商户类型" prop="params.merchant_type" required>
                        <el-radio-group v-model="formData.params.merchant_type">
                            <el-radio value="ordinary_merchant">普通商户</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="应用ID" prop="params.app_id">
                        <el-input v-model="formData.params.app_id" clearable />
                        <span class="form-tips">支付宝应用 (APP_ID)</span>
                    </el-form-item>
                    <el-form-item label="应用私钥" prop="params.private_key">
                        <el-input
                            type="textarea"
                            :rows="3"
                            v-model="formData.params.private_key"
                            clearable
                        />
                        <span class="form-tips">支付宝应用私钥RSA2（private_key） </span>
                    </el-form-item>
                    <el-form-item label="支付公钥" prop="params.public_key">
                        <el-input
                            type="textarea"
                            :rows="3"
                            v-model="formData.params.public_key"
                            clearable
                        />
                        <span class="form-tips">支付宝公钥RSA2（ali_public_key） </span>
                    </el-form-item>
                </template>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="999999" />
                </el-form-item>
                <el-form-item label="状态" prop="status">
                    <el-radio-group v-model="formData.status">
                        <el-radio :value="1">启用</el-radio>
                        <el-radio :value="0">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import paymentApi from '@/api/setting/payment'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '设置' : ''
})

enum PayWayEnum {
    BALANCE = 1,
    WXPAY = 2,
    ALIPAY = 3
}

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: 0,
    channel: 1,
    shorter: '',
    name: '',
    icon: '',
    sort: 0,
    status: 0,
    params: {}
})

// 表单规则
const formRules: any = reactive({
    'icon': [
        { required: true, message: '请选择支付图标', trigger: ['blur'] },
        { max: 250, message: '支付图标链接不能大于250个字符', trigger: ['blur'] }
    ],
    'shorter': [
        { required: true, message: '请填写显示名称', trigger: ['blur'] },
        { max: 32, message: '显示名称不能大于32个字符', trigger: ['blur'] }
    ]
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await paymentApi.save(formData)
            .finally(() => {
                loading.value = false
            })
    }

    feedback.msgSuccess('设置成功')
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
        const data = await paymentApi.detail(row.id)
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
