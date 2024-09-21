// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt([
    {
        rules: {
            'semi': ['warn', 'never'],
            'no-var': 'warn',
            'no-empty': 'warn',
            'no-undef': 'off',
            'no-shadow': 'off',
            'no-console': ['warn', { 'allow': ['error'] }],
            'no-debugger': 'warn',
            'no-lone-blocks': 'warn',
            'no-extra-parens': 'warn',
            'no-multi-spaces': 'off',
            'no-empty-function': 'off',
            'no-duplicate-case': 'warn',
            'no-redeclare': 'warn',
            'no-func-assign': 'warn',
            'no-unreachable': 'warn',
            'no-else-return': 'warn',
            'no-return-assign': 'warn',
            'no-return-await': 'warn',
            'no-self-compare': 'warn',
            'no-useless-catch': 'warn',
            'no-useless-return': 'warn',
            'no-mixed-spaces-and-tabs': 'warn',
            'no-multiple-empty-lines': 'warn',
            'no-trailing-spaces': 'warn',
            'no-useless-call': 'warn',
            'no-delete-var': 'off',
            'no-useless-escape': 'off',
            'dot-notation': 'warn',
            'default-case': 'off',
            'eqeqeq': 'warn',
            'curly': 'warn',
            'space-before-blocks': 'warn',
            'space-in-parens': 'warn',
            'space-infix-ops': 'warn',
            'space-unary-ops': 'warn',
            'arrow-spacing': 'warn',
            'array-bracket-spacing': 'warn',
            'brace-style': 'warn',
            'camelcase': 'off',
            'max-depth': ['warn', 4],
            'max-statements': ['warn', 100],
            'max-nested-callbacks': ['warn', 4],
            'max-statements-per-line': ['warn', { max: 1 }],
            'quotes': ['warn', 'single', 'avoid-escape'],
            'switch-case-space': 'off',
            'switch-colon-spacing': 'off',
            'switch-space': [0, 'always'],
            'indent': [
                'warn',
                4,
                { 'SwitchCase': 1 }
            ],
            '@typescript-eslint/ban-ts-comment': 'off',
            '@typescript-eslint/no-unused-vars': 'warn',
            '@typescript-eslint/no-explicit-any': 'off',
            'vue/attribute-hyphenation': 0,
            'vue/require-default-prop': 0,
            'vue/multi-word-component-names': 0,
            'vue/singleline-html-element-content-newline': 0,
            'vue/multiline-html-element-content-newline': 0,
            'vue/max-attributes-per-line': ['warn', { singleline: 5 }],
            'vue/no-v-html': 'off',
            'vue/html-indent': ['warn', 4, {
                'attribute': 1,
                'baseIndent': 1,
                'closeBracket': 0,
                'alignAttributesVertically': true,
                'ignores': []
            }],
            'vue/html-self-closing': ['error', {
                'html': {
                    'void': 'always',
                    'normal': 'never',
                    'component': 'always'
                },
                'svg': 'always',
                'math': 'always'
            }]
        }
    }
])
