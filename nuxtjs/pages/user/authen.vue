<template>
    <view
        v-loading="loading"
        element-loading-text="授权中..."
        class="min-h-[100vh]"
    >
        <div v-if="loading" style="min-height: 100vh;"></div>

        <el-result
            v-if="status === 'success'"
            class="mt-24"
            icon="success"
            :title="scene === 'login' ? '微信登录成功' : '微信绑定成功'"
            sub-title="~ 授权完成您随时可离开此页面 ~"
        />

        <el-result
            v-if="status === 'fail'"
            class="mt-24"
            icon="error"
            :title="scene === 'login' ? '微信登录失败' : '微信绑定失败'"
            :sub-title="error"
        />

        <el-result
            v-if="status === 'unknown'"
            class="mt-24"
            icon="warning"
            title="您好像迷路了"
            sub-title="似乎有一股神秘的力量暂时阻挡了我们的网络之路"
        />
    </view>
</template>

<script setup lang="ts">
import useUserStore from '~/stores/user'
import loginApi from '~/api/login'
import userApi from '~/api/user'

const route = useRoute()
const userStore = useUserStore()

const scene: string = String(route.query.scene || '')
const state: string = String(route.query.state || '')
const code: string = String(route.query.code || '')

const loading = ref(false)
const status = ref('')
const error = ref('')

setTimeout(() => {
    if (status.value === 'ing') {
        status.value = 'unknown'
        loading.value = false
    }
}, 20000)

onMounted(async () => {
    if (state && code) {
        switch (scene) {
            case 'login':
                await loginApi.oaLogin({state, code})
                    .then(async (data: any) => {
                        if (data.token) {
                            status.value = 'success'
                            userStore.login(data.token)
                            await userStore.getUser()
                        }
                    })
                    .catch((e: any) => {
                        status.value = 'fail'
                        error.value = error.value = e.msg
                    })
                    .finally(() => {
                        loading.value = false
                    })
                break
            case 'bind':
                await userApi.bindWechat({state, code})
                    .then(async () => {
                        status.value = 'success'
                        await userStore.getUser()
                    })
                    .catch((e: any) => {
                        status.value = 'fail'
                        error.value = e.msg
                    })
                    .finally(() => {
                        loading.value = false
                    })

        }
    } else {
        status.value = 'unknown'
        loading.value = false
    }
})
</script>