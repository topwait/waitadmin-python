<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :async-close="true"
        width="900px"
        @close="emits('close')"
    >
        <div class="p-6 pb-0">
            <el-tabs type="border-card" v-model="currTabPane">
                <!-- 基础信息 -->
                <el-tab-pane name="intros" label="基础信息" class="min-h-[542px]">
                    <!-- 账户 -->
                    <div class="flex justify-center pb-4">
                        <div class="flex items-center mr-4">
                            <el-avatar :src="formData.avatar" :size="60" />
                        </div>
                        <div class="instruments">
                            <div class="panel-item">
                                <em>钱包</em>
                                <div class="flex items-center text-[16px]">
                                    <span class="text-sm">¥</span>{{ formData.balance }}
                                    <el-button
                                        v-perms="['user.user/adjustAccount']"
                                        type="primary"
                                        link
                                        @click="adjustState = true"
                                    >
                                        调整
                                    </el-button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- 操作 -->
                    <el-divider content-position="left">基础操作</el-divider>
                    <div class="py-2">
                        <el-button type="primary" @click="pwdPopState = true">重置密码</el-button>
                        <el-button type="danger" @click="handleKickOut('all')">清退登录</el-button>
                    </div>
                    <!-- 资料 -->
                    <el-divider content-position="left">基础信息</el-divider>
                    <div class="information">
                        <dl>
                            <dt>用户编号：</dt>
                            <dd>{{ formData.sn }}</dd>
                        </dl>
                        <dl>
                            <dt>登录账号：</dt>
                            <dd>
                                {{ formData.account }}
                                <popover-input
                                    class="ml-[5px]"
                                    :limit="32"
                                    :value="formData.account"
                                    @confirm="handleEdit($event, 'account')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>用户昵称：</dt>
                            <dd>
                                {{ formData.nickname }}
                                <popover-input
                                    class="ml-[5px]"
                                    :limit="32"
                                    :value="formData.nickname"
                                    @confirm="handleEdit($event, 'nickname')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>联系电话：</dt>
                            <dd>
                                {{ formData.mobile || '未绑定' }}
                                <popover-input
                                    class="ml-[5px]"
                                    :value="formData.mobile"
                                    @confirm="handleEdit($event, 'mobile')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>用户性别：</dt>
                            <dd>
                                {{ formData.gender || '未知' }}
                                <popover-input
                                    class="ml-[5px]"
                                    type="select"
                                    :value="formData.gender"
                                    :options="[
                                        {
                                            label: '未知',
                                            value: 0
                                        },
                                        {
                                            label: '男',
                                            value: 1
                                        },
                                        {
                                            label: '女',
                                            value: 2
                                        }
                                    ]"
                                    @confirm="handleEdit($event, 'gender')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>电子邮箱：</dt>
                            <dd>
                                {{ formData.email || '未绑定' }}
                                <popover-input
                                    class="ml-[5px]"
                                    :value="formData.email"
                                    @confirm="handleEdit($event, 'email')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>用户分组：</dt>
                            <dd>
                                {{ formData.group || '未设置' }}
                                <popover-input
                                    class="ml-[5px]"
                                    type="select"
                                    :options="[]"
                                    @confirm="handleEdit($event, 'group')"
                                    v-perms="['users:user:edit']"
                                >
                                    <el-button type="primary" link>
                                        <icon name="el-icon-EditPen" />
                                    </el-button>
                                </popover-input>
                            </dd>
                        </dl>
                        <dl>
                            <dt>是否禁用：</dt>
                            <dd>
                                <el-tag
                                    :type="formData.is_disable ? 'warning' : 'success'"
                                    @click="handleBlacklist()"
                                    class="cursor-pointer"
                                >
                                    {{ formData.is_disable ? '已禁用' : '正常' }}
                                </el-tag>
                            </dd>
                        </dl>
                        <dl>
                            <dt>最后登录IP：</dt>
                            <dd>{{ formData.last_login_ip }}</dd>
                        </dl>
                        <dl>
                            <dt>注册时间：</dt>
                            <dd>{{ formData.create_time }}</dd>
                        </dl>
                        <dl>
                            <dt>最后登录时间：</dt>
                            <dd>{{ formData.last_login_time }}</dd>
                        </dl>
                    </div>
                </el-tab-pane>

                <!-- 登录信息 -->
                <el-tab-pane name="session" label="登录信息" class="min-h-[542px]">
                    <div class="pb-3">
                        <el-button plain @click="handleRefreshTable()">
                            <icon name="el-icon-Refresh" size="16" />
                        </el-button>
                    </div>
                    <el-table v-loading="sessionPager.loading" :data="sessionPager.lists" stripe>
                        <el-table-column prop="uuid" label="编号">
                            <template #default="{ row }">
                                <el-tooltip
                                    class="box-item"
                                    effect="dark"
                                    :content="row.uuid"
                                    placement="top-start"
                                >
                                    <p class="line-clamp-1">{{ row?.uuid }}</p>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="device" label="终端" width="120" />
                        <el-table-column prop="tips" label="状态" width="90">
                            <template #default="{ row }">
                                <el-tooltip placement="top">
                                    <template #content>
                                        <p>最后操作UA：{{ row?.last_ua_browser }}</p>
                                        <p>最后操作IP：{{ row?.last_ip_address }}</p>
                                        <p>最后操作时间：{{ row?.last_op_time }}</p>
                                        <p>令牌创建时间：{{ row?.create_time }}</p>
                                    </template>
                                    <div class="cursor-pointer">
                                        <el-tag v-if="row.status === 1" type="success">{{ row?.tips }}</el-tag>
                                        <el-tag v-if="row.status === 2" type="danger">{{ row?.tips }}</el-tag>
                                        <el-tag v-if="row.status === 3" type="warning">{{ row?.tips }}</el-tag>
                                    </div>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="login_host" label="登录IP" width="125" />
                        <el-table-column prop="expire_time" label="有效时间" width="175" />
                        <el-table-column label="操作" width="80" fixed="right">
                            <template #default="{ row }">
                                <el-button type="primary" link @click="handleKickOut(row.uuid)">强退</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div v-if="sessionPager.lists.length > 0" class="flex justify-end mt-4">
                        <paging
                            v-model="sessionPager"
                            @change="sessionLists"
                            :page-sizes="[10, 20, 30, 40]"
                            :small="true"
                        />
                    </div>
                </el-tab-pane>

                <!-- 账户日志 -->
                <el-tab-pane name="wallets" label="账户日志" class="min-h-[542px]">
                    <div class="pb-3">
                        <el-button plain @click="handleRefreshTable()">
                            <icon name="el-icon-Refresh" size="16"/>
                        </el-button>
                    </div>
                    <el-table v-loading="walletsPager.loading" :data="walletsPager.lists" stripe>
                        <el-table-column prop="log_sn" label="编号" />
                        <el-table-column prop="change_amount" label="变动数" width="120">
                            <template #default="{ row }">
                                <span v-if="row.action === 1" class="text-success">+{{ row?.change_amount }}</span>
                                <span v-if="row.action === 2" class="text-error">-{{ row?.change_amount }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="before_amount" label="变动前" width="120" />
                        <el-table-column prop="after_amount" label="变动后" width="120" />
                        <el-table-column prop="tips" label="来源类型" width="180">
                            <template #default="{ row }">
                                <el-tooltip placement="top">
                                    <template #content>
                                        <p>后台操作：{{ row?.op_user || '-' }}</p>
                                        <p>来源单号：{{ row?.source_sn || '-' }}</p>
                                        <p>记录时间：{{ row?.create_time || '-' }}</p>
                                    </template>
                                    <el-tag effect="plain" type="info" class="cursor-pointer">
                                        {{ row?.source_type || '无'}}
                                    </el-tag>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div v-if="walletsPager.lists.length > 0" class="flex justify-end mt-4">
                        <paging
                            v-model="walletsPager"
                            @change="walletsLists"
                            :page-sizes="[10, 20, 30, 40]"
                            :small="true"
                        />
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>

        <adjust-balance
            v-if="adjustState"
            :user_id="formData.id"
            :value="formData.balance"
            @close="adjustState = false"
            @success="handleAdjustBalance()"
        />

        <reset-password
            v-if="pwdPopState"
            :user_id="formData.id"
            @close="pwdPopState = false"
            @success="sessionResetPaging()"
        />
    </popup>
</template>

<script setup lang="ts">
import { usePaging } from '@/hooks/usePaging'
import feedback from '@/utils/feedback'
import userApi from '@/api/users/user'
import AdjustBalance from '../components/adjust-balance.vue'
import ResetPassword from '../components/reset-password.vue'

const emits = defineEmits(['success', 'close'])

const showMode = ref<string>('detail')
const showEdit = ref<boolean>(false)
const popTitle = '用户详情'

// 表单数据
const formData = reactive({
    id: 0,               // 用户ID
    sn: '',              // 用户编号
    account: '',         // 登录账号
    nickname: '',        // 用户昵称
    group: '',           // 用户分组
    avatar: '',          // 用户头像
    gender: '',          // 用户性别
    mobile: '',          // 联系电话
    email: '',           // 电子邮箱
    balance: 0,          // 钱包余额
    is_disable: 0,       // 是否禁用: [0=否, 1=是]
    last_login_ip: '',   // 最后登录IP
    last_login_time: '', // 最后登录时间
    create_time: '',     // 用户注册时间
})

// 当前数据面板
const currTabPane = ref('intros')

// 密码重置弹窗
const pwdPopState = ref(false)

// 余额调整弹窗
const adjustState = ref(false)

// 会话列表
const sessionQueryParams = reactive({user_id: 0})
const {
    pager: sessionPager,
    queryLists: sessionLists,
    resetPaging: sessionResetPaging
} = usePaging({
    fetchFun: userApi.sessions,
    params: sessionQueryParams,
    size: 10
})

// 账户日志
const walletsQueryParams = reactive({user_id: 0})
const {
    pager: walletsPager,
    queryLists: walletsLists,
    resetPaging: walletsResetPaging
} = usePaging({
    fetchFun: userApi.walletLogs,
    params: walletsQueryParams,
    size: 10
})

/**
 * 查询详情
 *
 * @param {number} id
 * @returns {Promise<void>}
 */
const queryDetail = async (id: number): Promise<void> => {
    const data = await userApi.detail(id)
    for (const key in formData) {
        if (data[key] !== null && data[key] !== undefined) {
            // @ts-ignore
            formData[key] = data[key]
        }
    }
}

/**
 * 编辑信息
 *
 * @param {string} value
 * @param {string} field
 * @returns {Promise<void>}
 */
const handleEdit = async (value: string, field: string): Promise<void> => {
    try {
        await userApi.edit(formData.id, field, value)
        await queryDetail(formData.id)
    } catch {}
}

/**
 * 拉黑名单
 */
const handleBlacklist = async () => {
    let messages = '您确定要禁用该用户吗? 禁用后该用户将会被限制登录。'
    if (formData.is_disable === 1) {
        messages = '您确定要解除禁用吗? 解除后该用户将恢复登录功能。'
    }
    await feedback.confirm(messages)
        .then(async () => {
            await userApi.blacklist(formData.id)
            await queryDetail(formData.id)
            await sessionResetPaging()
            feedback.msgSuccess(
                formData.is_disable === 0
                    ? '恢复成功'
                    : '禁用成功'
            )
        }).catch(() => {})
}

/**
 * 强制退出
 *
 * @param uuid
 * @returns {Promise<void>}
 */
const handleKickOut = async (uuid: string): Promise<void> => {
    let messages = `您确定要强退该登录吗? (${uuid})`
    if (uuid === 'all') {
        messages = '您确定要清退所有登录吗?'
    }
    await feedback.confirm(messages).then(async () => {
        await userApi.kickOut(formData.id, uuid)
        await sessionResetPaging()
        feedback.msgSuccess('操作成功')
    }).catch(() => {})
}

/**
 * 调整账户
 */
const handleAdjustBalance = async () => {
    await queryDetail(formData.id)
    await walletsResetPaging()
}

/**
 * 刷新表格
 */
const handleRefreshTable = async () => {
    switch (currTabPane.value) {
        case 'session':
            await sessionResetPaging()
            break
        case 'wallets':
            await walletsResetPaging()
    }
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

    if (type === 'detail') {
        sessionQueryParams.user_id = row.id
        walletsQueryParams.user_id = row.id
        await queryDetail(row.id)
        await sessionLists()
        await walletsLists()
    }
}

defineExpose({
    open
})
</script>

<style scoped lang="scss">
.information {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
    dl {
        display: flex;
        width: 50%;
        padding: 8px 0;
        dd {
            display: flex;
            align-content: center;
        }
    }
}

.instruments {
    display: flex;
    width: 100%;
    padding: 10px;
    border: 1px #dddddd dashed;
    border-radius: 8px;
    .panel-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 33.33%;
        padding: 12px 0;
        margin-right: 10px;
        font-weight: 500;
        background-color: var(--el-bg-color-page);
        border-radius: 8px;
        em {
            margin-bottom: 5px;
            font-size: 16px;
            font-style: normal;
            font-weight: 600;
        }
    }
}
</style>
