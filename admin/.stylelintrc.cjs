module.exports = {
    extends: [
        'stylelint-config-recess-order',
        'stylelint-config-standard-scss',
        'stylelint-config-recommended-vue/scss'
    ],
    plugins: [
        'stylelint-scss',
        'stylelint-order'
    ],
    ignoreFiles: [
        '**/*.js',
        '**/*.ts',
        '**/*.cjs',
        '**/*.jsx',
        '**/*.tsx',
        'index.html'
    ],
    rules: {
        'color-hex-length': 'long',
        'no-empty-source': null,
        'property-no-unknown': null,
        'keyframes-name-pattern': null,
        'selector-class-pattern': null,
        'rule-empty-line-before': null,
        'custom-property-pattern': null,
        'no-descending-specificity': null,
        'declaration-empty-line-before': null,
        'custom-property-empty-line-before': null,
        'declaration-block-single-line-max-declarations': null,
        'selector-pseudo-element-no-unknown': [
            true,
            {
                ignorePseudoElements: ['v-deep', 'v-global', 'v-slotted']
            }
        ],
        'scss/at-import-partial-extension': null,
        'scss/at-rule-no-unknown': [
            true,
            {
                ignoreAtRules: [
                    'tailwind',
                    'apply',
                    'variants',
                    'responsive',
                    'screen',
                    'function',
                    'if',
                    'each',
                    'include',
                    'mixin',
                    'use'
                ]
            }
        ]
    }
}
