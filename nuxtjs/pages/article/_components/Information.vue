<template>
    <div>
        <el-card v-if="type === 'topping'" class="!border-none" shadow="never">
            <template #header>
                <span class="font-bold">{{ title }}</span>
            </template>
            <ul class="py-[5px]">
                <li
                    v-for="(item, index) in data"
                    :key="index"
                    class="py-2"
                >
                    <NuxtLink
                        :to="'/article/detail/' + item.id"
                        class="text-base line-clamp-1 hover-primary"
                    >
                        <span class="text-[#dab26b]">[{{ item.category }}] · </span>
                        {{ item.title }}
                    </NuxtLink>
                </li>
            </ul>
        </el-card>

        <el-card v-if="type === 'ranking'" class="!border-none" shadow="never">
            <template #header>
                <span class="font-bold">{{ title }}</span>
            </template>
            <ul class="ranking">
                <li
                    v-for="(item, index) in data"
                    :key="index"
                    class="flex py-5"
                >
                    <span>{{ index < 9 ? '0' : ''}}{{ index + 1 }}</span>
                    <NuxtLink :to="'/article/detail/' + item.id" class="block w-[560px]">
                        <h3 class="text-lg font-bold line-clamp-1 hover-primary">
                            {{ item.title }}
                        </h3>
                        <div class="text-sm text-tx-secondary line-clamp-2 mt-[5px]">
                            {{ item.intro }}
                        </div>
                    </NuxtLink>
                </li>
            </ul>
        </el-card>

        <ElCarousel
            v-if="type === 'adv'"
            class="w-full"
            trigger="click"
            height="185px"
        >
            <ElCarouselItem v-for="(item, index) in data" :key="index">
                <NuxtLink :to="item.url" :target="item.target" :title="item.title">
                    <ElImage
                        class="w-full h-full rounded-[8px] overflow-hidden"
                        :src="item.image"
                    />
                </NuxtLink>
            </ElCarouselItem>
        </ElCarousel>
    </div>
</template>

<script setup lang="ts">
defineProps({
    type: {
        type: String
    },
    title: {
        type: String,
        default: ''
    },
    data: {
        type: Array<any>,
        default: () => {
            return []
        }
    }
})
</script>

<style scoped lang="scss">
:deep(.el-card__body) {
    padding-top: 0;
    padding-bottom: 0;
}

.ranking {
    li span {
        width: 40px;
        height: 61px;
        margin-right: 10px;
        font-family: Mangal, serif;
        font-size: 36px;
        font-weight: bold;
        line-height: 61px;
        color: #dbdbdb;
    }
}

.lately {
    padding: 5px 0;
    li a {
        display: block;
         height: 20px;
         overflow: hidden;
         font-size: 14px;
         line-height: 20px;
         color: #333333;
         text-overflow: ellipsis;
         white-space: nowrap;
        span {
            color: #dab26b;
        }
    }
}
</style>
