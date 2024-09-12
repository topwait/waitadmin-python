module.exports = {
    'env': {
        'browser': true,
        'es2021': true,
        'node': true
    },
    'extends': [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:vue/vue3-essential'
    ],
    'overrides': [
        {
            'env': {
                'node': true
            },
            'files': [
                '.eslintrc.{js,cjs}'
            ],
            'parserOptions': {
                'sourceType': 'script'
            }
        }
    ],
    'parserOptions': {
        'ecmaVersion': 'latest',
        'parser': '@typescript-eslint/parser',
        'sourceType': 'module'
    },
    'plugins': [
        '@typescript-eslint',
        'vue'
    ],
    'rules': {
        'no-var': 'warn',
        'no-empty': 'warn',
        'no-undef': 'off',
        'no-shadow': 'off',
        'no-console': 'warn',
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
        'no-return-await': 'off',
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
        'max-nested-callbacks': ['warn', 3],
        'max-statements-per-line': ['warn', { max: 1 }],
        'quotes': ['warn', 'single', 'avoid-escape'],
        'switch-case-space': 'off',
        'switch-colon-spacing': 'off',
        'switch-space': [0, 'always'],
        'semi': ['warn', 'never'],
        'indent': [
            'warn',
            4,
            { 'SwitchCase': 1 }
        ],

        '@typescript-eslint/no-unused-vars': 'warn',
        '@typescript-eslint/ban-ts-comment': 'off',
        '@typescript-eslint/no-explicit-any': 'off',

        'vue/require-default-prop': 'off',
        'vue/prefer-import-from-vue': 'off',
        'vue/multi-word-component-names': 'off',
        'vue/singleline-html-element-content-newline': 'off',
        'vue/multiline-html-element-content-newline': 'off',
        'vue/max-attributes-per-line': ['warn', { singleline: 5 }],
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
