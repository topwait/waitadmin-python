<script lang="ts">
import { createVNode } from 'vue'
import { ElIcon } from 'element-plus'
import SvgIcon from './SvgIcon.vue'
import { EL_ICON_PREFIX, SVG_ICON_PREFIX } from './index'

export default defineComponent({
    name: 'Icon',
    props: {
        name: {
            type: String,
            required: true
        },
        size: {
            type: [String, Number],
            default: '14px'
        },
        color: {
            type: String,
            default: 'inherit'
        }
    },
    setup(props) {
        if (props.name.indexOf(EL_ICON_PREFIX) === 0) {
            return () =>
                createVNode(
                    ElIcon,
                    {
                        size: props.size,
                        color: props.color
                    },
                    () => [createVNode(resolveComponent(props.name.replace(EL_ICON_PREFIX, '')))]
                )
        }
        if (props.name.indexOf(SVG_ICON_PREFIX) === 0) {
            const size: string = props.size + ''
            const font: string = /^\d+$/.test(size) ? size + 'px' : size
            return () =>
                h(
                    'i',
                    {
                        class: ['el-icon'],
                        style: {
                            'font-size': font,
                            '--color': props.color
                        }
                    },
                    createVNode(SvgIcon, { ...props })
                )
        }
    }
})
</script>
