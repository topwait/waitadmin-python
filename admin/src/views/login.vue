<template>
    <div class="login">
        <div class="flex-1 flex items-center justify-center">
            <div v-if="config.cover" class="login-cover">
                <photos
                    :src="config.cover"
                    :width="400"
                    height="100%"
                    borderTopLeftRadius="8px"
                    borderBottomLeftRadius="8px"
                />
            </div>
            <div class="login-card" :class="config.cover ? 'cover-style': ''">
                <h2>{{ config.name }}</h2>
                <el-form ref="formRef" :model="formData" size="large" :rules="rules">
                    <el-form-item prop="account">
                        <el-input
                            v-model="formData.username"
                            placeholder="请输入账号"
                            @keyup.enter="handleEnter"
                        >
                            <template #prepend>
                                <icon name="el-icon-User" />
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input
                            ref="passwordRef"
                            show-password
                            v-model="formData.password"
                            placeholder="请输入密码"
                            @keyup.enter="handleEnter"
                        >
                            <template #prepend>
                                <icon name="el-icon-Lock" />
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item v-if="config.enable_captcha" prop="code">
                        <div class="flex items-center">
                            <el-input
                                v-model="formData.code"
                                placeholder="请输入验证码"
                                @keyup.enter="handleEnter"
                            >
                                <template #prepend>
                                    <icon name="el-icon-Key" />
                                </template>

                            </el-input>
                            <div class="captcha" @click="getCaptcha">
                                <img class="w-full h-full"
                                     :src="captcha"
                                     alt="code"
                                />
                            </div>
                        </div>
                    </el-form-item>
                    <el-form-item>
                        <el-checkbox v-model="remAccount" label="记住账号" />
                    </el-form-item>
                    <el-form-item>
                        <el-button
                            type="primary"
                            size="large"
                            class="w-full"
                            :loading="isLock"
                            @click="onLockLogin"
                        >
                            登录
                        </el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { InputInstance, FormInstance } from 'element-plus'
import { useLockFn } from '@/hooks/useLockFn'
import { cacheEnum } from '@/enums/cache'
import useAppStore from '@/stores/modules/app'
import useUserStore from '@/stores/modules/user'
import cacheUtil from '@/utils/cache'
import loginApi from '@/api/login'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()

const passwordRef = shallowRef<InputInstance>()
const formRef = shallowRef<FormInstance>()
const config = computed(() => appStore.config)

// 验证码
const captcha = ref('')

// 记住密码
const remAccount = ref(false)

// 表单参数
const formData = reactive({
    username: '',
    password: '',
    uuid: '',
    code: ''
})

// 验证规则
const rules = {
    username: [
        { required: true, message: '请输入登录账号', trigger: ['blur'] }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: ['blur'] }
    ],
    code: [
        { required: true, message: '请输入验证码', trigger: ['blur'] }
    ]
}

/**
 * 获取验证码
 */
const getCaptcha = async (): Promise<void> => {
    const data = await loginApi.captcha()
    formData.uuid = data.uuid
    captcha.value = data.image
}

/**
 * 处理回车事件
 */
const handleEnter = (): any => {
    if (!formData.password) {
        return passwordRef.value?.focus()
    }
    handleLogin()
}

/**
 * 处理登录事件
 */
const handleLogin = async (): Promise<void> => {
    await formRef.value?.validate()

    if (remAccount.value) {
        cacheUtil.set(cacheEnum.ACCOUNT_KEY, {
            remember: remAccount.value,
            username: remAccount.value ? formData.username : ''
        })
    } else {
        cacheUtil.remove(cacheEnum.ACCOUNT_KEY)
    }

    try {
        await userStore.login(formData)

        const { query: { redirect } } = route
        const path = typeof redirect === 'string' ? redirect : '/'
        await router.push(path)
    }  catch (err) {
        await getCaptcha()
    }
}

const { isLock, lockFn: onLockLogin } = useLockFn(handleLogin)

onMounted(async () => {
    if (config.value.enable_captcha) {
        await getCaptcha()
    }
    const value = cacheUtil.get(cacheEnum.ACCOUNT_KEY)
    if (value?.remember) {
        remAccount.value = value.remember
        formData.username = value.username
    }
})
</script>

<style scoped lang="scss">
.login {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-image: url('@/assets/images/login_bg.png');
    background-position: 50%;
    background-size: cover;
    .login-cover {
        width: 400px;
        height: 400px;
        overflow: hidden;
    }
    .login-card {
        width: 400px;
        height: 400px;
        padding: 25px 30px 15px;
        background: var(--el-bg-color);
        border-radius: 8px;
        &.cover-style {
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
        }
        h2 {
            margin-bottom: 25px;
            font-size: 18px;
            font-weight: bold;
            color: var(--el-text-color-regular);
            text-align: center;
        }
        .captcha {
            flex: none;
            width: 100px;
            height: 40px;
            margin-left: 12px;
            cursor: pointer;
            border: 1px var(--el-border-color-light) solid;
            border-radius: 3px;
        }
        :deep(.el-input__inner) {
            height: 40px;
        }
        :deep(.el-checkbox:last-of-type) {
            height: 20px;
        }
    }
}
</style>
