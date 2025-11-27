<template>
    <popup
        :show="showPop"
        title="创建用户"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="登录账号" prop="account">
                    <el-input v-model="formData.account" placeholder="请输入登录账号" />
                </el-form-item>
                <el-form-item label="账号昵称" prop="nickname">
                    <el-input v-model="formData.nickname" placeholder="请输入账号昵称" />
                </el-form-item>
                <el-form-item label="手机号码" prop="mobile">
                    <el-input v-model="formData.mobile" placeholder="请输入手机号">
                        <template #prepend>
                            <el-select model-value="+86" style="width: 80px">
                                <el-option label="+86" value="+86" />
                            </el-select>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item label="电子邮箱" prop="email">
                    <el-input v-model="formData.email" placeholder="请输入邮箱号"/>
                </el-form-item>
                <el-form-item label="登录密码" prop="password">
                    <el-input
                        v-model="formData.password"
                        type="password"
                        show-password
                        placeholder="请输入6~20位数字+字母或符号组合密码"
                    />
                </el-form-item>
                <el-form-item label="确认密码" prop="password_confirm">
                    <el-input
                        v-model="formData.password_confirm"
                        type="password"
                        show-password
                        placeholder="请再次输入密码"
                    />
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import userApi from '@/api/users/user'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showPop = ref<boolean>(false)

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    account: '',    // 账号
    email: '',      // 邮箱
    mobile: '',     // 电话
    nickname: '',   // 昵称
    password: '',   // 密码
    password_confirm: ''
})

// 表单规则
const formRules = reactive({
    account: [
        { required: true, message: '请输入账号', trigger: 'blur' },
        { min: 4, max: 20, message: '账号长度应为4~20个字符', trigger: 'blur'}
    ],
    nickname: [
        { required: true, message: '请输入昵称', trigger: 'blur' },
        { min: 4, max: 20, message: '昵称长度应为4~20个字符', trigger: 'blur'}
    ],
    mobile: [
        {
            pattern: /^((0\d{2,3}-\d{7,8})|(1[3584]\d{9}))$/,
            message: '请输入正确的手机号码',
            trigger: 'blur'
        }
    ],
    email: [
        {
            pattern: /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
            min: 2,
            max: 30,
            message: '邮箱格式错误',
            trigger: 'blur'
        }
    ],
    password: [
        { required: true, message: '请输入6-20位数字+字母和符号组合', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应为6~20个字符', trigger: 'blur'}
    ],
    password_confirm: [
        { required: true, message: '请输入确认密码', trigger: 'blur' },
        {
            trigger: 'blur',
            validator(_rule: any, value: any, callback: any) {
                if (value === '') {
                    callback(new Error('请再次输入密码'))
                } else if (value !== formData.password) {
                    callback(new Error('两次输入的密码不一致'))
                } else {
                    callback()
                }
            }
        }
    ]
})

/**
 * 提交表单
 *
 * @returns {Promise<void>}
 * @author zero
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate().then(async () => {
        loading.value = true
        await userApi.create(formData)
            .finally(() => {
                loading.value = false
            })
        feedback.msgSuccess('操作成功')
        emits('close')
        emits('success')
    }).catch(() => {})
}

/**
 * 打开表单
 *
 * @returns {Promise<void>}
 * @author zero
 */
const open = async (): Promise<void> => {
    showPop.value = true
}

defineExpose({
    open
})
</script>
