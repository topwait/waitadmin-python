import { ElMessage, ElMessageBox, ElTree } from 'element-plus'
import { usePaging } from '@/hooks/usePaging'
import feedback from '@/utils/feedback'
import attachApi from '@/api/attach'

export function useCate(type: number): any {
    const cateId: Ref<number> = ref<number>(0)
    const cateLists: Ref<any[]> = ref<any[]>([])
    const treeRef: Ref = shallowRef<InstanceType<typeof ElTree>>()

    // 获取分组
    const getCateLists = async (): Promise<void> => {
        const item: any[] = [
            { id: -1, name: '全部' },
            { id: 0, name: '未分组' }
        ]
        cateLists.value = await attachApi.cateLists(type)
        cateLists.value.unshift(...item)
        setTimeout((): void => {
            treeRef.value?.setCurrentKey(cateId.value)
        }, 0)
    }

    // 添加分组
    const handleAddCate = async (value: string): Promise<void> => {
        await attachApi.cateAdd(type, value)
        await getCateLists()
        feedback.msgSuccess('添加成功')
    }

    //  编辑分组
    const handleRenameCate = async (value: string, id: number): Promise<void> => {
        await attachApi.cateRename(type, value, id)
        await getCateLists()
        feedback.msgSuccess('编辑成功')
    }

    // 删除分组
    const handleDeleteCate = async (id: number): Promise<void> => {
        await attachApi.cateDelete(type, id)
        await getCateLists()
        feedback.msgSuccess('删除成功')
    }

    // 切换分组
    const handleSwitchCate = async (item: any): Promise<void> => {
        cateId.value = item.id
    }

    // 导出函数
    return {
        treeRef,
        cateId,
        cateLists,
        getCateLists,
        handleAddCate,
        handleRenameCate,
        handleDeleteCate,
        handleSwitchCate
    }
}

export function useFile(
    type: number,
    cateId: Ref<number>,
    limit: Ref<number>,
    size: Ref<number>,
    data?: Ref<Record<string, any>>
): any {
    // 移动的ID
    const moveId: globalThis.Ref<number> = ref<number>(0)
    // 移动弹窗
    const movePo: globalThis.Ref<boolean> = ref<boolean>(false)

    // 已选素材
    const select: globalThis.Ref<any[]> = ref<any[]>([])

    // 搜索参数
    const searchParams: any = reactive({
        type: type,
        cid: cateId,
        keyword: '',
        ...data?.value
    })

    // 分页查询
    const { pager, queryLists, resetPaging } = usePaging({
        fetchFun: attachApi.albumLists,
        params: searchParams,
        firstLoading: true,
        size: size.value
    })

    // 附件获取
    const getFileLists = async (): Promise<void> => {
        await queryLists()
    }

    // 附件移动
    const handleMoveFile = async (): Promise<void> => {
        const ids: number[] = select.value.map((item: any) => item.id)
        await attachApi.albumMove(ids, moveId.value)
        moveId.value = 0
        movePo.value = false
        await queryLists()
        selectClear()
    }

    // 附件命名
    const handleRenameFile = async (id: number, name: string): Promise<void> => {
        ElMessageBox.prompt('', '文件重命名', { inputValue: name })
            .then(async (res): Promise<void> => {
                if (!res.value) {
                    ElMessage({
                        type: 'error',
                        message: '文件名称不可为空'
                    })
                } else {
                    await attachApi.albumRename(id, res.value)
                    await queryLists()
                }
            }).catch((): void => { })
    }

    // 附件删除
    const handleDeleteFile = async (id?: number[]): Promise<void> => {
        await feedback.confirm('您确定要删除吗?,删除后不恢复,请谨慎操作!')
            .then(async (): Promise<void> => {
                const ids: number[] = id ? id : select.value.map((item: any) => item.id)
                await attachApi.albumDelete(ids)
                await queryLists()
                selectClear()
            }).catch((): void => { })
    }

    // 是否选中
    const isSelect = (id: number) => {
        return !!select.value.find((item: any): boolean => item.id === id)
    }

    // 选择附件
    const selectFile = (item: any): void => {
        const index: number = select.value.findIndex((items: any): boolean => items.id === item.id)
        if (index !== -1) {
            select.value.splice(index, 1)
            return
        }
        if (select.value.length === limit.value) {
            if (limit.value === 1) {
                select.value = []
                select.value.push(item)
                return
            }
            ElMessage.warning('已达到选择上限')
            return
        }
        select.value.push(item)
    }

    // 选择清除
    const selectClear = (): void => {
        select.value = []
    }

    // 选择取消
    const selectCancel = (id: number): void => {
        select.value = select.value.filter((item: any): boolean => item.id !== id)
    }

    // 导出函数
    return {
        pager,
        movePo,
        moveId,
        select,
        searchParams,
        isSelect,
        selectFile,
        selectClear,
        selectCancel,
        resetPaging,
        getFileLists,
        handleMoveFile,
        handleRenameFile,
        handleDeleteFile
    }
}
