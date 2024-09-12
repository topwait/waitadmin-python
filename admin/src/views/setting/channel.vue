<template>
    <el-form ref="formRef" :model="formData" label-width="150px">
        <!-- 选项卡 -->
        <el-card shadow="never" class="!border-none">
            <el-tabs v-model="currentTab">
                <el-tab-pane
                    :label="item.label"
                    :name="item.value.toString()"
                    v-for="(item, index) in headerList"
                    :key="index"
                />
            </el-tabs>
            <el-alert
                v-if="currentTab === '1'"
                title="微信小程序配置: mp.weixin.qq.com"
                type="warning"
                :closable="false"
                show-icon
            />
            <el-alert
                v-if="currentTab === '2'"
                title="微信公众号配置: mp.weixin.qq.com"
                type="warning"
                :closable="false"
                show-icon
            />
            <el-alert
                v-if="currentTab === '3'"
                title="微信开放平台配置: open.weixin.qq.com"
                type="warning"
                :closable="false"
                show-icon
            />
        </el-card>

        <!-- 微信小程序 -->
        <div v-if="currentTab === '1'">
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">微信小程序</div>
                <el-form-item label="小程序名称" prop="wx.name">
                    <div class="w-80">
                        <el-input v-model="formData.wx.name" placeholder="请输入小程序名称" />
                    </div>
                </el-form-item>
                <el-form-item label="原始ID" prop="wx.original_id">
                    <div class="w-80">
                        <el-input v-model="formData.wx.original_id" placeholder="请输入原始ID" />
                    </div>
                </el-form-item>
                <el-form-item label="二维码" prop="wx.qr_code">
                    <material-picker v-model="formData.wx.qr_code" :limit="1" />
                </el-form-item>
            </el-card>
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">开发者ID</div>
                <el-form-item label="AppID" prop="wx.app_id">
                    <div class="w-80">
                        <el-input v-model="formData.wx.app_id" placeholder="请输入AppID" />
                    </div>
                </el-form-item>
                <el-form-item label="AppSecret" prop="wx.app_secret">
                    <div class="w-80">
                        <el-input v-model="formData.wx.app_secret" placeholder="请输入AppSecret" />
                    </div>
                </el-form-item>
            </el-card>
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">服务器域名</div>
                <el-form-item label="request合法域名" prop="wx.request_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.wx.request_domain" disabled />
                            </div>
                            <el-button v-copy="formData.wx.request_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            小程序账号登录微信公众平台，点击开发>开发设置->服务器域名，填写https协议域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="socket合法域名" prop="wx.socket_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.wx.socket_domain" disabled />
                            </div>
                            <el-button v-copy="formData.wx.socket_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            小程序账号登录微信公众平台，点击开发>开发设置->服务器域名，填写wss协议域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="uploadFile合法域名" prop="wx.upload_file_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.wx.upload_file_domain" disabled />
                            </div>
                            <el-button v-copy="formData.wx.upload_file_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            小程序账号登录微信公众平台，点击开发>开发设置->服务器域名，填写https协议域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="downloadFile合法域名" prop="wx.download_file_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.wx.download_file_domain" disabled />
                            </div>
                            <el-button v-copy="formData.wx.download_file_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            小程序账号登录微信公众平台，点击开发>开发设置->服务器域名，填写https协议域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="udp合法域名" prop="wx.udp_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.wx.udp_domain" disabled />
                            </div>
                            <el-button v-copy="formData.wx.udp_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            小程序账号登录微信公众平台，点击开发>开发设置->服务器域名，填写udp协议域名
                        </div>
                    </div>
                </el-form-item>
            </el-card>
        </div>

        <!-- 微信公众号 -->
        <div v-if="currentTab === '2'">
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">微信公众号</div>
                <el-form-item label="公众号名称" prop="oa.name">
                    <div class="w-80">
                        <el-input v-model="formData.oa.name" placeholder="请输入公众号名称" />
                    </div>
                </el-form-item>
                <el-form-item label="原始ID" prop="oa.original_id">
                    <div class="w-80">
                        <el-input v-model="formData.oa.original_id" placeholder="请输入原始ID" />
                    </div>
                </el-form-item>
                <el-form-item label="二维码" prop="oa.qr_code">
                    <material-picker v-model="formData.oa.qr_code" :limit="1" />
                </el-form-item>
            </el-card>
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">开发者ID</div>
                <el-form-item label="AppID" prop="oa.app_id">
                    <div class="w-80">
                        <el-input v-model="formData.oa.app_id" placeholder="请输入AppID" />
                    </div>
                </el-form-item>
                <el-form-item label="AppSecret" prop="oa.app_secret">
                    <div class="w-80">
                        <el-input v-model="formData.oa.app_secret" placeholder="请输入AppSecret" />
                    </div>
                </el-form-item>
            </el-card>
            <el-card class="!border-none mt-4" shadow="never">
                <div class="font-medium mb-7">服务器配置</div>
                <el-form-item label="URL">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.oa.url" disabled />
                            </div>
                            <el-button v-copy="formData.oa.url">复制</el-button>
                        </div>
                        <div class="form-tips">登录微信公众平台，点击开发>基本配置>服务器配置，填写服务器地址（URL）</div>
                    </div>
                </el-form-item>
                <el-form-item label="Token" prop="Token">
                    <div class="flex-1 min-w-0">
                        <div class="w-80">
                            <el-input v-model="formData.oa.token" placeholder="请输入Token" />
                        </div>
                        <div class="form-tips">
                            登录微信公众平台，点击开发>基本配置>服务器配置，设置令牌Token。不填默认为“wa”
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="EncodingAESKey" prop="oa.encoding_aes_key">
                    <div class="flex-1 min-w-0">
                        <div class="w-80">
                            <el-input
                                v-model="formData.oa.aes_key"
                                placeholder="请输入EncodingAESKey"
                            />
                        </div>
                        <div class="form-tips">消息加密密钥由43位字符组成，字符范围为A-Z,a-z,0-9</div>
                    </div>
                </el-form-item>
                <el-form-item label="消息加密方式" required prop="oa.encryption_type">
                    <div class="flex-1 min-w-0">
                        <el-radio-group
                            class="flex-col !items-start min-w-0"
                            v-model="formData.oa.encryption_type"
                        >
                            <el-radio :value="1">明文模式 (不使用消息体加解密功能，安全系数较低)</el-radio>
                            <el-radio :value="2">兼容模式 (明文、密文将共存，方便开发者调试和维护)</el-radio>
                            <el-radio :value="3">安全模式（推荐） (消息包为纯密文，需要开发者加密和解密，安全系数高)</el-radio>
                        </el-radio-group>
                    </div>
                </el-form-item>
            </el-card>
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">功能设置</div>
                <el-form-item label="request合法域名" prop="oa.wk_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.oa.wk_domain" disabled />
                            </div>
                            <el-button v-copy="formData.oa.wk_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            登录微信公众平台，点击设置>公众号设置>功能设置，填写业务域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="JS接口安全域名" prop="oa.js_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.oa.js_domain" disabled />
                            </div>
                            <el-button v-copy="formData.oa.js_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            登录微信公众平台，点击设置>公众号设置>功能设置，填写JS接口安全域名
                        </div>
                    </div>
                </el-form-item>
                <el-form-item label="网页授权域名" prop="oa.web_domain">
                    <div class="flex-1 min-w-0">
                        <div class="sm:flex">
                            <div class="mr-4 sm:w-80 flex">
                                <el-input v-model="formData.oa.web_domain" disabled />
                            </div>
                            <el-button v-copy="formData.oa.web_domain">复制</el-button>
                        </div>
                        <div class="form-tips">
                            登录微信公众平台，点击设置>公众号设置>功能设置，填写网页授权域名
                        </div>
                    </div>
                </el-form-item>
            </el-card>
        </div>

        <!-- 微信开放平台 -->
        <div v-if="currentTab === '3'">
            <el-card shadow="never" class="!border-none mt-4">
                <div class="font-medium mb-7">开发者ID</div>
                <el-form-item label="AppID" prop="op.app_id">
                    <div class="w-80">
                        <el-input v-model="formData.wx.app_id" placeholder="请输入AppID" />
                    </div>
                </el-form-item>
                <el-form-item label="AppSecret" prop="op.app_secret">
                    <div class="w-80">
                        <el-input v-model="formData.wx.app_secret" placeholder="请输入AppSecret" />
                    </div>
                </el-form-item>
            </el-card>
        </div>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:channel:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import channelApi from '@/api/setting/channel'

const currentTab = ref<string>('1')
const headerList = [
    { value: '1', label: '微信小程序' },
    { value: '2', label: '微信公众号' },
    { value: '3', label: '微信开发平台' }
]

const loading = ref(false)
const formData = reactive({
    // 微信小程序
    wx: {
        name: '',
        original_id: '',
        qr_code: '',
        app_id: '',
        app_secret: '',
        request_domain: '',
        socket_domain: '',
        upload_file_domain: '',
        download_file_domain: '',
        udp_domain: '',
    },
    // 微信公众号
    oa: {
        name: '',
        app_id: '',
        original_id: '',
        qr_code: '',
        app_secret: '',
        url: '',
        token: '',
        aes_key: '',
        encryption_type: 1,
        wk_domain: '',
        js_domain:'',
        web_domain: ''
    },
    // 微信开放平台
    op: {
        app_id: '',
        app_secret: ''
    }
})

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await channelApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    loading.value = true
    await channelApi.save(formData)
        .finally(() => {
            setTimeout(() => {
                loading.value = false
            }, 500)
        })

    await queryConfigs()
    feedback.msgSuccess('保存成功')
}

onMounted(async () => {
    await queryConfigs()
})
</script>
