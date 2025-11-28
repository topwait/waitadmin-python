import { reactive, toRaw } from 'vue'

// 分页钩子函数
interface Options {
    page?: number;
    size?: number;
    params?: Record<string, any>;
    firstLoading?: boolean;
    fetchFun: (_arg: any) => Promise<any>;
}

export function usePaging<T = any>(options: Options) {
    // 读取参数
    const fetchFun = options.fetchFun
    const page: number = options.page || 0
    const size: number = options.size || 0
    const params: Record<string, any> = options.params || {}
    const firstLoading: boolean = options.firstLoading || false

    // 初始参数
    const paramsInit: Record<any, any> = Object.assign({}, toRaw(params))

    // 分页数据
    const pager = reactive({
        page,
        size,
        total: 0,
        lists: [] as Array<T>,
        extend: {} as Record<string, any>,
        loading: firstLoading
    })

    // 请求分页接口
    const queryLists = async (): Promise<any> => {
        pager.loading = true
        try {
            const res = await fetchFun({
                ...filterNullObj(params),
                page_no: pager.page <= 0 ? pager.page : '',
                page_size: pager.size <= 15 ? pager.size : ''
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
