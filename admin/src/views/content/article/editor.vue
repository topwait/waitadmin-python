<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="860px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="所属类目" prop="cid">
                    <el-select
                        v-model="formData.cid"
                        placeholder="请选择所属类目"
                        clearable
                    >
                        <el-option
                            v-for="(item, index) in optionsData.cate"
                            :key="index"
                            :label="item.name"
                            :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="文章标题" prop="title">
                    <el-input v-model="formData.title" placeholder="请输入部门名称" maxlength="20" />
                </el-form-item>
                <el-form-item label="文章简介" prop="intro">
                    <el-input
                        type="textarea"
                        :rows="4"
                        v-model.trim="formData.intro"
                        show-word-limit
                    />
                </el-form-item>
                <el-form-item label="文章封面" prop="image">
                    <material-picker
                        v-model="formData.image"
                        :limit="1"
                    />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="999999" />
                </el-form-item>
                <el-form-item label="置顶" prop="is_topping">
                    <el-radio-group v-model="formData.is_topping">
                        <el-radio :value="1">是</el-radio>
                        <el-radio :value="0">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="推荐" prop="is_recommend">
                    <el-radio-group v-model="formData.is_recommend">
                        <el-radio :value="1">是</el-radio>
                        <el-radio :value="0">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="状态" prop="is_show">
                    <el-radio-group v-model="formData.is_show">
                        <el-radio :value="1">显示</el-radio>
                        <el-radio :value="0">隐藏</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <rich-text v-model="formData.content" :height="667"  />
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import { useDictOptions } from '@/hooks/useOption'
import feedback from '@/utils/feedback'
import articleCateApi from '@/api/content/category'
import articleApi from '@/api/content/article'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑文章' : '新增文章'
})

// 表单数据
const loading = ref(false)
const formData: any = reactive({
    id: '',          // 文章ID
    cid: '',         // 类目ID
    title: '',       // 标题
    image: '',       // 封面
    intro: '',       // 简介
    content: '',     // 内容
    sort: 0,         // 部门排序
    is_topping: 0,   // 是否置顶:[0=否, 1=是]
    is_recommend: 0, // 是否推荐:[0=否, 1=是]
    is_show: 0       // 是否显示:[0=否, 1=是]
})

// 表单规则
const formRules: any = reactive({
    cid: [
        { required: true, message: '请选择所属类目', trigger: ['blur'] }
    ],
    title: [
        { required: true, message: '文章标题不能为空', trigger: ['blur'] },
        { max: 100, message: '文章标题不能大于100个字符', trigger: ['blur'] }
    ]
})

// 字典选项
const { optionsData } = useDictOptions<{
    cate: any[]
}>({
    cate: {
        api: articleCateApi.whole
    }
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await articleApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await articleApi.add(formData)
            .finally(() => {
                loading.value = false
            })
    }

    feedback.msgSuccess('操作成功')
    emits('close')
    emits('success')
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

    if (type === 'edit') {
        const data = await articleApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
            }
        }
    }
}

defineExpose({
    open
})
</script>
