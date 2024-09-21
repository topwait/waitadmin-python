<template>
    <div>
        <video-play
            ref="playerRef"
            v-bind="options"
            :src="src"
            @play="onPlay"
            @pause="onPause"
            @timeupdate="onTimeupdate"
            @canplay="onCanplay"
        />
    </div>
</template>

<script setup lang="ts">
import { reactive, shallowRef } from 'vue'
import 'vue3-video-play/dist/style.css'
import VideoPlay from 'vue3-video-play/dist/index.mjs'

const props = defineProps({
    src: {
        type: String,
        required: true,
    },
    width: String,
    height: String,
    poster: String,
})

const attrs = useAttrs()
const playerRef = shallowRef()
const options = reactive({
    // 主题
    color: 'var(--el-color-primary)',
    // 静音
    muted: false,
    // 缩放
    webFullScreen: false,
    // 播放倍速
    speedRate: ['0.75', '1.0', '1.25', '1.5', '2.0'],
    // 自动播放
    autoPlay: false,
    // 循环播放
    loop: false,
    // 镜像画面
    mirror: false,
    // 关灯模式
    lightOff: false,
    // 默认音量大小
    volume: 0.5,
    // 是否显示控制器
    control: true,
    // 视频名称
    title: '',
    // 封面
    poster: '',
    ...props,
    ...attrs
})

const play = () => {
    playerRef.value.play()
}

const pause = () => {
    playerRef.value.pause()
}

const onPlay = () => {
    // console.log(event, '播放')
}
const onPause = () => {
    // console.log(event, '暂停')
}

const onTimeupdate = () => {
    // console.log(event, '时间更新')
}

const onCanplay = () => {
    // console.log(event, '可以播放')
}

defineExpose({
    play,
    pause,
})
</script>
