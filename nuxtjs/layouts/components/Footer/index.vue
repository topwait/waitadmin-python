<template>
    <footer class="layout-footer">
        <div class="container">
            <div class="flex justify-center py-[30px]">
                <div class="mii">
                    <div class="nav">
                        <NuxtLink :to="`/policy/${policyEnum.SERVICE}`">用户协议</NuxtLink>
                        <NuxtLink :to="`/policy/${policyEnum.PRIVACY}`">隐私政策</NuxtLink>
                        <NuxtLink to="https://www.waitadmin.cn/docs">开发文档</NuxtLink>
                        <NuxtLink to="tps://www.waitadmin.cn">源码下载</NuxtLink>
                    </div>
                    <p>
                        {{ pcConfig.description }}
                    </p>
                </div>
                <div class="contact">
                    <img src="https://www.waitadmin.cn/static/frontend/images/qr_qq.png" alt="" />
                    <p>官方Q群</p>
                </div>
            </div>

            <div class="copyright">
                {{ websiteConfig.copyright }}
                <template v-if="websiteConfig.icp">
                    | <NuxtLink to="https://beian.miit.gov.cn/" rel="nofollow" target="_blank">
                        {{ websiteConfig.icp }}
                    </NuxtLink>
                </template>
                <template v-if="websiteConfig.pcp">
                    | <NuxtLink to="https://beian.miit.gov.cn/" rel="nofollow" target="_blank">
                        {{ websiteConfig.pcp }}
                    </NuxtLink>
                </template>
            </div>
        </div>
    </footer>
</template>

<script lang="ts" setup>
import { policyEnum } from '~/enums/app'
import useAppStore from '~/stores/app'

const appStore = useAppStore()
const pcConfig = appStore.getPcConfig
const websiteConfig = appStore.getWebsiteConfig
</script>

<style scoped lang="scss">
.layout-footer {
    width: 100%;
    margin-top: 30px;
    text-align: center;
    background: #282b2f;
    .container {
        width: 1200px;
        margin: 0 auto;
    }
    .mii {
        width: 600px;
        margin-right: 40px;
        overflow: hidden;
        .nav {
           display: flex;
           a {
                margin-right: 80px;
                font-size: 17px;
                color: var(--el-text-color-secondary);
                text-align: center;
                &:hover {
                    color: var(--color-white);
                }
           }
        }
        p {
            margin: 20px auto 0;
            overflow: hidden;
            font-size: 15px;
            line-height: 30px;
            color: var(--el-text-color-regular);
            text-align: justify;
        }
    }
    .contact {
        img {
            width: 130px;
            height: 130px;
            margin: 0 30px;
            border-radius: 3px;
        }
        p {
            margin-top: 10px;
            font-size: 16px;
            color: var(--color-white);
        }
    }
    .copyright {
        margin: 0 auto;
        overflow: hidden;
        font-size: 15px;
        line-height: 70px;
        color: var(--el-text-color-regular);
        text-align: center;
        background: #282b2f;
        border-top: 1px dashed #444649;
    }
}
</style>
