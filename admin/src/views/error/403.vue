<template>
    <div class="error404">
        <error code="403" title="抱歉,您的权限不足！" :show-btn="false">
            <template #content>
                <div class="flex justify-center">
                    <img class="w-[150px] h-[150px]" src="@/assets/images/perm_no.png" alt="WaitAdmin" />
                </div>
            </template>
        </error>
    </div>
</template>

<script setup lang="ts">
import Error from './components/error.vue'
</script>
