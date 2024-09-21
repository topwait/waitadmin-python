import { reactive, toRaw } from 'vue'

// 分页钩子函数
interface Options {
    page?: number
    size?: number
    params?: Record<any, any>
    firstLoading?: boolean
    fetchFun: (_arg: any) => Promise<any>
}

export function usePaging(options: Options): any {
    // 读取参数
    const { page = 1, size = 15, fetchFun, params = {}, firstLoading = false } = options

    // 初始参数
    const paramsInit: Record<any, any> = Object.assign({}, toRaw(params))

    // 分页数据
    const pager: any = reactive({
        page,
        size,
        total: 0,
        lists: [] as any[],
        extend: {} as Record<string, any>,
        loading: firstLoading
    })

    // 请求分页接口
    const queryLists = async (): Promise<any> => {
        pager.loading = true
        try {
            const res = await fetchFun({
                ...filterNullObj(params),
                page_no: pager.page,
                page_size: pager.size
            })
            if (!res?.lists) {
                pager.lists = res
            } else {
                pager.total = res?.total
                pager.lists = res?.lists
                pager.extend = res?.extend
            }
            return await Promise.resolve(res)
        } catch (err) {
            return await Promise.reject(err)
        } finally {
            pager.loading = false
        }
    }

    // 重置为第一页
    const resetPaging = async (): Promise<void> => {
        pager.page = 1
        await queryLists()
    }

    // 重置查询参数
    const resetParams = async (): Promise<void> => {
        Object.keys(paramsInit).forEach((item: string): void => {
            params[item] = paramsInit[item]
        })
        await queryLists()
    }

    // 过滤对象空字段
    const filterNullObj = (obj: any) => {
        return Object.keys(obj).reduce((acc: any, key: string) => {
            if (obj[key] !== '' && obj[key] !== null && obj[key] !== undefined) {
                acc[key] = obj[key]
            }
            return acc
        }, {})
    }

    return {
        pager,
        queryLists,
        resetParams,
        resetPaging
    }
}
