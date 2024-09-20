<template>
    <div class="materials">
        <el-card class="!border-none" shadow="never">
            <el-tabs v-model="activeTab">
                <el-tab-pane
                    v-for="item in tabsMap"
                    :label="item.name"
                    :name="item.type"
                    :index="item.type"
                    :key="item.type"
                    lazy
                >
                    <material
                        mode="page"
                        :type="item.type"
                        :limit="-1"
                        :page-size="20"
                        file-size="120px"
                    />
                </el-tab-pane>
            </el-tabs>
        </el-card>
    </div>
</template>

<script setup lang="ts">
const activeTab = ref('image')
const tabsMap = [
    {
        type: 'image',
        name: '图片'
    },
    {
        type: 'video',
        name: '视频'
    },
    {
        type: 'audio',
        name: '音频'
    },
    {
        type: 'packs',
        name: '压缩'
    },
    {
        type: 'docs',
        name: '文档'
    }
]
</script>

<style scoped lang="scss">
.materials {
    min-width: 700px;
    height: calc(100vh - 117px);
    :deep(.el-card) {
      height: 100%;
      .el-card__body {
          padding-bottom: 10px;
          height: 100%;
      }
    }
    :deep(.el-tabs) {
        height: 100%;
        .el-tab-pane {
          height: 100%;
        }
    }
}
</style>
