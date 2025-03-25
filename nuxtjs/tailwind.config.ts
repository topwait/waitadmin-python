/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './components/**/*.{vue,js,ts}',
        './layouts/**/*.{vue,js,ts}',
        './pages/**/*.{vue,js,ts}',
        './plugins/**/*.{js,ts}'
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                'white': 'var(--color-white)',
                'black': 'var(--color-black)',
                'primary': {
                    DEFAULT: 'var(--el-color-primary)',
                    'light-3': 'var(--el-color-primary-light-3)',
                    'light-5': 'var(--el-color-primary-light-5)',
                    'light-7': 'var(--el-color-primary-light-7)',
                    'light-8': 'var(--el-color-primary-light-8)',
                    'light-9': 'var(--el-color-primary-light-9)',
                    'dark-2': 'var(--el-color-primary-dark-2)'
                },
                'success': 'var(--el-color-success)',
                'warning': 'var(--el-color-warning)',
                'danger': 'var(--el-color-danger)',
                'error': 'var(--el-color-error)',
                'info': 'var(--el-color-info)',

                'body': 'var(--el-bg-color)',
                'page': 'var(--el-bg-color-page)',
                'light': 'var(--el-bg-color-light)',
                'lighter': 'var(--el-bg-color-lighter)',

                'tx-primary': 'var(--el-text-color-primary)',
                'tx-regular': 'var(--el-text-color-regular)',
                'tx-secondary': 'var(--el-text-color-secondary)',
                'tx-placeholder': 'var(--el-text-color-placeholder)',
                'tx-disabled': 'var(--el-text-color-disabled)',

                'br': 'var(--el-border-color)',
                'br-dark': 'var(--el-border-color-dark)',
                'br-darker': 'var(--el-border-color-darker)',
                'br-light': 'var(--el-border-color-light)',
                'br-lighter': 'var(--el-border-color-lighter)',
                'br-extra-light': 'var(--el-border-color-extra-light)',

                'fill': 'var(--el-fill-color)',
                'fill-darker': 'var(--el-fill-color-darker)',
                'fill-dark': 'var(--el-fill-color-dark)',
                'fill-light': 'var(--el-fill-color-light)',
                'fill-lighter': 'var(--el-fill-color-lighter)',
                'fill-extra-light': 'var(--el-fill-color-extra-light)',
                'fill-blank': 'var(--el-fill-color-blank)'
            },
            fontFamily: {
                'sans': [
                    'PingFang SC',
                    'Arial',
                    'Hiragino Sans GB',
                    'Microsoft YaHei',
                    'sans-serif'
                ]
            },
            fontSize: {
                'xs': 'var(--el-font-size-extra-small)',  // 12px
                'sm': 'var(--el-font-size-small)',        // 13px
                'base': 'var(--el-font-size-base)',       // 14px
                'lg': 'var(--el-font-size-medium)',       // 16px
                'xl': 'var(--el-font-size-large)',        // 18px
                '2xl': 'var(--el-font-size-extra-large)', // 20px
                '3xl': '22px',
                '4xl': '24px',
                '5xl': '28px',
                '6xl': '30px',
                '7xl': '36px',
                '8xl': '48px',
                '9xl': '60px'
            },
            lineHeight: {
                'none': '1'
            },
            spacing: {
                px: '1px',
                0: '0px',
                0.5: '2px',
                1: '4px',
                1.5: '6px',
                2: '8px',
                2.5: '10px',
                3: '12px',
                3.5: '14px',
                4: '16px',
                4.5: '18px',
                5: '20px',
                5.5: '22px',
                6: '24px',
                7: '28px',
                8: '32px',
                9: '36px',
                10: '40px',
                11: '44px',
                12: '48px',
                14: '56px',
                16: '64px',
                20: '80px',
                24: '96px',
                28: '112px',
                32: '128px',
                36: '144px',
                40: '160px',
                44: '176px',
                48: '192px',
                52: '208px',
                56: '224px',
                60: '240px',
                64: '256px',
                72: '288px',
                80: '320px',
                96: '384px'
            },
            screens: {
                'sm': '640px',
                'md': '768px',
                'lg': '1024px',
                'xl': '1280px',
                '2xl': '1536px',
                '3xl': '1792px',
                '4xl': '2048px',
                '5xl': '2304px',
                '6xl': '2560px',
                '7xl': '2816px',
                '8xl': '3072px',
                '9xl': '3328px',
                '10xl': '3584px'
            }
        }
    },
    plugins: []
}
