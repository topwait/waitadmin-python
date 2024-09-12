<template>
    <div class="layout-policy-widget">
        <div class="policy-menu">
            <div class="lists">
                <NuxtLink
                    class="menu-item"
                    :to="`/policy/${policyEnum.SERVICE}`"
                    :class="{ active: route.params.type === 'service' }"
                >
                    服务协议
                </NuxtLink>
                <NuxtLink
                    class="menu-item"
                    :to="`/policy/${policyEnum.PRIVACY}`"
                    :class="{ active: route.params.type === 'privacy' }"
                >
                    隐私协议
                </NuxtLink>
                <NuxtLink
                    class="menu-item"
                    :to="`/policy/${policyEnum.PAYMENT}`"
                    :class="{ active: route.params.type === 'payment' }"
                >
                    支付协议
                </NuxtLink>
                <NuxtLink
                    class="menu-item"
                    target="_blank"
                    :to="'/'"
                >
                    返回首页
                </NuxtLink>
            </div>
        </div>
        <div class="policy-body">
            <div class="richText" v-html="pageData.content"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { policyEnum } from '@/enums/app'
import appApi from '~/api/app/index'

const route = useRoute()

let type: any = route.params.type || policyEnum.SERVICE
type = [
    policyEnum.SERVICE,
    policyEnum.PRIVACY,
    policyEnum.PAYMENT
].includes(type) ? type : policyEnum.SERVICE

const { data: pageData } = await useAsyncData(
    () => appApi.policy(type),
    {
        default() {
            return {} as AppPolicyResponse
        }
    }
)
</script>

<style scoped lang="scss">
.layout-policy-widget {
    display: flex;
    width: 1200px;
    margin: 20px auto 0;

    .policy-menu .lists {
        width: 140px;
        margin-right: 20px;
        font-size: 14px;
        text-align: center;
        background-color: #fff;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        .menu-item {
            display: block;
            padding: 14px 0;
            font-weight: bold;
            color: #101010;
            cursor: pointer;
            border-bottom: 1px #eee solid;
            border-radius: 8px;
            &:last-child {
                border-bottom: none;
            }
            &:hover {
                color: var(--el-color-primary);
                opacity: .8;
            }
            &.active {
                color: #fff;
                background-color: var(--el-color-primary);
            }
        }
    }

    .policy-body {
        box-sizing: border-box;
        width: 100%;
        min-height: 500px;
        padding: 20px;
        background-color: var(--color-white);
        border: 1px solid #f0f0f0;
        border-radius: 8px;
    }

    .richText {
        img {
            display: inline-block;
            max-width: 100%;
            max-height: 100%;
        }
    }
}
</style>