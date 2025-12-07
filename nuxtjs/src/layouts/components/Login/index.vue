<template>
    <div class="w-[390px]">
        <!--【账号】-->
        <template v-if="loginScene === 'am'">
            <!-- 账号登录 -->
            <login-routine :protocol="checked" />
            <!-- 更多登录 -->
            <div v-if="usableChannel.includes('wx')" class="oauth">
                <el-divider>其它方式登录</el-divider>
                <div class="flex justify-center my-[30px]">
                    <icon
                        name="svg-icon-Wechat"
                        size="42"
                        color="#00c800"
                        class="mx-10 cursor-pointer"
                        @click="currentLogin = 'wx'"
                    />
                </div>
            </div>
        </template>

        <!--【微信】-->
        <template v-if="loginScene === 'wx'">
            <!-- 微信登录 -->
            <login-wechat :protocol="checked" />
            <div v-if="isSupportAccount" class="oauth">
                <div class="flex justify-center items-center text-primary hover:opacity-80">
                    <icon name="el-icon-Iphone" size="18" />
                    <div class="button" @click="currentLogin = usableChannel[0] || ''">
                        <span class="ml-[6px] cursor-pointer">账号登录</span>
                    </div>
                </div>
            </div>
        </template>

        <!-- 登录关闭 -->
        <el-empty
            v-if="loginScene === 'close'"
            description="登录服务暂停"
            :image-size="200"
        />

        <!-- 授权协议 -->
        <div v-if="isAgreement" class="protocol">
            <el-checkbox v-model="checked" size="large" />
            <span class="ml-1.5">您登录或注册即同意</span>
            <nuxt-link
                v-slot="{ href }"
                :to="`/policy/${policyEnum.SERVICE}`"
                custom
            >
                <a
                    :href="href"
                    target="_blank"
                    class="text-tx-regular cursor-pointer hover:opacity-80"
                >
                    《用户协议》
                </a>
            </nuxt-link>和
            <nuxt-link
                v-slot="{ href }"
                :to="`/policy/${policyEnum.PRIVACY}`"
                custom
            >
                <a
                    :href="href"
                    target="_blank"
                    class="text-tx-regular cursor-pointer hover:opacity-80"
                >
                    《隐私政策》
                </a>
            </nuxt-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import { policyEnum } from '@/enums/app'
import LoginWechat from './LoginWechat.vue'
import LoginRoutine from './LoginRoutine.vue'
import useAppStore from '@/stores/app'

const appStore = useAppStore()

// 登录配置参数
const config = appStore.getLoginConfig.pc

// 是否同意协议
const checked = ref<boolean>(!config?.is_agreement)

// 显示授权协议
const isAgreement = ref<boolean>(config?.is_agreement)

// 当前登录方式
const currentLogin = ref<string>(config?.default_method)

// 可用登录渠道
const usableChannel = ref<string[]>(config?.usable_channel)

// 当前登录场景
const loginScene = computed<string>(() => {
    const val: string  = currentLogin.value
    if (!usableChannel.value.length) {
        return 'close'
    } else if (['account', 'mobile'].includes(val)) {
        return 'am'
    } else if (val === 'wx') {
        return 'wx'
    }
    return ''
})

// 是否支持账号登录
const isSupportAccount = computed<boolean>(() => {
    return usableChannel.value.includes('account')
        || usableChannel.value.includes('mobile')
})
</script>

<style scoped lang="scss">
// 更多登录样式
.oauth {
    padding: 0 25px;
    :deep(.el-divider__text.is-center) {
        font-size: 12px;
        color: var(--el-text-color-secondary);
    }
}

// 授权协议样式
.protocol {
    display: flex;
    align-items: center;
    padding-left: 15px;
    margin-top: 20px;
    font-size: 13px;
    color: var(--el-text-color-secondary);
    background-color: var(--el-bg-color-page);
    border-radius: 4px;
}
</style>
