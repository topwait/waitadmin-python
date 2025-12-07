<template>
    <div class="pagination">
        <el-pagination
            v-model:current-page="pager.page"
            v-model:page-size="pager.size"
            :background="background"
            :layout="layout"
            :size="size"
            :disabled="disabled"
            :pager-count="pageCount"
            :page-sizes="pageSizes"
            :total="pager.total"
            :teleported="teleported"
            :hide-on-single-page="hideOnSinglePage"
            @size-change="sizeChange"
            @current-change="pageChange"
        />
    </div>
</template>

<script setup lang="ts">
import type { EpPropMergeType } from 'element-plus/es/utils/index.mjs'

interface Props {
    modelValue?: Record<string, any>;
    // 每页显示条目个数
    pageSizes?: number[];
    // 组件布局
    layout?: string;
    // 分页大小
    size?: EpPropMergeType<StringConstructor, '' | 'default' | 'small' | 'large', never>;
    // 总页数
    pageCount?: number;
    // 是否禁用分页
    disabled?: boolean;
    // 分页按钮添加背景色
    background?: boolean;
    // 将下拉菜单teleport至body
    teleported?: boolean;
    // 只有一页时是否隐藏
    hideOnSinglePage?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
    modelValue: () => ({}),
    pageSizes: () => [15, 20, 30, 40, 50],
    layout: 'total, sizes, prev, pager, next, jumper',
    size: 'default',
    pageCount: 5,
    disabled: false,
    background: true,
    teleported: true,
    hideOnSinglePage: false
})

const emit = defineEmits<{
    (event: 'change'): void
    (event: 'update:modelValue', value: any): void
}>()

const pager = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})

const sizeChange = () => {
    pager.value.page = 1
    emit('change')
}

const pageChange = () => {
    emit('change')
}
</script>

<style scoped lang="scss">
.pagination {
    :deep(.el-input)  {
        &.el-input--small {
            --el-input-height: 32px !important;
        }
    }
}
</style>
