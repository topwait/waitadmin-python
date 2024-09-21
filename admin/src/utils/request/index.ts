import NProgress from 'nprogress'
import { merge } from 'lodash'
import { ElMessage } from 'element-plus'
import { type AxiosRequestConfig, AxiosError, RawAxiosRequestHeaders, AxiosHeaders } from 'axios'
import { type AxiosHooks } from './type'
import { Axios } from './axios'
import { errorEnum } from '@/enums/errors'
import { cacheEnum } from '@/enums/cache'
import router from '@/router'
import configs from '@/config'
import cacheUtil from '@/utils/cache'

const axiosHooks: AxiosHooks = {
    requestInterceptorsHook(config: AxiosRequestConfig<any>) {
        const { withToken, isParamsToData, showProgress } = config.requestOptions
        const params = config.params || {}
        const headers: RawAxiosRequestHeaders | AxiosHeaders = config.headers || {}

        showProgress && NProgress.start()

        if (withToken) {
            const token: string = cacheUtil.get(cacheEnum.TOKEN_KEY) || ''
            headers.Authorization = 'Bearer ' + token
        }

        if (
            isParamsToData
            && !Reflect.has(config, 'data')
            && config.method?.toUpperCase() === 'POST'
        ) {
            config.data = params
            config.params = {}
        }

        config.headers = headers
        return config
    },
    responseInterceptorsHook(response) {
        NProgress.done()
        const { isTransformResponse, isReturnDefaultResponse } = response.config.requestOptions

        if (isReturnDefaultResponse) {
            return response
        }

        if (!isTransformResponse) {
            return response.data
        }

        const { code, data, msg } = response.data
        switch (code) {
            case errorEnum.SUCCESS:
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
            case errorEnum.DB_OPERATIONS_ERROR:
            case errorEnum.DB_EMPTY_DATA_ERROR:
                msg && ElMessage.error(msg)
                return Promise.reject(data)
            case errorEnum.TOKEN_EMPTY:
            case errorEnum.TOKEN_VALID:
                router.push('/login').then((): void => { })
                return Promise.reject()
            default:
                return data
        }
    },
    requestInterceptorsCatchHook(error: Error) {
        NProgress.done()
        return error
    },
    responseInterceptorsCatchHook(error: AxiosError) {
        NProgress.done()
        if (error.code !== AxiosError.ERR_CANCELED) {
            error.message && ElMessage.error(error.message)
        }
        return Promise.reject(error)
    }
}

function createAxios(opt?: Partial<AxiosRequestConfig>): Axios {
    return new Axios(
        merge({
            // 接口超时时间
            timeout: configs.timeout,
            // 基础接口地址
            baseURL: configs.baseUrl,
            // 请求头的配置
            headers: { 'Content-Type': 'application/json;charset=UTF-8' },
            // 处理Axios的钩子函数
            axiosHooks: axiosHooks,
            // 每个接口可以单独配置
            requestOptions: {
                // 是否将params视为data参数(仅限post请求)
                isParamsToData: true,
                // 是否处理返回的数据
                isTransformResponse: true,
                // 是否返回默认的响应
                isReturnDefaultResponse: false,
                // 忽略重复请求
                ignoreCancelToken: false,
                // 接口拼接地址
                urlPrefix: configs.urlPrefix,
                // 是否携带令牌
                withToken: true,
                // 超时重新请求
                isOpenRetry: true,
                // 重新请求次数
                retryCount: 2,
                // 进度条的显示
                showProgress: true
            }
        }, opt || {})
    )
}

const request: Axios = createAxios()

export default request
