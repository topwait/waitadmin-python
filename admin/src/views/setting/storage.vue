<template>
    <el-form ref="formRef" :model="formData" label-width="160px">
        <el-card shadow="never" class="!border-none">
            <div class="text-xl font-medium mb-[20px]">存储设置</div>
            <el-form-item label="存储方式：" prop="drive">
                <el-radio-group v-model="formData.drive">
                    <el-radio value="local">本地存储</el-radio>
                    <el-radio value="qiniu">七牛云存储</el-radio>
                    <el-radio value="aliyun">阿里云OSS</el-radio>
                    <el-radio value="qcloud">腾讯云COS</el-radio>
                </el-radio-group>
            </el-form-item>
            <div v-show="formData.drive === 'qiniu'" class="qiniu">
                <el-form-item label="存储空间名称 Bucket：" prop="qiniu.bucket">
                    <div class="w-80">
                        <el-input v-model="formData.qiniu.bucket" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="ACCESS_KEY AK：" prop="qiniu.access_key">
                    <div class="w-80">
                        <el-input v-model="formData.qiniu.access_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="SECRET_KEY SK：" prop="qiniu.secret_key">
                    <div class="w-80">
                        <el-input v-model="formData.qiniu.secret_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="空间域名 Domain：" prop="qiniu.domain">
                    <div class="w-80">
                        <el-input v-model="formData.qiniu.domain" clearable />
                    </div>
                </el-form-item>
            </div>

            <div v-show="formData.drive === 'aliyun'" class="aliyun">
                <el-form-item label="存储空间名称 Bucket：" prop="aliyun.bucket">
                    <div class="w-80">
                        <el-input v-model="formData.aliyun.bucket" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="AccessKeyId：" prop="aliyun.access_key">
                    <div class="w-80">
                        <el-input v-model="formData.aliyun.access_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="AccessKeySecret：" prop="qiniu.secret_key">
                    <div class="w-80">
                        <el-input v-model="formData.aliyun.secret_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="空间域名 Domain：" prop="aliyun.domain">
                    <div class="w-80">
                        <el-input v-model="formData.aliyun.domain" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="空间地区 Region：" prop="aliyun.region">
                    <div class="w-80">
                        <el-input v-model="formData.aliyun.region" clearable />
                    </div>
                </el-form-item>
            </div>

            <div v-show="formData.drive === 'qcloud'" class="qcloud">
                <el-form-item label="存储空间名称 Bucket：" prop="qcloud.bucket">
                    <div class="w-80">
                        <el-input v-model="formData.qcloud.bucket" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="SecretId：" prop="qcloud.access_key">
                    <div class="w-80">
                        <el-input v-model="formData.qcloud.access_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="SecretKey：" prop="qcloud_sk">
                    <div class="w-80">
                        <el-input v-model="formData.qcloud.secret_key" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="空间域名 Domain：" prop="qcloud.domain">
                    <div class="w-80">
                        <el-input v-model="formData.qcloud.domain" clearable />
                    </div>
                </el-form-item>
                <el-form-item label="空间地区 Region：" prop="qcloud.region">
                    <div class="w-80">
                        <el-input v-model="formData.qcloud.region" clearable />
                    </div>
                </el-form-item>
            </div>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:storage:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import storageApi from '@/api/setting/storage'

const loading = ref(false)
const formData = reactive({
    drive: 'local',
    qiniu: {
        bucket: '',
        domain: '',
        access_key: '',
        secret_key: ''
    },
    aliyun: {
        bucket: '',
        domain: '',
        access_key: '',
        secret_key: '',
        region: ''
    },
    qcloud: {
        bucket: '',
        domain: '',
        access_key: '',
        secret_key: '',
        region: ''
    }
})

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await storageApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    loading.value = true
    await storageApi.save(formData)
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
