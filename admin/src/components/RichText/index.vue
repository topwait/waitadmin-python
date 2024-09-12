<template>
    <div class="border border-br flex flex-col" :style="styles">
        <toolbar
            class="border-b border-br"
            :editor="editorRef"
            :defaultConfig="toolbarConfig"
            :mode="mode"
        />
        <w-editor
            class="overflow-y-auto flex-1"
            v-model="valueHtml"
            :defaultConfig="editorConfig"
            :mode="mode"
            @onCreated="handleCreated"
        />
        <material-picker
            ref="materialPickerRef"
            :type="'image'"
            :limit="-1"
            :upload-hidden="true"
            @change="selectChange"
        />
    </div>
</template>

<script setup lang="ts">
import '@wangeditor/editor/dist/css/style.css'
import type { CSSProperties } from 'vue'
import type { IEditorConfig, IToolbarConfig } from '@wangeditor/editor'
import { Editor as WEditor, Toolbar } from '@wangeditor/editor-for-vue'
import MaterialPicker from '@/components/Material/picker.vue'
import toolsUtil from '@/utils/tools'

const emit = defineEmits<{
    (event: 'update:modelValue', value: string): void
}>()

const props = withDefaults(
    defineProps<{
        modelValue?: string
        mode?: 'default' | 'simple'
        height?: string | number
        width?: string | number
        toolbarConfig?: Partial<IToolbarConfig>
    }>(),
    {
        modelValue: '',
        mode: 'default',
        height: '100%',
        width: 'auto',
        toolbarConfig: () => ({})
    }
)

let insertFn: any
const fileType = ref('')
const editorRef = shallowRef()
const materialPickerRef = shallowRef<InstanceType<typeof MaterialPicker>>()

const editorConfig: Partial<IEditorConfig> = {
    MENU_CONF: {
        uploadImage: {
            customBrowseAndUpload(insert: any) {
                fileType.value = 'image'
                materialPickerRef.value?.showPopup(-1)
                insertFn = insert
            }
        },
        uploadVideo: {
            customBrowseAndUpload(insert: any) {
                fileType.value = 'video'
                materialPickerRef.value?.showPopup(-1)
                insertFn = insert
            }
        }
    }
}

const styles = computed<CSSProperties>(() => ({
    height: toolsUtil.addUnit(props.height),
    width: toolsUtil.addUnit(props.width)
}))

const valueHtml = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})

const selectChange = (fileUrl: string[]) => {
    fileUrl.forEach((item: any) => {
        insertFn(item.url)
    })
}

const handleCreated = (editor: any) => {
    editorRef.value = editor
}

onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor === null) {
        return
    }
    editor.destroy()
})
</script>

<style lang="scss">
.w-e-text-container {
    [data-slate-editor] ul {
        list-style: disc;
    }

    [data-slate-editor] ol {
        list-style: decimal;
    }
}

.w-e-full-screen-container {
    z-index: 9999;
}

h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.17em; }
h4 { font-size: 1em; }
h5 {  font-size: 0.83em; }

h1,
h2,
h3,
h4,
h5 {  font-weight: bold; }
</style>
