<template>
    <ClientOnly>
        <ElDialog
            v-model="showLogin"
            append-to-body
            width="auto"
            class="none-padding"
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
import { popupEnum } from '~/enums/app'
import useAppStore from '~/stores/app'
import Login from './Login.vue'
import Register from './Register.vue'
import ForgotPwd from './ForgotPwd.vue'
import ChangePwd from './ChangePwd.vue'
import BindEmail from './BindEmail.vue'
import BindMobile from './BindMobile.vue'
import BindWechat from './BindWechat.vue'

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
