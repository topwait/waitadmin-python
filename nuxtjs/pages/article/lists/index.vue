<template>
    <NuxtLayout name="default">
        <template #container>
            <!-- Left -->
            <div v-loading="pager.loading" class="w-[810px] mt-4 mr-5">
                <el-card class="!border-none card_body-padding-y0" shadow="never">
                    <template #header>
                        <span v-if="!queryParams.keyword" class="font-bold">文章列表</span>
                        <span v-else class="font-bold">查找 "{{ queryParams.keyword }}"</span>
                    </template>
                    <ul>
                        <li
                            v-for="(item, index) in pager.lists"
                            :key="index"
                            class="flex py-5 border-b border-br"
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
                    <template v-if="pager?.lists.length <= 0 && !pager.loading">
                        <el-empty
                            v-if="pager?.lists.length <= 0 && !pager.loading"
                            description="暂无资讯"
                            :image-size="200"
                        />
                        <div class="flex justify-end my-4">
                            <paging
                                v-model="pager"
                                layout="prev, pager, next"
                                @change="queryLists"
                            />
                        </div>
                    </template>
                </el-card>
            </div>

            <!-- Right -->
            <div class="w-[370px] mt-4">
                <el-card class="!border-none" shadow="never">
                    <el-input
                        v-model="queryParams.keyword"
                        size="large"
                        placeholder="请输入搜索关键词"
                        :prefix-icon="Search"
                        @keyup.enter="resetPaging"
                    />
                </el-card>

                <Information
                    class="mt-4"
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
import { Search } from '@element-plus/icons-vue'
import articleApi from '~/api/article'
import Information from '../_components/Information.vue'

// 页面数据
const { data: pageData } = await useAsyncData(
    () => articleApi.pages(),
    {
        default() {
            return {} as ArticlePagesResponse
        }
    }
)

// 查询参数
const queryParams = reactive({
    keyword: ''
})

// 分页查询
const { pager, queryLists, resetPaging } = usePaging<ArticleListsResponse>({
    fetchFun: articleApi.lists,
    params: queryParams
})

onMounted(async () => {
    await queryLists()
})
</script>
