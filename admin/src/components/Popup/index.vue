<template>
    <div class="dialog">
        <!-- 触发弹窗 -->
        <div class="dialog__trigger" @click="open">
            <slot name="trigger"></slot>
        </div>

        <el-dialog
            v-model="visible"
            :width="width"
            :center="center"
            :append-to-body="appendToBody"
            :close-on-click-modal="clickModalClose"
            :before-close="handleClose"
            class="none-padding"
            :class="customClass"
            @closed="close"
        >
            <!-- 弹窗标题 -->
            <template #header>
                <slot name="header">
                    <div class="dialog-header">
                        <el-image
                            v-if="icon"
                            :src="icon"
                            class="w-[24px] h-[24px] mr-3"
                        />
                        <div>
                            <h5>{{ title }}</h5>
                            <p
                                v-if="tips"
                                class="text-xs font-normal text-tx-secondary"
                            >{{ tips }}</p>
                        </div>
                    </div>
                </slot>
            </template>

            <!-- 弹窗内容 -->
            <slot>{{ content }}</slot>

            <!-- 弹窗页脚 -->
            <template #footer>
                <slot name="footer">
                    <div
                        v-if="cancelButtonText || confirmButtonText"
                        class="dialog-footer"
                        :class="footerBorder ? 'top-br' : ''"
                    >
                        <el-button v-if="cancelButtonText" @click="handleEvent('cancel')">
                            {{ cancelButtonText }}
                        </el-button>
                        <el-button
                            v-if="confirmButtonText"
                            type="primary"
                            :loading="loadingBtn"
                            :disabled="disabled"
                            @click="handleEvent('confirm')"
                        >
                            {{ confirmButtonText }}
                        </el-button>
                    </div>
                </slot>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
const emits = defineEmits(['confirm', 'cancel', 'close', 'open', 'beforeClose'])
const props = defineProps({
    // 弹窗显示
    show: {
        type: Boolean,
        default: false
    },
    // 弹窗图标
    icon: {
        type: String,
        default: ''
    },
    // 弹窗提示
    tips: {
        type: String,
        default: ''
    },
    // 弹窗标题
    title: {
        type: String,
        default: ''
    },
    // 弹窗内容
    content: {
        type: String,
        default: ''
    },
    // 确认按钮内容
    confirmButtonText: {
        type: [String, Boolean],
        default: '确定'
    },
    // 取消按钮内容
    cancelButtonText: {
        type: [String, Boolean],
        default: '取消'
    },
    // 弹出窗口宽度
    width: {
        type: String,
        default: '400px'
    },
    // 是否居中布局
    center: {
        type: Boolean,
        default: false
    },
    // 确认按钮加载
    loading: {
        type: Boolean,
        default: false
    },
    // 禁用确认按钮
    disabled: {
        type: Boolean,
        default: false
    },
    // 开启异步关闭
    asyncClose: {
        type: Boolean,
        default: false
    },
    // 遮罩层关闭窗口
    clickModalClose: {
        type: Boolean,
        default: false
    },
    // 关闭前拦截通知
    beforeClose: {
        type: Boolean,
        default: false
    },
    // 插入body元素
    appendToBody: {
        type: Boolean,
        default: true
    },
    // 自定义样式类
    customClass: {
        type: String,
        default: ''
    },
    // 页脚边框线条
    footerBorder: {
        type: Boolean,
        default: false
    }
})

const visible = ref(false)
const loadingBtn = ref(false)

const handleEvent = (type: 'confirm' | 'cancel') => {
    emits(type)
    if (!props.asyncClose || type === 'cancel') {
        close()
    }
}

const handleClose = (done: any) => {
    if (props.beforeClose) {
        emits('beforeClose')
    } else {
        done()
    }
}

const close = () => {
    visible.value = false
    nextTick(() => {
        emits('close')
    })
}

const open = () => {
    if (props.disabled) {
        return
    }
    emits('open')
    visible.value = true
}

watch(
    () => props.show,
    (val) => {
        visible.value = val
    }
)

watch(
    () => props.loading,
    (val) => {
        loadingBtn.value = val
    }
)

provide('visible', visible)
</script>

<style scoped lang="scss">
.el-dialog {
    .dialog-header {
        display: flex;
        align-items: center;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        color: var(--el-text-color-regular);
        background-color: var(--el-bg-color-light);
        border-bottom: 1px solid var(--el-border-color-extra-light);
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    .dialog-footer {
        padding: 12px 24px;
        color: var(--el-text-color-regular);
        border-bottom-right-radius: 6px;
        border-bottom-left-radius: 6px;
        &.top-br {
            border-top: 1px solid var(--el-border-color-extra-light);
        } 
    }
}
</style>
