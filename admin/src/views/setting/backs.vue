<template>
    <el-form ref="formRef" :rules="rules" :model="formData" label-width="120px">
        <!-- 后台设置 -->
        <el-card shadow="never" class="!border-none">
            <div class="text-xl font-medium mb-[20px]">后台设置</div>
            <el-form-item prop="name">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.name"
                        maxlength="30"
                        show-word-limit
                    />

                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='用于后台登录页面名称'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    网站名称
                </template>
            </el-form-item>
            <el-form-item prop="title">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.title"
                        maxlength="30"
                        show-word-limit
                    />

                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='用于后台浏览器的标题'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    网站标题
                </template>
            </el-form-item>
            <el-form-item prop="logo_black_big" required>
                <material-picker tipsBtn="选大图" v-model="formData.logo_black_big" />
                <material-picker tipsBtn="选小图" v-model="formData.logo_black_small" />
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='遇到浅色背景时使用 (大: 180px * 50、 小: 60px * 50px), 支持格式 [ jpg、jpeg、png ]'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    深色logo
                </template>
            </el-form-item>
            <el-form-item prop="logo_white_big" required>
                <material-picker tipsBtn="选大图" v-model="formData.logo_white_big" />
                <material-picker tipsBtn="选小图" v-model="formData.logo_white_small" />
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='遇到浅色背景时使用 (大: 180px * 50、 小: 60px * 50px), 支持格式 [ jpg、jpeg、png ]'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    浅色logo
                </template>
            </el-form-item>
            <el-form-item prop="favicon">
                <material-picker v-model="formData.favicon" />
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='建议尺寸: 64 * 64像素, 支持格式 [ jpg、jpeg、png、ico ]'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    网站图标
                </template>
            </el-form-item>
            <el-form-item prop="cover">
                <material-picker v-model="formData.cover" />
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='建议尺寸: 180 * 50像素, 支持格式 [ jpg、jpeg、png ]'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    登录封面
                </template>
            </el-form-item>
        </el-card>

        <!-- 联系方式 -->
        <el-card shadow="never" class="!border-none mt-4">
            <div class="text-xl font-medium mb-[20px]">联系方式</div>
            <el-form-item label="联系人" prop="pc.name">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.contacts"
                        show-word-limit
                    />
                </div>
            </el-form-item>
            <el-form-item label="手机号码" prop="pc.name">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.mobile"
                        show-word-limit
                    />
                </div>
            </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:backs:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import backsApi from '@/api/setting/backs'

const loading = ref(false)
const formRef = ref()
const formData = reactive({
    // 基础的
    name: '',
    title: '',
    favicon: '',
    cover: '',
    logo_black_big: '',
    logo_black_small: '',
    logo_white_big: '',
    logo_white_small: '',
    // 联系人
    contacts: '',
    mobile: ''
})

// 表单验证
const rules = {
    'name': [
        { required: true, message: '请填写网站名称', trigger: ['blur'] },
        { max: 30, message: '网站名称不能超出30个字符', trigger: ['blur'] },
    ],
    'title': [
        { required: true, message: '请填写网站标题', trigger: ['blur'] },
        { max: 30, message: '网站标题不能超出30个字符', trigger: ['blur'] },
    ],
    'cover': [
        { max: 500, message: '网站封面链接不能超出500个字符', trigger: ['blur'] },
    ],
    'favicon': [
        { required: true, message: '请设置网站图标', trigger: ['blur'] },
        { max: 500, message: '网站图标链接不能超出500个字符', trigger: ['blur'] },
    ],
    'logo_black_big': [
        { required: true, message: '请选择深色logo', trigger: ['blur'] }
    ],
    'logo_white_big': [
        { required: true, message: '请选择浅色', trigger: ['blur'] }
    ],
    'contacts': [
        { max: 20, message: '联系人姓名不能超出20个字符', trigger: ['blur'] },
    ],
    'mobile': [
        { max: 20, message: '联系电话不能超出200个字符', trigger: ['blur'] },
    ]
}

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await backsApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()

    loading.value = true
    await backsApi.save(formData)
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
