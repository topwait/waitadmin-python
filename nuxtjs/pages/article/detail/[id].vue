<template>
    <NuxtLayout name="default">
        <template #container>
            <!-- Left -->
            <div class="w-[810px] mt-4 mr-5">
                <el-card class="!border-none card_body-padding-y0" shadow="never">
                    <div class="border-b border-br py-4">
                        <h1 class="font-medium text-[22px]">
                            {{ details.title }}
                        </h1>
                        <div class="mt-3 text-sm text-tx-secondary flex items-center flex-wrap">
                            <span v-if="details.category">
                                {{ details.category }}&nbsp;|&nbsp;
                            </span>
                            <span class="mr-5">{{ details.create_time }}</span>
                            <div class="flex items-center">
                                <icon name="el-icon-View" />
                                <span class="ml-1">{{ details.browse }}阅读量</span>
                            </div>
                        </div>
                    </div>

                    <div
                        v-if="details.intro"
                        class="text-sm text-tx-secondary bg-page mt-4 p-3 rounded-lg"
                    >
                        {{ details.intro }}
                    </div>

                    <div class="min-h-[300px] py-4" v-html="details.content"></div>

                    <div class="flex justify-center mt-[40px]">
                        <ElButton size="large" round @click="handleCollect()">
                            &nbsp;{{ details.is_collect ? '取消收藏' : '点击收藏' }}
                        </ElButton>
                    </div>

                    <div class="border-t border-br mt-[30px] py-4">
                        <div class="flex text-base text-tx-regular">
                            <span>上一篇：</span>
                            <NuxtLink
                                v-if="details.prev.id"
                                class="flex-1 text-primary-default hover-opacity"
                                :to="`/article/detail/${details.prev?.id}`"
                            >
                                {{ details.prev?.title }}
                            </NuxtLink>
                            <span v-else>暂无数据</span>
                        </div>
                        <div class="flex mt-2.5 text-base text-tx-regular">
                            <span>下一篇：</span>
                            <NuxtLink
                                v-if="details.next.id"
                                class="flex-1 text-primary-default hover-opacity"
                                :to="`/article/detail/${details.next?.id}`"
                            >
                                {{ details.next?.title }}
                            </NuxtLink>
                            <span v-else>暂无数据</span>
                        </div>
                    </div>
                </el-card>
            </div>

            <!-- Right -->
            <div class="w-[370px] mt-4">
                <Information
                    type="topping"
                    title="每日推荐"
                    :data="pageData.topping"
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
import articleApi from '~/api/article'
import Information from '../_components/Information.vue'

const route = useRoute()
const articleId = parseInt(String(route.params.id))

/**
 * 文章数据
 */
const { data: details, refresh } = useAsyncData(
    () => articleApi.detail(articleId),
    {
        default() {
            return {} as ArticleDetailResponse
        }
    }
)

/**
 * 页面数据
 */
const { data: pageData } = await useAsyncData(
    () => articleApi.pages(),
    {
        default() {
            return {} as ArticlePagesResponse
        }
    }
)

/**
 * 文章收藏
 */
const handleCollect = async () => {
    if (details.value.is_collect) {
        await articleApi.collect(articleId)
        feedback.msgSuccess('取消成功')
    } else {
        await articleApi.collect(articleId)
        feedback.msgSuccess('收藏成功')
    }
    await refresh()
}
</script>
