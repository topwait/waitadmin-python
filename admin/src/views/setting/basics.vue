<template>
    <el-form ref="formRef" :rules="rules" :model="formData" label-width="120px">
        <!-- 基础设置 -->
        <el-card shadow="never" class="!border-none">
            <div class="text-xl font-medium mb-[20px]">基础设置</div>
            <el-form-item label="版权信息" prop="website.copyright">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.website.copyright"
                        show-word-limit
                    />
                </div>
            </el-form-item>
            <el-form-item label="ICP备案" prop="website.icp">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.website.icp"
                        show-word-limit
                    />
                </div>
            </el-form-item>
            <el-form-item label="公安备案" prop="website.pcp">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.website.pcp"
                        show-word-limit
                    />
                </div>
            </el-form-item>
            <el-form-item label="统计代码" prop="website.analyse">
                <div class="w-[380px]">
                    <el-input
                        type="textarea"
                        :rows="5"
                        v-model.trim="formData.website.analyse"
                        show-word-limit
                        placeholder="https://hm.baidu.com/hm.js?d16da1a2f..."
                    />
                </div>
            </el-form-item>
        </el-card>

        <!-- 电脑端设置 -->
        <el-card shadow="never" class="!border-none mt-4">
            <div class="text-xl font-medium mb-[20px]">电脑端设置</div>
            <el-form-item prop="pc.logo">
                <material-picker v-model="formData.pc.logo" />
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
            <el-form-item prop="pc.favicon">
                <material-picker v-model="formData.pc.favicon" />
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
            <el-form-item prop="pc.name">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.pc.name"
                        show-word-limit
                    />
                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='多数情况下用于顶部导航条左侧展示'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    网站名称
                </template>
            </el-form-item>
            <el-form-item prop="pc.title">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.pc.title"
                        show-word-limit
                    />
                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='Title: 一般不超过80个字符'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    网站标题
                </template>
            </el-form-item>
            <el-form-item prop="pc.keywords">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.pc.keywords"
                        show-word-limit
                    />
                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='KeyWords: 一般不超过100个字符'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    关键词组
                </template>
            </el-form-item>
            <el-form-item prop="pc.description">
                <div class="w-[380px]">
                    <el-input
                        type="textarea"
                        :rows="5"
                        v-model.trim="formData.pc.description"
                        show-word-limit
                    />
                </div>
                <template v-slot:label>
                    <el-tooltip
                        placement="right"
                        content='Description: 一般不超过200个字符'
                    >
                        <icon name="el-icon-question-filled" class="mr-1" />
                    </el-tooltip>
                    描述信息
                </template>
            </el-form-item>
        </el-card>

        <!-- H5端设置 -->
        <el-card shadow="never" class="!border-none mt-4" style="display: none;">
            <div class="text-xl font-medium mb-[20px]">H5端设置</div>
            <el-form-item label="H5端logo" prop="h5.logo">
                <material-picker v-model="formData.h5.logo" />
            </el-form-item>
            <el-form-item label="H5端标题" prop="h5.title">
                <div class="w-[380px]">
                    <el-input
                        v-model.trim="formData.h5.title"
                        show-word-limit
                    />
                </div>
            </el-form-item>
            <el-form-item label="渠道状态" prop="h5.status">
                <div class="w-[380px]">
                    <el-radio-group v-model="formData.h5.status">
                        <el-radio :value="0">开启</el-radio>
                        <el-radio :value="1">关闭</el-radio>
                    </el-radio-group>
                </div>
            </el-form-item>
            <el-form-item label="关闭访问" prop="h5.close_url" v-if="formData.h5.status === 1">
                <div class="w-80">
                    <el-input v-model="formData.h5.close_url" placeholder="请输入自定义链接" />
                </div>
            </el-form-item>
        </el-card>

        <!-- 保存按钮 -->
        <el-card shadow="never" class="!border-none mt-4">
            <el-button
                v-perms="['setting:basics:save']"
                :loading="loading"
                type="primary"
                @click="handleSubmit"
            >保存配置</el-button>
        </el-card>
    </el-form>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import basicsApi from '@/api/setting/basics'

const loading = ref(false)
const formRef = ref()
const formData = reactive({
    website: {
        icp: '',
        pcp: '',
        analyse: '',
        copyright: ''
    },
    h5: {
        title: '',
        logo: '',
        status: 0,
        close_url: ''
    },
    pc: {
        favicon: '',
        logo: '',
        name: '',
        title: '',
        keywords: '',
        description: '',
    }
})

// 表单验证
const rules = {
    // Base
    'website.icp': [
        { max: 500, message: 'ICP备案不能超出500个字符', trigger: ['blur'] },
    ],
    'website.pcp': [
        { max: 500, message: '公安备案不能超出500个字符', trigger: ['blur'] },
    ],
    // H5
    'h5.title': [
        { max: 200, message: 'H5端标题不能超出200个字符', trigger: ['blur'] },
    ],
    'h5.close_url': [
        { max: 500, message: 'H5端关闭访问地址不能超出500个字符', trigger: ['blur'] },
    ],
    // PC
    'pc.name': [
        { max: 200, message: '网站名称不能超出200个字符', trigger: ['blur'] },
    ],
    'pc.title': [
        { max: 200, message: '网站标题不能超出200个字符', trigger: ['blur'] },
    ],
    'pc.keyword': [
        { max: 200, message: '网站关键词不能超出200个字符', trigger: ['blur'] },
    ],
    'pc.description': [
        { max: 500, message: '网站描述不能超出500个字符', trigger: ['blur'] },
    ]
}

/**
 * 查询配置参数
 */
const queryConfigs = async (): Promise<void> => {
    const data = await basicsApi.detail()
    Object.assign(formData, data)
}

/**
 * 提交修改参数
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()

    loading.value = true
    await basicsApi.save(formData)
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
