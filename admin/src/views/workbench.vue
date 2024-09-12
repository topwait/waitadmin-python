<template>
    <div v-loading="pageLoading">
        <el-row :gutter="20">
            <el-col :xs="24"
                    :sm="12"
                    :md="6"
                    :lg="6"
                    :xl="6"
                    :span="6"
                    v-for="(item, index) in workbenchData.today"
                    :key="index"
            >
                <el-card class="mb-4 !border-none" shadow="never">
                    <template #header>
                        <div class="flex items-center justify-between">
                            <span>{{ item.name }}</span>
                        </div>
                    </template>
                    <div class="flex items-center justify-between py-2">
                        <span class="text-5xl font-medium">{{ item.value }}</span>
                        <el-image class="w-[48px] h-[48px]" :src="item.icon"  />
                    </div>
                    <div class="flex items-center mb-3">
                        <span>昨日: {{ item.total }}</span>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <div class="lg:flex">
            <!-- 常用功能 -->
            <el-card class="flex-1 lg:mr-4 mb-4 !border-none" shadow="never">
                <template #header>
                    <span>常用功能</span>
                </template>
                <ul class="shortcut flex flex-wrap">
                    <li
                        v-for="(item, index) in workbenchData.shortcut"
                        :key="index"
                        class="md:w-[25%] w-1/4 flex flex-col items-center"
                    >
                        <router-link :to="item.path" class="flex flex-col items-center">
                            <div class="icon">
                                <icon :name="item.icon" size="30"/>
                            </div>
                            <p class="mt-1">{{ item.name }}</p>
                        </router-link>
                    </li>
                </ul>
            </el-card>
            <!-- 待办事项 -->
            <el-card class="flex-1 lg:mr-4 mb-4 !border-none" shadow="never">
                <template #header>
                    <div class="flex items-center justify-between">
                        <span>待办事项</span>
                    </div>
                </template>
                <ul class="backlogs">
                    <li v-for="(item, index) in workbenchData.backlogs" :key="index">
                        <router-link :to="item.path">
                            <h3>{{ item.name }}</h3>
                            <p>{{ item.value }}</p>
                        </router-link>
                    </li>
                </ul>
            </el-card>
            <!-- 版本信息 -->
            <el-card class="mb-4 !border-none" shadow="never">
                <template #header>
                    <div class="flex items-center justify-between">
                        <span>版本信息</span>
                    </div>
                </template>
                <div class="p-[5px]">
                    <table>
                        <colgroup>
                            <col width="100"/>
                        </colgroup>
                        <tbody>
                            <tr>
                                <td>当前版本</td>
                                <td>v{{ workbenchData.version.version }}</td>
                            </tr>
                            <tr>
                                <td>基于框架</td>
                                <td>{{ workbenchData.version.frame }}</td>
                            </tr>
                            <tr>
                                <td>主要特色</td>
                                <td>{{ workbenchData.version.tones }}</td>
                            </tr>
                            <tr>
                                <td>获取渠道</td>
                                <td>
                                    <a :href="workbenchData.version.official" target="_blank">
                                        <el-button type="primary">官方网站</el-button>
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </el-card>
        </div>

        <div class="lg:flex">
            <el-card class="flex-1 lg:mr-4 mb-4 !border-none" shadow="never">
                <template #header>
                    <span>访问量趋势图</span>
                </template>
                <v-charts
                    style="height: 350px"
                    :option="chartOption.visitor"
                    :autoresize="true"
                />
            </el-card>
            <el-card class="flex-1 mb-4 !border-none" shadow="never">
                <template #header>
                    <span>访问量趋势图</span>
                </template>
                <v-charts
                    style="height: 350px"
                    :option="chartOption.website"
                    :autoresize="true"
                />
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import vCharts from 'vue-echarts'
import appApi from '@/api/app'

// 页面加载中
const pageLoading: Ref<boolean> = ref(true)

// 控制台数据
const workbenchData: Ref<any> = ref({
    today: [],    // 今日数据
    shortcut: [], // 快捷方式
    backlogs: [], // 待办事项
    version: {},  // 版本信息
})

// 趋势图配置
const chartOption = ref({
    // 访客趋势图
    visitor: {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    width: 1,
                    color: '#019680',
                },
            },
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [],
            splitLine: {
                show: true,
                lineStyle: {
                    width: 1,
                    type: 'solid',
                    color: 'rgba(226,226,226,0.5)',
                },
            },
            axisTick: {
                show: false,
            },
        },
        yAxis: [
            {
                type: 'value',
                splitNumber: 4,
                axisTick: {
                    show: false,
                },
                splitArea: {
                    show: true,
                    areaStyle: {
                        color: ['rgba(255,255,255,0.2)', 'rgba(226,226,226,0.2)'],
                    },
                },
            },
        ],
        grid: { left: '1%', right: '1%', top: '2  %', bottom: 0, containLabel: true },
        series: [
            {
                smooth: true,
                data: [],
                type: 'line',
                areaStyle: {},
                itemStyle: {
                    color: '#5ab1ef',
                },
            }

        ],
    },
    // 浏览器趋势图
    website: {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: '50%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
})

const getWorkbenchData = () => {
    appApi.workbench().then((res: any) => {
        workbenchData.value.today = res.today
        workbenchData.value.backlogs = res.backlogs
        workbenchData.value.shortcut = res.shortcut
        workbenchData.value.version = res.version

        chartOption.value.visitor.xAxis.data = res.echartsVisitor.date
        chartOption.value.visitor.series[0].data = res.echartsVisitor.list
        chartOption.value.website.series[0].data = res.echartsWebsite
        pageLoading.value = false
    })
}

onMounted(() => {
    getWorkbenchData()
})
</script>

<style scoped lang="scss">
:deep(.el-card) {
    .el-card__header {
        padding: 12px 15px;
        font-size: 13px;
        font-weight: bold;
    }
    .el-card__body {
        padding: 10px 15px;
    }
}

table {
    box-sizing: border-box;
    display: table;
    text-indent: initial;
    border-spacing: 0;
    border-collapse: collapse;
    border-color: gray;
    unicode-bidi: isolate;
    td {
        position: relative;
        min-height: 20px;
        padding: 10px 15px;
        font-size: 14px;
        line-height: 20px;
        color: var(--el-text-color-regular);
        border-color: var(--el-border-color-lighter);
        border-style: solid;
        border-width: 1px;
    }
}

.shortcut {
    li {
        padding: 5px;
        a {
            display: block;
            width: 100%;
            color: var(--el-text-color-regular);
            text-align: center;
        }
        .icon {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 60px;
            font-size: 30px;
            line-height: 60px;
            text-align: center;
            background-color: var(--el-bg-color-light);
            border-radius: 2px;
            transition: all 0.3s;
            &:hover {
                background-color: var(--el-bg-color-lighter);
            }
        }
    }
}

.backlogs {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    li {
        width: 50%;
        padding: 5px;
        a {
            display: block;
            padding: 10px 15px;
            color: var(--el-text-color-regular);
            background-color: var(--el-bg-color-light);
            border-radius: 2px;
            transition: all 0.3s;
            h3 {
                padding-bottom: 10px;
                font-size: 13px;
            }
            p { font-size: 24px;
                font-style: normal;
                font-weight: 400;
                color: var(--el-color-primary);
            }
            &:hover {
                background-color: var(--el-bg-color-lighter);
            }
        }
    }
}
</style>
