<template>
    <div
        class="h-full cursor-pointer flex items-center px-2"
        @click="onSetShow"
    >
        <icon name="el-icon-setting" :size="16"/>
    </div>

    <el-drawer
        v-model="settingShow"
        append-to-body
        direction="rtl"
        size="280px"
        :with-header="false"
        :show-close="false"
    >
        <div class="drawer-card">
            <div class="drawer-card-header">布局设置</div>
            <div class="drawer-card-body">
                <div class="layout-drawer-container">
                    <div class="drawer-item"
                         :class="layout==='classic' ? 'active' : ''"
                         @click="layout = 'classic'"
                    >
                        <section class="el-container">
                            <aside class="el-aside" style="width: 17px; margin-right: 5px;"></aside>
                            <section class="el-container is-vertical">
                                <header class="el-header" style="height: 10px; margin-bottom: 5px;"></header>
                                <main class="el-main"></main>
                            </section>
                        </section>
                    </div>
                    <div class="drawer-item"
                         :class="layout==='columns' ? 'active' : ''"
                         @click="layout = 'columns'"
                    >
                        <section class="el-container">
                            <aside class="el-aside" style="width: 10px; margin-right: 5px;"></aside>
                            <aside class="el-aside-dark" style="width: 17px; margin-right: 5px;"></aside>
                            <section class="el-container is-vertical">
                                <header class="el-header" style="height: 10px; margin-bottom: 5px;"></header>
                                <main class="el-main"></main>
                            </section>
                        </section>
                    </div>
                    <div class="drawer-item"
                         :class="layout==='regular' ? 'active' : ''"
                         @click="layout = 'regular'"
                    >
                        <section class="el-container is-vertical">
                            <header class="el-aside" style="height: 10px; margin-bottom: 5px;"></header>
                            <section class="el-container">
                                <aside class="el-aside-dark" style="width: 17px; margin-right: 5px;"></aside>
                                <section class="el-container is-vertical">
                                    <main class="el-main"></main>
                                </section>
                            </section>
                        </section>
                    </div>
                    <div class="drawer-item"
                         :class="layout==='roomier' ? 'active' : ''"
                         @click="layout = 'roomier'"
                    >
                        <section class="el-container is-vertical">
                            <header class="el-aside" style="height: 10px; margin-bottom: 5px;"></header>
                            <section class="el-container">
                                <section class="el-container is-vertical">
                                    <main class="el-main"></main>
                                </section>
                            </section>
                        </section>
                    </div>
                </div>
            </div>
        </div>

        <hr />

        <div class="drawer-card">
            <div class="drawer-card-header">风格设置</div>
            <div class="drawer-card-body">
                <dl>
                    <dt>主题配色</dt>
                    <dd>
                        <el-select v-model="theme" size="default">
                            <el-option
                                v-for="(item, index) in themes"
                                :key="index"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-select>
                    </dd>
                </dl>
                <dl>
                    <dt>暗黑模式</dt>
                    <dd>
                        <el-switch v-model="isDarkColor" :active-value="true" :inactive-value="false" />
                    </dd>
                </dl>
                <dl>
                    <dt>菜单手风琴</dt>
                    <dd>
                        <el-switch v-model="isUniqueOpened" :active-value="true" :inactive-value="false" />
                    </dd>
                </dl>
                <dl>
                    <dt>历史标签风格</dt>
                    <dd>
                        <el-radio-group v-model="tagsStyle" size="small">
                            <el-radio-button label="灵动" value="nimble" />
                            <el-radio-button label="卡片" value="wedged" />
                            <el-radio-button label="圆滑" value="smooth" />
                        </el-radio-group>
                    </dd>
                </dl>
                <dl>
                    <dt>页面切换动画</dt>
                    <dd>
                        <el-radio-group v-model="pagesAnimation" size="small">
                            <el-radio-button label="渐显" value="slide-fade" />
                            <el-radio-button label="左滑" value="slide-left" />
                            <el-radio-button label="右滑" value="slide-right" />
                        </el-radio-group>
                    </dd>
                </dl>
                <dl v-if="layout !== 'roomier'">
                    <dt>菜单高亮风格</dt>
                    <dd>
                        <el-radio-group v-model="menuLightStyle" size="small" >
                            <el-radio-button label="卡片" value="card" />
                            <el-radio-button label="圆角" value="round" />
                        </el-radio-group>
                    </dd>
                </dl>
            </div>
        </div>

        <hr />

        <div class="drawer-card">
            <div class="drawer-card-header">界面显示</div>
            <div class="drawer-card-body">
                <dl>
                    <dt>显示标签栏</dt>
                    <dd>
                        <el-switch v-model="isTabMultiple" :active-value="true" :inactive-value="false" />
                    </dd>
                </dl>
                <dl>
                    <dt>显示面包屑</dt>
                    <dd>
                        <el-switch
                            v-model="isBreadcrumb"
                            :active-value="true"
                            :inactive-value="false"
                            :disabled="['regular', 'roomier'].includes(layout)"
                        />
                    </dd>
                </dl>
                <dl>
                    <dt>显示图标 (Logo)</dt>
                    <dd>
                        <el-switch v-model="isLayoutLogo" :active-value="true" :inactive-value="false" />
                    </dd>
                </dl>
            </div>
        </div>

        <div class="drawer-card">
            <div class="drawer-card-header">其它设置</div>
            <div class="drawer-card-body">
                <dl>
                    <dt>是否缓存页面</dt>
                    <dd>
                        <el-switch v-model="isKeepAlive" :active-value="true" :inactive-value="false" />
                    </dd>
                </dl>
            </div>
        </div>
    </el-drawer>
