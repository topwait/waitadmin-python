<template>
    <div @mouseenter="inPopover = true" @mouseleave="inPopover = false">
        <el-popover
            v-model:visible="visible"
            placement="top"
            trigger="contextmenu"
            class="popover-input"
            popper-class="!p-0"
            :width="width"
            :teleported="teleported"
            :persistent="false"
        >
            <div class="flex p-3" @click.stop="">
                <div class="popover-input__input mr-[10px] flex-1">
                    <el-select
                        v-if="type == 'select'"
                        v-model="inputValue"
                        class="flex-1"
                        :size="size"
                        :teleported="teleported"
                    >
                        <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                    <el-input
                        v-else
                        v-model.trim="inputValue"
                        clearable
                        :maxlength="limit"
                        :show-word-limit="showLimit"
                        :type="type"
                        :size="size"
                        :placeholder="placeholder"
                    />
                </div>
                <div class="popover-input__btn flex-none">
                    <el-button link @click="close">取消</el-button>
                    <el-button
                        type="primary"
                        :size="size"
                        @click="handleConfirm"
                    >
                        确定
                    </el-button>
                </div>
            </div>
            <template #reference>
                <div class="inline" @click.stop="handleOpen">
                    <slot></slot>
                </div>
            </template>
        </el-popover>
    </div>
</template>

<script lang="ts" setup>
import { useEventListener } from '@vueuse/core'
import { ElPopover, ElButton, ElSelect, ElOption, ElInput } from 'element-plus'
import type { PropType } from 'vue'

const props = defineProps({
    value: {
        type: [Number, String],
        default: ''
    },
    type: {
        type: String,
        default: 'text'
    },
    width: {
        type: [Number, String],
        default: '300px'
    },
    placeholder: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    },
    options: {
        type: Array as PropType<any[]>,
        default: () => []
    },
    size: {
        type: String as PropType<'default' | 'small' | 'large'>,
        default: 'default'
    },
    limit: {
        type: Number,
        default: 200
    },
    showLimit: {
        type: Boolean,
        default: false
    },
    teleported: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits(['confirm'])
const visible = ref(false)
const inPopover = ref(false)
const inputValue = ref()

/**
 * 确定按钮
 */
const handleConfirm = () => {
    close()
    emit('confirm', inputValue.value)
}

/**
 * 弹出窗口
 */
const handleOpen = () => {
    if (props.disabled) {
        return
    }
    visible.value = true
    inputValue.value = props.value
}

/**
 * 关闭窗口
 */
const close = () => {
    visible.value = false
}

/**
 * 监听变化
 */
watch(() => props.value,
    (value) => {
        inputValue.value = value
    },
    { immediate: true }
)

/**
 * 监听点击
 */
useEventListener(document.documentElement, 'click', () => {
    if (inPopover.value) {
        return
    }
    close()
})
</script>