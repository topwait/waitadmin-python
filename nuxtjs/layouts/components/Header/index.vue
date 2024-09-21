<template>
    <header>
        <div class="container">
            <NuxtLink v-if="pcConfig.logo" to="/" class="logo">
                <img :src="pcConfig.logo" :alt="pcConfig.name"/>
            </NuxtLink>
            <ul class="navigation">
                <li
                    v-for="(item, index) in menus"
                    :key="index"
                    :class="activeMenu === item.path ? 'active' : ''"
                >
                    <NuxtLink :to="item.path" :target="item.target">
                        {{ item.name }}
                        <icon v-if="item.children" name="el-icon-ArrowDown" />
                    </NuxtLink>
                    <dl v-if="item.children">
                        <dd v-for="(sub, i) in item.children" :key="i">
                            <NuxtLink :to="sub.path" :target="sub.target">
                                {{ sub.name }}
                            </NuxtLink>
                        </dd>
                    </dl>
                </li>
            </ul>
            <ul class="right">
                <li class="mx-[20px] cursor-pointer" @click="changeDark()">
                    <icon v-if="isDark" name="svg-icon-Dark" :size="22" />
                    <icon v-else name="svg-icon-Light" :size="22" />
                </li>
                <li v-if="!userStore.isLogin">
                    <a href="javascript:" @click="appStore.setPopup(popupEnum.LOGIN)">登录</a> /
                    <a href="javascript:" @click="appStore.setPopup(popupEnum.REGISTER)">注册</a>
                </li>
                <li v-else>
                    <el-dropdown class="px-2.5 h-full" @command="handleCommand">
                        <div class="flex items-center">
                            <el-avatar :size="30" :src="userInfo.avatar" />
                            <div class="ml-2 mr-1">{{ userInfo.nickname }}</div>
                            <icon name="el-icon-ArrowDown" />
                        </div>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <router-link to="/user/center">
                                    <el-dropdown-item>个人设置</el-dropdown-item>
                                </router-link>
                                <el-dropdown-item :divided="true" command="logout">退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </li>
            </ul>
        </div>
    </header>
</template>

<script setup lang="ts">
import { popupEnum } from '~/enums/app'
import useAppStore from '~/stores/app'
import useUserStore from '~/stores/user'
import useConfStore from '~/stores/conf'
import menus from '~/config/menu'

const route = useRoute()
const appStore = useAppStore()
const userStore = useUserStore()
const confStore = useConfStore()

// 暗黑主题
const isDark = computed(() => confStore.isDarkColor)
const changeDark = () => {
    confStore.setTheme(confStore.primaryTheme, !isDark.value)
    confStore.setSetting({
        key: 'isDarkColor',
        value: !isDark.value
    })
}

// PC端配置
const pcConfig = computed(() => {
    return {
        logo: appStore.getPcConfig.logo,
        name: appStore.getPcConfig.name
    }
})

// 用户信息
const userInfo = computed(() => {
    return {
        avatar: userStore.users.avatar,
        nickname: userStore.users.nickname
    }
})

// 激活菜单
const activeMenu = computed<string>(() => route.path)

// 指令处理
const handleCommand = async (command: string) => {
    switch (command) {
        case 'logout':
            feedback.confirm('确定退出登录吗？')
                .then(async () => {
                    await userStore.logout()
                }).catch(() => {})
    }
}
</script>

<style scoped lang="scss">
header {
    position: sticky;
    top: 0;
    z-index: 999;
    width: 100%;
    height: 60px;
    background: var(--el-bg-color);
    border-bottom: 1px solid var(--el-border-color-light);
    .container {
        display: flex;
        align-items: center;
        width: 1200px;
        margin: 0 auto;
    }
    .logo {
        display: flex;
        align-items: center;
        width: 160px;
        height: 60px;
        img {
            max-width: 100%;
            max-height: 100%;
        }
    }
    .navigation {
        display: flex;
        flex: 1;
        li {
            height: 60px;
            line-height: 60px;
            a {
                position: relative;
                display: block;
                padding: 0 24px;
                font-size: 16px;
                font-weight: bold;
                color: var(--el-text-color-regular);
            }
            &.active a {
                color: var(--el-color-primary);
            }
            &:hover > a {
                opacity: 0.8;
            }
            &:hover > dl {
                display: block;
                transition: all 300ms;
            }
            dl {
                position: absolute;
                z-index: 2000;
                display: none;
                min-width: 140px;
                padding: 5px 0;
                background: var(--color-white);
                border: 1px solid var(--el-border-color-light);
                border-radius: 2px;
                box-shadow: 0 6px 12px rgb(0 0 0 / 17.5%);
                transition: all 300ms;
                dd a {
                    display: block;
                    padding: 11px 20px;
                    font-size: 15px;
                    line-height: 1;
                    color: var(--el-text-color-regular);
                }
                dd:hover {
                    background: #f3f3f3;
                }
            }
        }
    }
    .right {
        display: flex;
        align-items: center;
        li {
            display: flex;
            align-items: center;
            a {
                display: inline-block;
                padding: 0 8px;
                font-size: 16px;
                font-weight: bold;
                color: var(--el-text-color-regular);
                &:hover {
                    color: var(--el-color-primary);
                }
            }
        }
    }
}
</style>
