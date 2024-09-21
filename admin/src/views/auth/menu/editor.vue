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
            <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
                <el-form-item label="菜单类型" prop="type" required>
                    <el-radio-group v-model="formData.type">
                        <el-radio value="M">目录</el-radio>
                        <el-radio value="C">菜单</el-radio>
                        <el-radio value="A">按钮</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="父级菜单" prop="pid" label-width="100px">
                    <el-tree-select
                        class="flex-1"
                        v-model="formData.pid"
                        :data="menuOptions"
                        clearable
                        node-key="id"
                        :props="{
                            label: 'name'
                        }"
                        :default-expand-all="true"
                        placeholder="请选择父级菜单"
                        check-strictly
                    />
                </el-form-item>
                <el-form-item label="菜单名称" prop="name" label-width="100px">
                    <el-input v-model="formData.name" placeholder="请输入菜单名称" clearable />
                </el-form-item>
                <el-form-item v-if="formData.type !== 'A'" label="菜单图标" prop="icon">
                    <icon-picker class="flex-1" v-model="formData.icon" />
                </el-form-item>
                <el-form-item v-if="formData.type !== 'A'" prop="path" label-width="100px">
                    <el-input
                        v-model="formData.path"
                        placeholder="请输入路由地址"
                        clearable
                    />
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='访问的路由地址，如：`user`，如外网地址需内链访问则以`http(s)://`开头'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        路由地址
                    </template>
                </el-form-item>
                <el-form-item v-if="formData.type === 'C'" prop="component" label-width="100px">
                    <el-autocomplete
                        class="w-full"
                        v-model="formData.component"
                        :fetch-suggestions="querySearch"
                        clearable
                        placeholder="请输入组件路径"
                    />
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content="访问的组件路径，如：`system/user/index`，默认在`views`目录下"
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        组件路径
                    </template>
                </el-form-item>
                <el-form-item v-if="formData.type === 'C'" prop="params" label-width="100px">
                    <el-input v-model="formData.params" placeholder="请输入路由参数" clearable />
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='访问路由的默认传递参数，如：`{"id": 1, "name": "wa"}`'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        路由参数
                    </template>
                </el-form-item>
                <el-form-item v-if="formData.type !== 'M'" prop="perms" label-width="100px">
                    <el-input v-model="formData.perms" placeholder="请输入权限字符" clearable />
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='访问API接口的权限字符，如：system:user:list'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        权限字符
                    </template>
                </el-form-item>
                <el-form-item prop="sort" label-width="100px">
                    <el-input-number v-model="formData.sort" :min="0" :max="9999" />
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='数字越大顺序越靠前'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        菜单排序
                    </template>
                </el-form-item>
                <el-form-item v-if="formData.type !== 'A'" prop="is_show" label-width="100px">
                    <el-radio-group v-model="formData.is_show">
                        <el-radio :value="1">显示</el-radio>
                        <el-radio :value="0">隐藏</el-radio>
                    </el-radio-group>
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='选择隐藏则路由将不会出现在侧边栏，但仍然可以访问'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        是否显示
                    </template>
                </el-form-item>
                <el-form-item label="菜单状态" label-width="100px">
                    <el-radio-group v-model="formData.is_disable">
                        <el-radio :value="0">正常</el-radio>
                        <el-radio :value="1">停用</el-radio>
                    </el-radio-group>
                    <template v-slot:label>
                        <el-tooltip
                            placement="top"
                            content='选择停用则路由将不会出现在侧边栏，也不能被访问'
                        >
                            <icon name="el-icon-question-filled" class="mr-1" />
                        </el-tooltip>
                        菜单状态
                    </template>
                </el-form-item>
            </el-form>
        </div>
    </popup>
</template>

<script setup lang="ts">
import { getModulesKey } from '@/router'
import feedback from '@/utils/feedback'
import toolsUtil from '@/utils/tools'
import authMenuApi from '@/api/auth/menu'

const emits = defineEmits(['success', 'close'])

const formRef = ref()
const showMode = ref<string>('add')
const showEdit = ref<boolean>(false)
const popTitle = computed<string>(() => {
    return showMode.value === 'edit' ? '编辑菜单' : '新增菜单'
})

// 菜单选项
const menuOptions = ref<any[]>([])

// 表单数据
const loading = ref<boolean>(false)
const formData = reactive<any>({
    id: 0,         // 菜单ID
    pid: 0,        // 父级菜单
    type: 'M',     // 菜单类型
    name: '',      // 菜单名称
    icon: '',      // 菜单图标
    perms: '',     // 权限标识
    params: '',    // 路由参数
    component: '', // 组件路径
    path: '',      // 路由地址
    sort: 0,       // 菜单排序
    is_show: 1,    // 是否显示:[0=否, 1=是]
    is_disable: 0  // 是否禁用:[0=否, 1=是]
})

// 表单规则
const formRules = reactive({
    pid: [
        {required: true,  message: '请选择父级菜单', trigger: ['blur', 'change']}
    ],
    name: [
        { required: true, message: '菜单名称不能为空', trigger: ['blur'] },
        { max: 100, message: '菜单名称不能大于100个字符', trigger: ['blur'] }
    ],
    path: [
        { required: true, message: '路由地址不能为空', trigger: ['blur'] },
        { max: 200, message: '路由地址不能大于200个字符', trigger: ['blur'] }
    ],
    perms: [
        { max: 200, message: '权限字符不能大于200个字符', trigger: ['blur'] }
    ],
    params: [
        { max: 200, message: '路由参数不能大于200个字符', trigger: ['blur'] }
    ],
    component: [
        { max: 200, message: '组件路径不能大于200个字符', trigger: ['blur'] }
    ]
})

/**
 * 获取视图
 */
const componentsOptions = ref(getModulesKey())
const querySearch = (queryString: string, cb: any) => {
    const results = queryString
        ? componentsOptions.value.filter((item: any) =>
            item.toLowerCase().includes(queryString.toLowerCase())
        )
        : componentsOptions.value
    cb(results.map((item: any) => ({ value: item })))
}

/**
 * 获取菜单
 */
const getMenu = async (): Promise<void> => {
    const data: any = await authMenuApi.lists()
    const menu: any = { id: 0, name: '顶级', children: [] }
    menu.children = toolsUtil.arrayToTree(
        toolsUtil.treeToArray(data).filter((item: any) => item.type !== 'A')
    )
    menuOptions.value.push(menu)
}

/**
 * 提交表单
 */
const handleSubmit = async (): Promise<void> => {
    await formRef.value?.validate()
    loading.value = true
    if (showMode.value === 'edit') {
        await authMenuApi.edit(formData)
            .finally(() => {
                loading.value = false
            })
    } else {
        await authMenuApi.add(formData)
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

    await getMenu()
    if (type === 'edit') {
        const data = await authMenuApi.detail(row.id)
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
