<template>
    <el-date-picker
        v-model="content"
        :type="type"
        :range-separator="rangeSeparator"
        :start-placeholder="startPlaceholder"
        :end-placeholder="endPlaceholder"
        :value-format="valueFormat"
        clearable
    />
</template>

<script setup lang="ts">
const props = withDefaults(
    defineProps<{
        startTime?: string
        endTime?: string
        type?: any
        rangeSeparator?: string
        startPlaceholder?: string
        endPlaceholder?: string
        valueFormat?: string
    }>(),
    {
        startTime: '',
        endTime: '',
        type: 'datetimerange',
        rangeSeparator: '-',
        startPlaceholder: '开始时间',
        endPlaceholder: '结束时间',
        valueFormat: 'YYYY-MM-DD HH:mm:ss'
    }
)

const emits = defineEmits(['update:startTime', 'update:endTime'])

const content = computed<any>({
    get: () => {
        return [props.startTime, props.endTime]
    },
    set: (value: Event | any) => {
        if (value === null) {
            emits('update:startTime', '')
            emits('update:endTime', '')
        } else {
            emits('update:startTime', value[0])
            emits('update:endTime', value[1])
        }
    }
})
</script>
