import type { FetchResponse } from 'ofetch'

declare module 'ofetch' {
    interface FetchOptions {
        url?: string
        requestOptions?: RequestOptions
    }

    interface RequestOptions {
        // 请求接口的前缀
        apiPrefix?: string
        // 返回数据进行处理
        isTransformResponse?: boolean
        // 是否返回默认数据
        isReturnDefaultResponse?: boolean
        // POST请求下Data
        isParamsToData?: boolean
        // 是否自动携带Token
        withToken?: boolean
        // 是否弹出提示框
        withHints?: boolean
        // 是否显示加载框
        isShowLoading?: boolean
        // 请求前的拦截器
        requestInterceptorsHook?(options: FetchOptions): FetchOptions
        // 请求后的拦截器
        responseInterceptorsHook?(response: FetchResponse<any>, options: FetchOptions): any
        // 请求错误拦截器
        responseInterceptorsCatchHook?: (error: any) => void
    }

    interface RequestEventStreamOptions extends Partial<RequestOptions> {
        onstart?: (reader: ReadableStreamDefaultReader<Uint8Array>) => void
        onmessage?: (value: string) => void
        onclose?: () => void
    }

    interface FileParams {
        file: File
        name?: string
        data?: any
    }
}
