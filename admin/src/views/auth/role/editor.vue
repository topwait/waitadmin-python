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
                <el-form-item label="角色名称" prop="name">
                    <el-input
                        v-model="formData.name"
                        placeholder="请输入角色名称"
                        maxlength="20"
                        clearable
                    />
                </el-form-item>
                <el-form-item label="角色描述" prop="describe">
                    <el-input
                        v-model="formData.describe"
                        type="textarea"
                        :autosize="{ minRows: 4, maxRows: 6 }"
                        placeholder="请输入角色描述"
                        maxlength="200"
                        show-word-limit
                    />
                </el-form-item>
                <el-form-item label="角色排序" prop="sort">
                    <el-input-number v-model="formData.sort" :min="0" :max="99999" />
                </el-form-item>
                <el-form-item label="状态" prop="is_disable">
                    <el-radio-group v-model="formData.is_disable">
                        <el-radio :value="0">正常</el-radio>
                        <el-radio :value="1">停用</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="菜单权限">
                    <el-checkbox @change="handleExpand">展开/折叠</el-checkbox>
                    <el-checkbox @change="handleSelectAll">全选/全不选</el-checkbox>
                    <el-checkbox v-model="checkStrictly">父子联动</el-checkbox>
                    <el-tree
                        ref="treeRef"
                        class="tree-border"
                        show-checkbox
                        node-key="id"
                        :data="menuOptions"
                        :check-strictly="!checkStrictly"
                        :props="{
                            label: 'name',
                            children: 'children'
                        }"
                    />
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import type { CheckboxValueType, ElTree, FormInstance } from 'element-plus'
import feedback from '@/utils/feedback'
import authRoleApi from '@/api/auth/role'
import authMenuApi from '@/api/auth/menu'

const emits = defineEmits(['success', 'close'])

const formRef = shallowRef<FormInstance>()
const treeRef = shallowRef<InstanceType<typeof ElTree>>()

const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑角色' : '新增角色'
})

// 菜单数据
const menuOptions = ref<any[]>([])
const checkStrictly = ref(true)

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: 0,         // 角色ID
    name: '',      // 角色名称
    sort: 0,       // 角色排序
    describe: '',  // 角色描述
    is_disable: 0, // 是否禁用:[0=否, 1=是]
    menu_ids: [] as any[]
})

// 表单规则
const formRules = reactive({
    name: [
        { required: true, message: '角色名称不能为空', trigger: 'blur' },
        { min: 2, message: '角色名称不能少于2个字符', trigger: 'blur' },
        { max: 20, message: '角色名称不能大于20个字符', trigger: 'blur' }
    ],
    describe: [
        { max: 200, message: '角色描述不能大于200个字符', trigger: 'blur' }
    ]
})

/**
 * 展开/折叠
 */
const handleExpand = (check: CheckboxValueType) => {
    const treeList = menuOptions.value
    for (let i = 0; i < treeList.length; i++) {
        // @ts-ignore
        treeRef.value.store.nodesMap[treeList[i].id].expanded = check
    }
}

/**
 * 全选/全不选
 */
const handleSelectAll = (check: CheckboxValueType) => {
    if (check) {
        treeRef.value?.setCheckedKeys(menuOptions.value.map((item) => item.id))
    } else {
        treeRef.value?.setCheckedKeys([])
    }
}

/**
 * 获取选中
 */
const getAllCheckedKeys = () => {
    const checkedKeys = treeRef.value?.getCheckedKeys()
    const halfCheckedKeys: any = treeRef.value?.getHalfCheckedKeys()
    checkedKeys?.unshift.apply(checkedKeys, halfCheckedKeys)
    return checkedKeys
}

/**
 * 设置选中
 */
const setAllCheckedKeys = () => {
    formData.menu_ids.forEach((v: any) => {
        nextTick(() => {
            treeRef.value?.setChecked(v, true, false)
        })
    })
}

/**
 * 获取菜单
 */
const getMenuOptions = () => {
    authMenuApi.whole().then((res: any) => {
        menuOptions.value = res
        nextTick(() => {
            setAllCheckedKeys()
        })
    })
}

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    formData.menu_ids = getAllCheckedKeys()!
    loading.value = true
    if (showMode.value === 'edit') {
        await authRoleApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await authRoleApi.add(formData)
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
        const data = await authRoleApi.detail(row.id)
        for (const key in formData) {
            if (data[key] !== null && data[key] !== undefined) {
                formData[key] = data[key]
            }
        }
    }

    getMenuOptions()
}

defineExpose({
    open
})
</script>

<style scoped lang="scss">
.tree-border {
    width: 100%;
    margin-top: 5px;
    background: #ffffff none;
    border: 1px solid #e5e6e7;
    border-radius: 4px;
}
</style>
