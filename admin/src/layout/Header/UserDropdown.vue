<template>
    <el-dropdown class="px-2.5 h-full" @command="handleCommand">
        <div class="flex items-center">
            <el-avatar :size="30" :src="userInfo.avatar" />
            <div class="ml-2 mr-1">{{ userInfo.nickname }}</div>
            <icon name="el-icon-ArrowDown" />
        </div>
        <template #dropdown>
            <el-dropdown-menu>
                <router-link to="/auth/account/setting">
                    <el-dropdown-item>个人设置</el-dropdown-item>
                </router-link>
                <el-dropdown-item :divided="true" command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
</template>

<script setup lang="ts">
import feedback from '@/utils/feedback'
import useUserStore from '@/stores/modules/user'

const userStore = useUserStore()

const userInfo = computed(() => userStore.users)

const handleCommand = async (command: string) => {
    switch (command) {
        case 'logout':
            await feedback.confirm('确定退出登录吗？')
            userStore.logout()
    }
}
</script>
