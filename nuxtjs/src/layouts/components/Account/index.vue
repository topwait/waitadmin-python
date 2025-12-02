<template>
    <ClientOnly>
        <ElDialog
            v-model="showLogin"
            append-to-body
            width="auto"
            class="none-padding"
            :close-on-click-modal="false"
        >
            <div class="flex">
                <login v-if="appStore.popupType === popupEnum.LOGIN" />

                <register v-if="appStore.popupType === popupEnum.REGISTER" />

                <forgot-pwd v-if="appStore.popupType === popupEnum.FORGOT_PWD" />

                <change-pwd v-if="appStore.popupType === popupEnum.CHANGE_PWD" />

                <bind-email v-if="appStore.popupType === popupEnum.BIND_EMAIL" />

                <bind-mobile v-if="appStore.popupType === popupEnum.BIND_MOBILE" />

                <bind-wechat v-if="appStore.popupType === popupEnum.BIND_WECHAT" />
            </div>
        </ElDialog>
    </ClientOnly>
</template>

<script setup lang="ts">
import { popupEnum } from '@/enums/app'
import useAppStore from '@/stores/app'
import Register from './register.vue'
import ForgotPwd from './forgot-pwd.vue'
import ChangePwd from './change-pwd.vue'
import BindEmail from './bind-email.vue'
import BindMobile from './bind-mobile.vue'
import BindWechat from './bind-wechat.vue'
import Login from '../login/index.vue'

const appStore = useAppStore()

let showType = appStore.popupType
const showLogin = computed({
    get() {
        showType = appStore.popupType
        return !!appStore.popupType
    },
    set(value) {
        if (value) {
            appStore.popupType = showType
        } else {
            showType = popupEnum.NULL
            appStore.popupType = popupEnum.NULL
        }
    }
})
</script>
