<template>
    <div class="pagination">
        <el-pagination
            v-model:currentPage="pager.page"
            v-model:pageSize="pager.limit"
            :background="background"
            :layout="layout"
            :size="size"
            :pager-count="pageCount"
            :page-sizes="pageSizes"
            :total="pager.total"
            :hide-on-single-page="false"
            @size-change="sizeChange"
            @current-change="pageChange"
        />
    </div>
</template>

<script setup lang="ts">
import type { EpPropMergeType } from 'element-plus/es/utils/index.mjs'

interface Props {
    modelValue?: Record<string, any>;
    pageSizes?: number[];
    layout?: string;
    size?: EpPropMergeType<StringConstructor, '' | 'default' | 'small' | 'large', never>;
    pageCount?: number;
    background?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
    modelValue: () => ({}),
    pageSizes: () => [15, 20, 30, 40, 50],
    layout: 'total, sizes, prev, pager, next, jumper',
    size: 'default',
    pageCount: 5,
    background: true
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
