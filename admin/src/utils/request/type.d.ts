import 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'

declare module 'axios' {
    interface AxiosRequestConfig {
        retryCount?: number
        axiosHooks?: AxiosHooks
        requestOptions: RequestOptions
    }
}

export interface RequestOptions {
    isParamsToData: boolean
    isTransformResponse: boolean
    isReturnDefaultResponse: boolean
    ignoreCancelToken: boolean
    withToken: boolean
    urlPrefix: string
    retryCount: number
    isOpenRetry: boolean
    showProgress: boolean
}

export interface AxiosHooks {
    requestInterceptorsHook?: (config: AxiosRequestConfig) => AxiosRequestConfig
    requestInterceptorsCatchHook?: (error: Error) => void
    responseInterceptorsHook?: (
        response: AxiosResponse<RequestData<T>>
    ) => AxiosResponse<RequestData> | RequestData | T
    responseInterceptorsCatchHook?: (error: AxiosError) => void
}

export interface RequestData<T = any> {
    code: number
    show: boolean
    msg: string
    data: T
}

export interface FileParams {
    name?: string
    file: File
    data?: any
    header?: any
}
