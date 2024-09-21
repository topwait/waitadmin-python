<template>
    <el-button v-if="!isStart" link @click="handleStart">
        <span v-if="isIng" class="text-tx-disabled">{{ ingText }}</span>
        <span v-else>{{ isRetry ? endText : startText }}</span>
    </el-button>
    <vue-countdown
        v-else
        ref="vueCountdownRef"
        v-slot="{ totalSeconds }"
        :time="seconds * 1000"
        @end="end"
    >
        {{ getChangeText(totalSeconds) }}
    </vue-countdown>
</template>

<script lang="ts">
import VueCountdown from '@chenfengyuan/vue-countdown'
import { useThrottleFn } from '@vueuse/core'
import { ElButton } from 'element-plus'

export default defineComponent({
    components: {
        VueCountdown,
        ElButton
    },
    props: {
        // 倒计时的总秒数
        seconds: {
            type: Number,
            default: 60
        },
        // 正在获取时提示
        ingText: {
            type: String,
            default: '正在发送中'
        },
        // 尚未开始时提示
        startText: {
            type: String,
            default: '获取验证码'
        },
        // 正在倒计时中的提示
        changeText: {
            type: String,
            default: 'x秒重新获取'
        },
        // 倒计时结束时的提示
        endText: {
            type: String,
            default: '重新获取'
        }
    },
    emits: ['click-get'],
    setup(props, { emit }) {
        const isIng = ref(false)
        const isStart = ref(false)
        const isRetry = ref(false)

        const start = async () => {
            if (!isStart.value) {
                isStart.value = true
            }
        }

        const end = () => {
            isIng.value = false
            isStart.value = false
            isRetry.value = true
        }

        const ing = () => {
            isIng.value = true
            isStart.value = false
            isRetry.value = false
        }

        const getChangeText = (second: any) => {
            return props.changeText.replace('x', second)
        }

        const handleStart = useThrottleFn(
            () => {
                emit('click-get')
            },
            1000,
            false
        )

        return {
            isIng,
            isStart,
            isRetry,
            start,
            end,
            ing,
            handleStart,
            getChangeText
        }
    }
})
</script>
