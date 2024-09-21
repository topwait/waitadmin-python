<template>
    <NuxtLayout name="default">
        <template #container>
            <div class="left-sidebar">
                <div class="member">
                    <div class="avatar">
                        <ElAvatar :size="120" :src="userInfo.avatar" />
                    </div>
                    <div class="name">{{ userInfo.nickname }}</div>
                    <div class="nums">
                        <p>
                            <span class="num">{{ userInfo.balance }}</span>
                            <span class="text">余额</span>
                        </p>
                        <p>
                            <span class="num">{{ userInfo.collect }}</span>
                            <span class="text">收藏</span>
                        </p>
                    </div>
                </div>
                <ul class="menus">
                    <li
                        v-for="(item, index) in menus"
                        :key="index"
                        :class="activeMenu === item.path ? 'active' : ''"
                    >
                        <NuxtLink :to="item.path">
                            <icon :name="item.icon" size="22" />
                            <span>{{ item.name }}</span>
                        </NuxtLink>
                    </li>
                </ul>
            </div>
            <div class="right-iframe">
                <NuxtPage />
            </div>
        </template>
    </NuxtLayout>
</template>

<script setup lang="ts">
import useUserStore from '~/stores/user'

const route = useRoute()
const userStore = useUserStore()

// 激活菜单
const activeMenu = computed<string>(() => route.path)

// 用户信息
const userInfo = computed(() => userStore.users)

// 导航菜单
const menus: Ref<any> = ref([
    {
        name: '主页',
        icon: 'el-icon-User',
        path: '/user/center'
    },
    {
        name: '安全',
        icon: 'el-icon-SetUp',
        path: '/user/safer'
    },
    {
        name: '收藏',
        icon: 'el-icon-Star',
        path: '/user/collect'
    },
    {
        name: '充值',
        icon: 'el-icon-Ship',
        path: '/user/recharge'
    }
])

definePageMeta({
    auth: true
})
</script>

<style scoped lang="scss">
.left-sidebar {
    flex-shrink: 0;
    width: 200px;
    min-height: 750px;
    margin: 20px 0;
    background-color: var(--el-bg-color-overlay);
    border-radius: 4px;
    .member {
        .avatar {
            display: block;
            width: 120px;
            height: 120px;
            margin: 10px auto 0;
            border-radius: 50%;
        }
        .name {
            width: 100%;
            height: 24px;
            margin: 10px 0;
            font-size: 14px;
            text-align: center;
        }
        .nums {
            display: block;
            padding: 5px 10px;
            margin-top: 15px;
            border-top: 1px solid var(--el-border-color-light);
            border-bottom: 1px solid var(--el-border-color-light);
            p {
                display: inline-block;
                width: 50%;
                border-right: 1px solid var(--el-border-color-light);
                &:nth-child(2) { border-right: none; }
                .num {
                    display: block;
                    font-size: 16px;
                    text-align: center;
                }
                .text {
                    display: block;
                    height: 14px;
                    margin-top: 8px;
                    font-size: 14px;
                    line-height: 14px;
                    color: #999999;
                    text-align: center;
                }
            }
        }
    }
    .menus {
        margin-top: 20px;
        li {
            width:
            160px; height: 48px;
            margin: 0 auto 8px;
            a {
                position: relative;
                display: flex;
                align-items: center;
                height: 48px;
                padding-left: 20px;
                font-size: 16px;
                line-height: 48px;
                color: var(--el-text-color-regular);
                text-align: left;
                span {
                    margin-left: 10px;
                }
            }

            &.active a {
                color: var(--color-white);
                background: var(--el-color-primary);
                border-radius: 8px 0 0 8px;
                &::after {
                    position: absolute;
                    right: 0;
                    bottom: 0;
                    display: block;
                    width: 0;
                    height: 0;
                    content: "";
                    border-top: 24px solid var(--el-bg-color-overlay);
                    border-bottom: 24px solid var(--el-bg-color-overlay);
                    border-left: 15px solid transparent;
                }
            }

        }
    }
}

.right-iframe {
    flex: 1;
    width: 100%;
    margin: 20px 0 20px 20px;
}
</style>
