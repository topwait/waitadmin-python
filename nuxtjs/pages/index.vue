<template>
    <NuxtLayout name="default">
        <template #container>
            <!-- Left -->
            <div class="w-[810px] mt-4 mr-5">
                <div class="w-[810px] h-[364px]">
                    <el-carousel
                        class="w-full"
                        trigger="click"
                        height="364px"
                    >
                        <el-carousel-item v-for="(item, index) in pageData.banner" :key="index">
                            <NuxtLink :to="item.url" :target="item.target" :title="item.title">
                                <el-image
                                    class="w-full h-full rounded-[8px] overflow-hidden"
                                    :src="item.image"
                                />
                            </NuxtLink>
                        </el-carousel-item>
                    </el-carousel>
                </div>
                <el-card class="!border-none card_body-padding-y0 mt-4" shadow="never">
                    <template #header>
                        <span class="font-bold">每日推荐</span>
                    </template>
                    <ul>
                        <li
                            v-for="(item, index) in pageData.topping"
                            :key="index"
                            :class="pageData.topping.length > index+1 ? 'border-b' : ''"
                            class="flex py-5 border-br"
                        >
                            <NuxtLink
                                :to="'/article/detail/' + item.id"
                                class="block w-[200px] h-[132px]"
                            >
                                <ElImage
                                    class="w-full h-full rounded-[4px]"
                                    :src="item.image"
                                />
                            </NuxtLink>
                            <div class="w-[560px] ml-4">
                                <NuxtLink
                                    :to="'/article/detail/' + item.id"
                                    class="block hover-primary"
                                >
                                    <h3 class="text-lg font-bold line-clamp-1">{{ item.title }}</h3>
                                </NuxtLink>
                                <div class="text-sm text-tx-secondary line-clamp-2 mt-[5px] min-h-[39px]">
                                    {{ item.intro }}
                                </div>
                                <el-tag class="my-2">{{ item.category }}</el-tag>
                                <div class="text-sm text-tx-secondary">
                                    <span class="mr-7">{{ item.create_time }}</span>
                                    <span>{{ item.browse }} 阅读量</span>
                                </div>
                            </div>
                        </li>
                    </ul>
                </el-card>
            </div>

            <!-- Right -->
            <div class="w-[370px] mt-4">
                <Information
                    type="topping"
                    title="最近更新"
                    :data="pageData.everyday"
                />

                <Information
                    class="mt-4"
                    type="ranking"
                    title="排名榜单"
                    :data="pageData.ranking"
                />

                <Information
                    class="mt-4"
                    type="adv"
                    :data="pageData.adv"
                />
            </div>
        </template>
    </NuxtLayout>
</template>

<script setup lang="ts">
import appApi from '~/api/app'
import Information from './article/_components/Information.vue'

// 页面数据
const { data: pageData } = await useAsyncData(
    () => appApi.homing(),
    {
        default() {
            return {} as AppHomingResponse
        }
    }
)
</script>
