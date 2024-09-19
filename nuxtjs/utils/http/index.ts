import type { FetchOptions } from 'ofetch'
import { ElLoading } from 'element-plus'
import { merge } from 'lodash-es'
import { Request } from './request'
import { errorEnum } from '~/enums/errors'
import useUserStore from '~/stores/user'
import feedback from '~/utils/feedback'
import config from '~/config'

let loadingInstance: any = null

export function createRequest(opt?: Partial<FetchOptions>): Request {
    const userStore = useUserStore()

    const defaultOptions: FetchOptions = {
        retry: config.reqRetry,
        baseURL: config.baseUrl,
        headers: {
            Version: String(config.version),
            Terminal: String(config.terminal)
        },
        requestOptions: {
            apiPrefix: config.urlPrefix,
            withToken: true,
            withHints: false,
            isShowLoading: false,
            isParamsToData: true,
            isTransformResponse: true,
            isReturnDefaultResponse: false,
            requestInterceptorsHook(options: any) {
                // 取出配置
                const apiPrefix: string = options.requestOptions?.apiPrefix || ''
                const withToken: boolean = options.requestOptions?.withToken || false
                const isShowLoading: boolean = options.requestOptions?.isShowLoading || false
                const isParamsToData: boolean = options.requestOptions?.isParamsToData || false

                // 拼接前缀
                if (apiPrefix) {
                    options.url = `${apiPrefix}${options.url}`
                }

                // 请求参数
                const params = options.params || {}
                if (isParamsToData && !Reflect.has(options, 'body') && options.method?.toUpperCase() === 'POST') {
                    options.body = params
                    options.params = {}
                }

                // 头部参数
                const headers: any = options.headers || {}
                if (withToken) {
                    const token: string = userStore.token || ''
                    headers.Authorization = 'Bearer ' + token
                }
                options.headers = headers

                // 开启加载中
                if (isShowLoading) {
                    loadingInstance = ElLoading.service({
                        fullscreen: true,
                        lock: true,
                        text: '加载中',
                        background: 'rgba(0,0,0,0.3)',
                        customClass: 'w-loading'
                    })
                }

                return options
            },
            async responseInterceptorsHook(response: any, options: any): Promise<any> {
                const { isTransformResponse, isReturnDefaultResponse, withHints }: any = options.requestOptions

                // 关闭加载中
                if (loadingInstance) {
                    loadingInstance.close()
                }

                // 需响应头及其它时可使用
                if (isReturnDefaultResponse) {
                    return response
                }

                // 是否需要对数据进行处理
                if (!isTransformResponse) {
                    return response._data
                }

                // 对响应回的数据进行处理
                const { code, msg, data } = response._data
                switch (code) {
                    case errorEnum.SUCCESS:
                        if (withHints && msg) {
                            feedback.msgSuccess(msg)
                        }
                        return data
                    case errorEnum.FAILED:
                    case errorEnum.PARAMS_TYPE_ERROR:
                    case errorEnum.PARAMS_VALID_ERROR:
                    case errorEnum.PARAMS_ASSERT_ERROR:
                    case errorEnum.PERMISSIONS_ERROR:
                    case errorEnum.REQUEST_404_ERROR:
                    case errorEnum.REQUEST_405_ERROR:
                    case errorEnum.SYSTEM_UNKNOWN_ERROR:
                    case errorEnum.SYSTEM_TIMEOUT_ERROR:
                    case errorEnum.DB_CONNECT_ERROR:
                    case errorEnum.DB_EMPTY_DATA_ERROR:
                        feedback.msgError(msg)
                        return Promise.reject(response._data)
                    case errorEnum.TOKEN_EMPTY:
                    case errorEnum.TOKEN_VALID:
                        await userStore.logout()
                        return Promise.reject(data)
                    default:
                        return data
                }
            },
            responseInterceptorsCatchHook(err: any) {
                if (loadingInstance) {
                    loadingInstance.close()
                }
                return err
            }
        }
    }

    return new Request(merge(defaultOptions, opt || {}))
}