</template>

<script setup lang="ts">
import useConfStore from '@/stores/modules/conf'

const confStore = useConfStore()
const primaryTheme = computed(() => confStore.primaryTheme)

// 主题风格
const themes = [
    {label: '黑蓝', color: '#0669E3', value: 'black-blue'},
    {label: '黑绿', color: '#41B584', value: 'black-green'},
    {label: '黑紫', color: '#6954F0', value: 'black-purple'},
    {label: '白蓝', color: '#0669E3', value: 'white-blue'},
    {label: '白绿', color: '#41B584', value: 'white-green'},
    {label: '白紫', color: '#6954F0', value: 'white-purple'}
]

// 主题配色
const theme = computed({
    get() {
        return confStore.theme
    },
    set(value) {
        const index = themes.findIndex(theme => theme.value === value)
        confStore.setTheme(value, themes[index].color, isDarkColor.value)
        confStore.setSetting({
            key: 'theme',
            value
        })
        confStore.setSetting({
            key: 'theme',
            value
        })
    }
})

// 暗黑模式
const isDarkColor = computed({
    get() {
        return confStore.isDarkColor
    },
    set(value) {
        confStore.setTheme(theme.value, primaryTheme.value, value)
        confStore.setSetting({
            key: 'isDarkColor',
            value
        })
    }
})

// 布局设置
const layout = computed({
    get() {
        return confStore.layout
    },
    set(value) {
        confStore.setSetting({
            key: 'settingShow',
            value: false
        })

        confStore.setSetting({
            key: 'layout',
            value
        })

        confStore.setSetting({
            key: 'isTabMultiple',
            value: !['regular', 'roomier'].includes(value)
        })
    }
})

// 历史标签风格
const tagsStyle = computed({
    get() {
        return confStore.tagsStyle
    },
    set(value) {
        confStore.setSetting({
            key: 'tagsStyle',
            value
        })
    }
})

// 页面切换动画
const pagesAnimation = computed({
    get() {
        return confStore.pagesAnimation
    },
    set(value) {
        confStore.setSetting({
            key: 'pagesAnimation',
            value
        })
    }
})

// 菜单高亮风格
const menuLightStyle = computed({
    get() {
        return confStore.menuLightStyle
    },
    set(value) {
        confStore.setSetting({
            key: 'menuLightStyle',
            value
        })
    }
})

// 菜单手风琴
const isUniqueOpened = computed({
    get() {
        return confStore.isUniqueOpened
    },
    set(value) {
        confStore.setSetting({
            key: 'isUniqueOpened',
            value
        })
    }
})

// 显示标签栏
const isTabMultiple = computed({
    get() {
        return confStore.isTabMultiple
    },
    set(value) {
        confStore.setSetting({
            key: 'isTabMultiple',
            value
        })
    }
})

// 显示面包屑
const isBreadcrumb = computed({
    get() {
        return confStore.isBreadcrumb
    },
    set(value) {
        confStore.setSetting({
            key: 'isBreadcrumb',
            value
        })
    }
})

// 显示图标 Logo
const isLayoutLogo = computed({
    get() {
        return confStore.isLayoutLogo
    },
    set(value) {
        confStore.setSetting({
            key: 'isLayoutLogo',
            value
        })
    }
})

// 是否缓存页面
const isKeepAlive = computed({
    get() {
        return confStore.isKeepAlive
    },
    set(value) {
        confStore.setSetting({
            key: 'isKeepAlive',
            value
        })
    }
})

// 抽屉控制显示
const settingShow = computed({
    get() {
        return confStore.settingShow
    },
    set(value) {
        confStore.setSetting({
            key: 'settingShow',
            value
        })
    }
})

const onSetShow = () => {
    confStore.setSetting({
        key: 'settingShow',
        value: true
    })
}
</script>

<style scoped lang="scss">
hr {
    margin: 15px 0 10px;
    border-color: #e9eaee;
}

.drawer-card {
    margin-bottom: 20px;
    .drawer-card-header {
        padding: 10px 0;
        font-size: 15px;
        font-weight: bold;
        line-height: 22px;
        color: #606266;
    }
    .drawer-card-body {
        dl {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0;
            dt {
                overflow: hidden;
                font-size: 14px;
                color: var(--el-text-color-regular);
            }
            dd {
                display: flex;
                align-items: center;
            }
        }
        :deep(.el-select) {
            width: 90px;
        }
        :deep(.el-radio-button__inner) {
            padding: 7px 8px;
        }
    }
}

.layout-drawer-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    .drawer-item {
        position: relative;
        width: 100px;
        height: 70px;
        padding: 6px;
        margin: 10px 8px;
        cursor: pointer;

        background: var(--el-bg-color);
        border: 1px solid transparent;
        border-radius: 6px;
        box-shadow: 0 2px 5px 0 rgb(0 0 0 / 8%);
        opacity: 1;
        &.active {
            border: 1px solid var(--el-color-primary);
        }
        .el-container {
            height: 100%;
            overflow: hidden;
            .el-header {
                background-color: #b3c0d1;
                border-radius: 2px;
            }
            .el-main {
                padding: 0;
                border: 1px dashed var(--el-color-primary);
                border-radius: 2px;
            }
            .el-aside {
                background-color: var(--el-color-primary);
                border-radius: 2px;
            }
            .el-aside-dark {
                background-color: var(--el-color-primary-light-3);
                border-radius: 2px;
                opacity: .5;
            }
        }
    }
}
</style>
