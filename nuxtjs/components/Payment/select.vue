<template>
    <div class="payments">
        <div
            v-for="(item, index) in payWayList"
            :key="index"
            class="pay-item"
            :class="{ active: payWayType === item.channel }"
            @click="payWayType = item.channel"
        >
            <el-image :src="item.icon" class="h-[24px] w-[24px]" />
            <div class="ml-[10px]">{{ item.shorter }}</div>
            <div v-if="payWayType === item.channel" class="select-icon">
                <icon class="el-icon-select" name="el-icon-Select" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useVModel } from '@vueuse/core'
import paymentApi from '@/api/payment'

const props = defineProps<{
    from: 'recharge'
    modelValue: string | number
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: string | number): void
}>()

const payWayType = useVModel(props, 'modelValue', emit)
const payWayList: any = ref([])

const queryPayWay = async () => {
    payWayList.value = await paymentApi.payWay()
    payWayType.value = payWayList.value[0].channel
}

queryPayWay()
</script>

<style scoped lang="scss">
.payments {
    display: flex;
    .pay-item {
        position: relative;
        display: flex;
        align-items: center;
        padding: 20px 35px;
        margin: 0 8px;
        overflow: hidden;
        cursor: pointer;
        border: 1px solid var(--el-border-color-light) !important;
        border-radius: .5rem;
        &.active {
            border: 1px solid var(--el-color-primary) !important;
        }
        .select-icon {
            position: absolute;
            right: -1px;
            bottom: -1px;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 26px;
            height: 26px;
            clip-path: polygon(0 100%, 100% 0, 100% 100%);
            color: var(--color-white);
            background-color: var(--el-color-primary);
            :deep() .el-icon-select {
                transform: translate(35%, 35%);
                transform-origin: center center;
            }
        }
    }
}
</style>
