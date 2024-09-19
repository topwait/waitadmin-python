<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="560px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="管理头像" prop="avatar">
                    <upload-cropper-select v-model="formData.avatar" />
                </el-form-item>
                <el-form-item label="所属部门" prop="dept_id">
                    <el-tree-select
                        class="flex-1"
                        v-model="formData.dept_id"
                        :data="optionsData.dept"
                        clearable
                        node-key="id"
                        :props="{
                            value: 'id',
                            label: 'name',
                            disabled(data: any) {
                                return data.is_disable !== 0
                            }
                        }"
                        check-strictly
                        :default-expand-all="true"
                        placeholder="请选择上级部门"
                    />
                </el-form-item>
                <el-form-item label="所属岗位" prop="post_id">
                    <el-select
                        v-model="formData.post_id"
                        placeholder="请选择岗位"
                        clearable
                    >
                        <el-option
                            v-for="(item, index) in optionsData.post"
                            :key="index"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="所属角色" prop="role_id">
                    <el-select
                        v-model="formData.role_id"
                        :disabled="formData.id === 1"
                        placeholder="请选择角色"
                        clearable
                    >
                        <el-option v-if="formData.id === 1" label="系统管理员" :value="0" />
                        <el-option
                            v-for="(item, index) in optionsData.role"
                            :key="index"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="用户昵称" prop="nickname">
                    <el-input v-model="formData.nickname" placeholder="请输入用户昵称" maxlength="20" />
                </el-form-item>
                <el-form-item label="登录账号" prop="username">
                    <el-input v-model="formData.username" placeholder="请输入登录账号" maxlength="20" />
                </el-form-item>
                <el-form-item label="登录密码" prop="password">
                    <el-input
                        type="password"
                        v-model="formData.password"
                        placeholder="请输入登录密码"
                        maxlength="20"
                        show-password
                    />
                </el-form-item>
                <el-form-item label="确认密码" prop="password_confirm">
                    <el-input
                        type="password"
                        v-model="formData.password_confirm"
                        placeholder="请输入确认密码"
                        maxlength="20"
                        show-password
                    />
                </el-form-item>
                <el-form-item label="联系电话" prop="mobile">
                    <el-input v-model="formData.mobile" placeholder="请输入联系电话" />
                </el-form-item>
                <el-form-item label="电子邮箱" prop="email">
                    <el-input v-model="formData.email" placeholder="请输入电子邮箱" />
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
import { useDictOptions } from '@/hooks/useOption'
import feedback from '@/utils/feedback'
import authRoleApi from '@/api/auth/role'
import authPostApi from '@/api/auth/post'
import authDeptApi from '@/api/auth/dept'
import authAdminApi from '@/api/auth/admin'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑管理员' : '新增管理员'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: '',               // 管理ID
    role_id: '',          // 角色ID
    dept_id: '',          // 部门ID
    post_id: '',          // 岗位ID
    avatar: '',           // 用户头像
    nickname: '',         // 用户昵称
    username: '',         // 登录账号
    password: '',         // 登录密码
    password_confirm: '', // 确认密码
    mobile: '',            // 联系电话
    email: '',            // 电子邮箱
    is_disable: 0         // 是否禁用:[0=否, 1=是]
})

// 密码规则
const passwordConfirmValidator = (_rule: object, value: string, callback: any) => {
    if (formData.password) {
        if (!value) {
            callback(new Error('请再次输入密码'))
        }
        if (value !== formData.password) {
            callback(new Error('两次输入密码不一致!'))
        }
    }
    callback()
}

// 表单规则
const formRules = reactive({
    role_id: [
        { required: true, message: '请选择所属角色', trigger: ['blur'] }
    ],
    avatar: [
        { required: true, message: '请上传头像', trigger: 'blur' },
        { max: 250, message: '头像链接不能大于250个字符', trigger: 'blur' }
    ],
    nickname: [
        { required: true, message: '用户昵称不能为空', trigger: 'blur' },
        { max: 20, message: '用户昵称不能大于20个字符', trigger: 'blur' }
    ],
    username: [
        { required: true, message: '登录账号不能为空', trigger: 'blur' },
        { max: 20, message: '登录账号不能大于20个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '登陆密码不能为空', trigger: 'blur' },
        { min: 6, max: 20, message: '登陆密码长度必须介于 6 和 20 之间', trigger: 'blur' },
        { pattern: /^[^<>"'|\\]+$/, message: "登陆密码不能包含非法字符：< > \" ' \\\ |", trigger: 'blur' }
    ] as any[],
    password_confirm: [
        { required: true, message: '确认密码不能为空', trigger: 'blur' },
        {
            validator: passwordConfirmValidator,
            trigger: 'blur'
        }
    ] as any[]
})

// 字典选项
const { optionsData } = useDictOptions<{
    role: any[],
    post: any[],
    dept: any[]
}>({
    role: {
        api: authRoleApi.whole
    },
    post: {
        api: authPostApi.whole
    },
    dept: {
        api: authDeptApi.whole
    }
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await authAdminApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await authAdminApi.add(formData)
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
        formRules.password = []
        formRules.password_confirm = [
            {
                validator: passwordConfirmValidator,
                trigger: 'blur'
            }
        ]
        const data = await authAdminApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
                if (key === 'dept_id' || key === 'post_id') {
                    formData[key] = data[key] ? data[key] : ''
                }
            }
        }
    }
}

defineExpose({
    open
})
</script>
