import { defineConfig } from 'eslint/config'
import tsPlugin from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import vuePlugin from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'

export default defineConfig([
    // 忽略特定文件
    {
        ignores: [
            'dist/**',
            'node_modules/**',
            'auto-imports.d.ts',
            'components.d.ts'
        ]
    },
    // JS规则
    {
        files: ['**/*.{js,ts,jsx,tsx,mjs,cjs}'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            parser: tsParser,
            parserOptions: {
                ecmaVersion: 'latest',
                sourceType: 'module'
            }
        },
        linterOptions: {
            reportUnusedDisableDirectives: true
        },
        plugins: {
            '@typescript-eslint': tsPlugin as any
        },
        rules: {
            ...tsPlugin.configs.recommended.rules,
            '@typescript-eslint/no-unused-vars': 'warn',
            '@typescript-eslint/ban-ts-comment': 'off',
            '@typescript-eslint/no-explicit-any': 'off',
            '@typescript-eslint/no-unused-expressions': 'off'
        }
    },

    // VUE规则
    {
        files: ['**/*.vue'],
        languageOptions: {
            parser: vueParser,
            parserOptions: {
                parser: tsParser,
                ecmaVersion: 'latest',
                sourceType: 'module',
                extraFileExtensions: ['.vue']
            }
        },
        plugins: {
            'vue': vuePlugin
        },
        rules: {
            ...vuePlugin.configs.recommended.rules,
            'vue/no-v-html': 'warn',
            'vue/no-unused-refs': 'warn',
            'vue/no-useless-v-bind': 'warn',
            'vue/require-prop-types': 'warn',
            'vue/require-default-prop': 'warn',
            'vue/prefer-import-from-vue': 'off',
            'vue/multi-word-component-names': 'off',
            'vue/multiline-html-element-content-newline': 'off',
            'vue/singleline-html-element-content-newline': 'off',
            'vue/padding-line-between-blocks': ['warn', 'always'],
            'vue/attribute-hyphenation': ['error', 'always'],
            'vue/v-on-event-hyphenation': ['error', 'always', {
                'ignore': []
            }],
            'vue/max-attributes-per-line': [
                'warn',
                { singleline: 5 }
            ],
            'vue/html-indent': ['warn', 4, {
                'attribute': 1,
                'baseIndent': 1,
                'closeBracket': 0,
                'alignAttributesVertically': false,
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
    },

    // 通用规则
    {
        rules: {
            // 变量相关规则
            'no-var': 'warn',                  // 禁止使用var
            'no-shadow': 'off',                // 禁止变量声明与外层作用域变量同名
            'no-delete-var': 'off',            // 禁止删除变量
            'prefer-const': 'warn',            // 优先使用 const 声明未重新赋值的变量

            // 函数相关规则
            'no-func-assign': 'warn',           // 禁止对函数声明重新赋值
            'no-empty-function': 'off',         // 禁止空函数（关闭）
            'no-useless-call': 'warn',          // 禁止不必要的 call/apply
            'no-return-assign': 'warn',         // 禁止 return 语句中赋值
            'no-useless-return': 'warn',        // 禁止多余的 return 语句
            'prefer-arrow-callback': 'warn',    // 推荐使用箭头函数作为回调
            'arrow-spacing': 'warn',            // 箭头函数箭头前后需有空格
            'no-useless-catch': 'warn',         // 禁止不必要的 catch 块

            // 调试相关规则
            'no-console': 'warn',               // 禁止 console
            'no-debugger': 'warn',              // 禁止 debugger
            'no-undef': 'off',                  // 禁止未定义变量
            'no-redeclare': 'error',            // 禁止重复声明变量
            'no-lone-blocks': 'warn',           // 禁止不必要的代码块
            'no-extra-parens': 'warn',          // 禁止不必要的括号

            // 逻辑与控制流
            'no-empty': 'off',                   // 禁止空的代码块
            'no-unreachable': 'warn',            // 禁止不可达代码
            'no-else-return': 'warn',            // 如果 if 内有 return, 则else多余
            'no-self-compare': 'warn',           // 禁止与自身比较
            'no-return-await': 'warn',           // 禁止不必要的 return await
            'default-case': 'off',               // switch 必须包含 default 分支
            'no-duplicate-case': 'warn',         // 禁止 switch 中重复 case
            'max-depth': ['warn', 4],            // 限制代码块嵌套深度
            'max-statements': ['warn', 100],     // 限制函数内语句数量
            'max-nested-callbacks': ['warn', 3], // 限制嵌套回调深度
            'max-statements-per-line': ['warn', { max: 1 }], // 每行最多 1 条语句
            'curly': 'warn',                     // 强制使用大括号包裹代码块
            'eqeqeq': 'warn',                    // 强制使用 === 和 !==

            // 代码风
            'no-multi-spaces': 'off',           // 禁止多个空格
            'no-trailing-spaces': 'warn',       // 禁止行尾空格
            'no-multiple-empty-lines': 'warn',  // 禁止连续多个空行
            'no-mixed-spaces-and-tabs': 'warn', // 禁止混合使用空格和制表符
            'template-curly-spacing': 'warn',   // 模板字符串中大括号内需有空格
            'dot-notation': 'warn',             // 优先使用点表示法访问属性
            'brace-style': 'warn',              // 大括号风格(1TBS)
            'space-in-parens': 'warn',          // 括号内需有空格
            'space-infix-ops': 'warn',          // 中缀操作符周围需有空格
            'space-unary-ops': 'warn',          // 一元操作符前后需有空格
            'space-before-blocks': 'warn',      // 代码块前需有空格
            'array-bracket-spacing': 'warn',    // 数组括号内需有空格
            'yield-star-spacing': 'warn',       // yield* 表达式中 * 前后需有空格
            'switch-case-space': 'off',         // case 和 : 之间需有空格（关闭）
            'switch-colon-spacing': 'off',      // : 后需有空格（关闭）
            'prefer-template': 'warn',          // 推荐使用模板字符串
            'comma-dangle': ['warn', 'never'],  // 禁止末尾逗号
            'semi': ['warn', 'never'],          // 禁止分号
            'quotes': ['warn', 'single', 'avoid-escape'],  // 优先单引号
            'indent': ['warn', 4, { 'SwitchCase': 1 }]     // 缩进空格数
        }
    }
])
