<template>
    <div class="price-container">
        <div
            :class="['price-wrap', { 'price-wrap--disabled': lineThrough }]"
            :style="{ color: color }"
        >
            <!-- Prefix -->
            <div class="fix-pre" :style="{ fontSize: minorSize }">
                <slot name="prefix">{{ prefix }}</slot>
            </div>

            <!-- Content -->
            <div :style="{ 'font-weight': fontWeight }">
                <!-- Integer -->
                <text :style="{ fontSize: mainSize }">{{ integer }}</text>
                <!-- Decimals -->
                <text :style="{ fontSize: minorSize }">{{ decimals }}</text>
            </div>

            <!-- Suffix -->
            <div class="fix-suf" :style="{ fontSize: minorSize }">
                <slot name="suffix">{{ suffix }}</slot>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

const props = withDefaults(
    defineProps<{
      content: string | number // 标题
      digits?: number          // 小数位数
      autoDigits?: boolean     // 动态小数
      color?: string           // 字体颜色
      mainSize?: string        // 主要内容字体大小
      minorSize?: string       // 次要内容字体大小
      lineThrough?: boolean    // 贯穿线
      fontWeight?: string      // 字重
      prefix?: string          // 前缀
      suffix?: string          // 后缀
    }>(),
    {
        content: '',
        digits: 2,
        autoDigits: true,
        color: 'inherit',
        mainSize: '18px',
        minorSize: '14px',
        lineThrough: false,
        fontWeight: 'normal',
        prefix: '￥',
        suffix: ''
    }
)

/**
 * 金额主体部分
 */
const integer = computed(() => {
    return formatPrice({
        price: props.content,
        take: 'int'
    })
})

/**
 * 金额小数部分
 */
const decimals = computed(() => {
    let decimals: any = formatPrice({
        price: props.content,
        prec: props.digits,
        take: 'dec'
    })
    // 小数余十不能是 .10||.20||.30以此类推
    decimals = decimals % 10 === 0 ? decimals.substr(0, decimals.length - 1) : decimals
    return props.autoDigits
        ? decimals * 1
            ? `.${decimals}`
            : ''
        : props.digits
            ? `.${decimals}`
            : ''
})

function formatPrice({ price, take = 'all', digits = undefined }: any) {
    // eslint-disable-next-line prefer-const
    let [integer, decimals = ''] = `${price}`.split('.')

    // 小数位补
    if (digits !== undefined) {
        const LEN = decimals.length
        for (let i = digits - LEN; i > 0; --i) {
            decimals += '0'
        }
        decimals = decimals.substr(0, digits)
    }

    switch (take) {
        case 'int':
            return integer
        case 'dec':
            return decimals
        case 'all':
            return `${integer}.${decimals}`
    }
}
</script>

<style lang="scss" scoped>
.price-container {
    display: inline-block;
}

.price-wrap {
    display: flex;
    align-items: baseline;
    &--disabled {
        position: relative;
        &::before {
            position: absolute;
            top: 50%;
            right: 0;
            left: 0;
            display: block;
            height: 0.05em;
            content: '';
            background-color: currentcolor;
            transform: translateY(-50%);
        }
    }
}
</style>
