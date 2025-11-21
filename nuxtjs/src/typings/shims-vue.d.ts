/**
 * TS2307: Cannot find module ./SvgIcon.vue or its corresponding type declarations.
 */
declare module '*.vue' {
    import Vue from 'vue'
    export default Vue
}

declare module '@element-plus/icons-vue' {
    import type { DefineComponent } from 'vue'
    const components: Record<string, DefineComponent>
    export default components
}
