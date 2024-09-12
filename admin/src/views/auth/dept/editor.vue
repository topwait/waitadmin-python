<template>
    <popup
        :show="showEdit"
        :title="popTitle"
        :loading="loading"
        :async-close="true"
        width="500px"
        @close="emits('close')"
        @confirm="handleSubmit"
    >
        <div class="p-6 pb-0">
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="80px">
                <el-form-item label="上级部门" prop="pid" v-if="formData.pid !== 0">
                    <el-tree-select
                        class="flex-1"
                        v-model="formData.pid"
                        :data="optionsData.dept"
                        clearable
                        node-key="id"
                        :props="{
                            value: 'id',
                            label: 'name'
                        }"
                        check-strictly
                        :default-expand-all="true"
                        placeholder="请选择上级部门"
                    />
                </el-form-item>
                <el-form-item label="部门名称" prop="name">
                    <el-input v-model="formData.name" placeholder="请输入部门名称" maxlength="20" />
                </el-form-item>
                <el-form-item label="部门电话" prop="mobile">
                    <el-input v-model="formData.mobile" placeholder="请输入部门电话" maxlength="20" />
                </el-form-item>
                <el-form-item label="负责人名" prop="duty">
                    <el-input v-model="formData.duty" placeholder="请输入负责人名" maxlength="20" />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="999999" />
                </el-form-item>
                <el-form-item label="状态" prop="is_disable">
                    <el-radio-group v-model="formData.is_disable">
                        <el-radio :value="0">正常</el-radio>
                        <el-radio :value="1">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import { useDictOptions } from '@/hooks/useOption'
import feedback from '@/utils/feedback'
import authDeptApi from '@/api/auth/dept'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑部门' : '新增部门'
})

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: 0,        // 部门ID
    pid: '',      // 上级ID
    name: '',     // 部门名称
    mobile: '',   // 部门电话
    duty: '',     // 负责人名
    sort: 0,      // 部门排序
    is_disable: 0 // 是否禁用:[0=否, 1=是]
})

// 表单规则
const formRules = reactive({
    pid: [
        { required: true, message: '请选择上级部门', trigger: ['blur'] }
    ],
    name: [
        { required: true, message: '部门名称不能为空', trigger: ['blur'] },
        { max: 100, message: '部门名称不能超出100个字符', trigger: ['blur'] }
    ],
    mobile: [
        { required: true, message: '部门电话不能为空', trigger: ['blur'] },
        { max: 30, message: '部门电话不能超出30个字符', trigger: ['blur'] }
    ],
    duty: [
        { required: true, message: '负责人名称不能为空', trigger: ['blur'] },
        { max: 30, message: '负责人名称不能超出30个字符', trigger: ['blur'] }
    ]
})

// 字典选项
const { optionsData } = useDictOptions<{
    dept: any[]
}>({
    dept: {
        api: authDeptApi.whole
    }
})

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await authDeptApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await authDeptApi.add(formData)
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
        const data = await authDeptApi.detail(row.id)
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
