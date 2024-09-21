<template>
    <el-card class="!border-none h-full" shadow="never">
        <el-tabs v-model="tabIndex" type="card">
            <el-tab-pane :label="'账号安全'" name="safer">
                <ul class="binding">
                    <!-- 邮箱 -->
                    <li>
                        <div class="icon">
                            <icon name="el-icon-Postcard" size="22" />
                        </div>
                        <div class="info">
                            <p>
                                <span>邮箱  </span>
                                <em v-if=userInfo.email>{{ userInfo.email }}</em>
                                <em v-else class="text-[red]">未绑定</em>
                            </p>
                            <p>邮箱号用于接收网站重要的信息通知</p>
                        </div>
                        <el-button round @click="handlePopShow(popupEnum.BIND_EMAIL)">
                            {{ userInfo.email ? '更改' : '绑定'}}
                        </el-button>
                    </li>
                    <!-- 手机 -->
                    <li>
                        <div class="icon">
                            <icon name="el-icon-Iphone" size="22" />
                        </div>
                        <div class="info">
                            <p>
                                <span>手机  </span>
                                <em v-if=userInfo.mobile>{{ userInfo.mobile }}</em>
                                <em v-else class="text-[red]">未绑定</em>
                            </p>
                            <p>手机号可用于登录或者密码找回等</p>
                        </div>
                        <el-button round @click="handlePopShow(popupEnum.BIND_MOBILE)">
                            {{ userInfo.mobile ? '更改' : '绑定'}}
                        </el-button>
                    </li>
                    <!-- 密码 -->
                    <li>
                        <div class="icon">
                            <icon name="el-icon-Lock" size="22" />
                        </div>
                        <div class="info">
                            <p>
                                <span>密码  </span>
                                <em v-if=userInfo.is_password>********</em>
                                <em v-else class="text-[red]">未设置</em>
                            </p>
                            <p>密码很重要请谨慎保管不要泄露</p>
                        </div>
                        <el-button round @click="handlePopShow(popupEnum.CHANGE_PWD)">
                            {{ userInfo.is_password ? '更改' : '设置'}}
                        </el-button>
                    </li>
                    <!-- 微信 -->
                    <li>
                        <div class="icon">
                            <icon name="el-icon-CoffeeCup" size="22" />
                        </div>
                        <div class="info">
                            <p>
                                <span>微信  </span>
                                <em v-if="userInfo.is_wechat">已绑定</em>
                                <em v-else class="text-[red]">未绑定</em>
                            </p>
                            <p>绑定后可使用微信扫码快速登录</p>
                        </div>
                        <el-button round @click="handlePopShow(popupEnum.BIND_WECHAT)">
                            {{ userInfo.is_wechat ? '更改' : '绑定'}}
                        </el-button>
                    </li>
                </ul>
            </el-tab-pane>
        </el-tabs>
    </el-card>
</template>

<script setup lang="ts">
import { popupEnum } from '~/enums/app'
import useAppStore from '~/stores/app'
import useUserStore from '~/stores/user'

const appStore = useAppStore()
const userStore = useUserStore()

// 页面状态
const tabIndex: Ref<string> = ref('safer')

// 用户信息
const userInfo = computed(() => userStore.users)

/**
 * 弹窗显示
 */
const handlePopShow = (type: popupEnum) => {
    appStore.setPopup(type)
}
</script>

<style scoped lang="scss">
:deep(.el-tabs) {
    .el-tabs__item.is-active,
    .el-tabs__item:hover {
        color: var(--el-text-color-regular);
    }
}

.binding {
    li { box-sizing: border-box;
        display: flex;
        align-items: center;
        height: 98px;
        border-bottom: 1px solid var(--el-border-color-light);;
        .icon {
            width: 50px;
            height: 100%;
            padding-top: 34px;
            margin-left: 15px;
            .el-icon {
                width: 22px;
                height: 22px;
                padding: 2px;
                margin: 0 auto;
                color: #b5b6b7;
                background: var(--el-bg-color-overlay);
                border: 1px solid var(--el-border-color-light);
                border-radius: 50px;
            }
        }
        .info {
            flex: 1;
            padding-top: 20px;
            font-size: 14px;
            color: var(--el-text-color-secondary);
            p {
                height: 30px;
                line-height: 30px;
                em {
                    font-style: normal;
                }
                span {
                    font-weight: bold;
                    color: var(--el-text-color-regular);
                }
            }
        }
    }
}
</style>