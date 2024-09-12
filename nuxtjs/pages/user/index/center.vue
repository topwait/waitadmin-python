<template>
    <el-card class="!border-none h-full" shadow="never">
        <el-tabs v-model="tabIndex" type="card" >
            <el-tab-pane label="基本信息" name="introduce" >
                <div class="introduce">
                    <dl>
                        <dt>头像</dt>
                        <dd class="avatar">
                            <upload-cropper-select
                                v-model="userInfo.avatar"
                                @change="setUserInfo(userInfo.avatar, UserFieldEnum.AVATAR)"
                            />
                        </dd>
                    </dl>
                    <dl>
                        <dt>编号</dt>
                        <dd>{{ userInfo.sn }}</dd>
                    </dl>
                    <dl>
                        <dt>账号</dt>
                        <dd>{{ userInfo.account }}</dd>
                    </dl>
                    <dl>
                        <dt>昵称</dt>
                        <dd>
                            {{ userInfo.nickname }}
                            <ClientOnly>
                                <popover-input
                                    class="inline-block"
                                    :limit="30"
                                    :value="userInfo.nickname"
                                    @confirm="setUserInfo($event, UserFieldEnum.NICKNAME)"
                                >
                                    <el-button link>
                                        <Icon name="el-icon-Edit" :size="16" />
                                    </el-button>
                                </popover-input>
                            </ClientOnly>
                        </dd>
                    </dl>
                    <dl>
                        <dt>性别</dt>
                        <dd>
                            {{ GenderOptions.find(option => option.value === userInfo.gender)?.label }}
                            <ClientOnly>
                                <popover-input
                                    class="inline-block"
                                    type="select"
                                    :teleported="false"
                                    :value="userInfo.gender"
                                    :options="GenderOptions"
                                    @confirm="setUserInfo($event, UserFieldEnum.GENDER)"
                                >
                                    <el-button link>
                                        <Icon name="el-icon-Edit" :size="16" />
                                    </el-button>
                                </popover-input>
                            </ClientOnly>
                        </dd>
                    </dl>
                    <dl>
                        <dt>手机号</dt>
                        <dd>{{ userInfo.mobile ? userInfo.mobile : '未绑定' }}</dd>
                    </dl>
                    <dl>
                        <dt>邮箱号</dt>
                        <dd>{{ userInfo.email ? userInfo.email : '未绑定' }}</dd>
                    </dl>
                    <dl>
                        <dt>注册时间</dt>
                        <dd>{{ userInfo.create_time }}</dd>
                    </dl>
                    <dl>
                        <dt>最后登录</dt>
                        <dd>{{ userInfo.last_login_time }}</dd>
                    </dl>
                    <div class="mt-[40px] flex justify-center">
                        <el-button type="primary">退出登录</el-button>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </el-card>
</template>

<script setup lang="ts">
import feedback from '~/utils/feedback'
import useUserStore from '~/stores/user'
import userApi from '~/api/user'

// 字段枚举
enum UserFieldEnum {
    GENDER = 'gender',
    AVATAR = 'avatar',
    NICKNAME = 'nickname'
}

// 性别选项
const GenderOptions = [
    {label: '保密', value: 0},
    {label: '男', value: 1},
    {label: '女', value: 2}
]

// 用户信息
const userStore = useUserStore()
const tabIndex: Ref<string> = ref('introduce')
const userInfo = computed(() => userStore.users)

// 编辑资料
const setUserInfo = async (
    value: string,
    type: UserFieldEnum
): Promise<void> => {
    await userApi.edit({
        field: type,
        value: value
    })
    await userStore.getUser()
    feedback.msgSuccess('修改成功')
}
</script>

<style scoped lang="scss">
:deep(.el-tabs) {
    .el-tabs__item.is-active,
    .el-tabs__item:hover {
        color: var(--el-text-color-regular);
    }
}

.introduce {
    padding: 0 10px;
    dl {
        display: flex;
        align-items: center;
        padding: 18px 0;
        font-size: 14px;
        color: var(--el-text-color-regular);
        border-bottom: 1px solid var(--el-border-color-light);
        dt {
            width: 90px;
            padding-left: 5px;
            font-size: 14px;
            color: var(--el-text-color-regular);
        }
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
                line-height: 30px;
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
    }
}
</style>
