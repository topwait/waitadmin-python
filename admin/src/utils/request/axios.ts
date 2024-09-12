import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { isFunction, merge, cloneDeep, isObject } from 'lodash'
import type { FileParams, RequestData, RequestOptions } from './type'
import axiosCancel from './cancel'

export class Axios {
    private readonly axiosInstance: AxiosInstance
    private readonly config: AxiosRequestConfig
    private readonly options: RequestOptions

    constructor(config: AxiosRequestConfig) {
        this.config = config
        this.options = config.requestOptions
        this.axiosInstance = axios.create(config)
        this.setupInterceptors()
    }

    getAxiosInstance(): AxiosInstance {
        return this.axiosInstance
    }

    setupInterceptors(): void {
        if (!this.config.axiosHooks) {
            return
        }

        const {
            requestInterceptorsHook,
            requestInterceptorsCatchHook,
            responseInterceptorsHook,
            responseInterceptorsCatchHook
        } = this.config.axiosHooks

        this.axiosInstance.interceptors.request.use(
            (config: any) => {
                const { ignoreCancelToken } = config.requestOptions
                if (!ignoreCancelToken) {
                    axiosCancel.add(config)
                }
                if (isFunction(requestInterceptorsHook)) {
                    return requestInterceptorsHook(config)
                }
                return config
            },
            (err: Error) => {
                if (isFunction(requestInterceptorsCatchHook)) {
                    requestInterceptorsCatchHook(err)
                }
                return err
            }
        )

        this.axiosInstance.interceptors.response.use(
            (response: AxiosResponse<RequestData>) => {
                axiosCancel.remove(response.config.url!)
                if (isFunction(responseInterceptorsHook)) {
                    response = responseInterceptorsHook(response)
                }
                return response
            },
            async (err: AxiosError) => {
                if (isFunction(responseInterceptorsCatchHook)) {
                    responseInterceptorsCatchHook(err)
                }
                if (err.code !== AxiosError.ERR_CANCELED) {
                    const url: string = err.config?.url ? err.config?.url : ''
                    axiosCancel.remove(url)
                }

                if (err.code === AxiosError.ECONNABORTED || err.code === AxiosError.ERR_NETWORK) {
                    await new Promise((resolve) => setTimeout(resolve, 500))
                    return await this.retryRequest(err)
                }
                return Promise.reject(err)
            }
        )
    }

    retryRequest(error: AxiosError) {
        const config: any = error.config
        const { retryCount, isOpenRetry } = config.requestOptions
        if (!isOpenRetry || config.method?.toUpperCase() === 'POST') {
            return Promise.reject(error)
        }

        config.retryCount = config.retryCount ?? 0
        if (config.retryCount >= retryCount) {
            return Promise.reject(error)
        }
        config.retryCount++

        return this.axiosInstance.request(config)
    }

    get<T = any>(
        config: Partial<AxiosRequestConfig>,
        options?: Partial<RequestOptions>
    ): Promise<T> {
        return this.request({ ...config, method: 'GET' }, options)
    }

    post<T = any>(
        config: Partial<AxiosRequestConfig>,
        options?: Partial<RequestOptions>
    ): Promise<T> {
        return this.request({ ...config, method: 'POST' }, options)
    }

    upload<T>(
        config: Partial<AxiosRequestConfig>,
        params: FileParams,
        options?: Partial<RequestOptions>
    ): Promise<T> {
        const formData: FormData = new FormData()
        const customFilename: string = params.name || 'file'
        formData.append(customFilename, params.file)
        if (params.data) {
            Object.keys(params.data).forEach((key: string): void => {
                const value = params.data![key]
                if (isObject(value)) {
                    formData.append(key, JSON.stringify(value))
                } else {
                    formData.append(key, value)
                }
            })
        }

        return this.post<T>(
            {
                timeout: 30 * 1000,
                ...config,
                data: formData
            },
            {
                ignoreCancelToken: true,
                showProgress: false,
                ...options
            }
        )
    }

    request<T = any>(
        config: Partial<AxiosRequestConfig>,
        options?: Partial<RequestOptions>
    ): Promise<any> {
        const opt: RequestOptions = merge({}, this.options, options)
        const axiosConfig: AxiosRequestConfig = {
            ...cloneDeep(config),
            requestOptions: opt
        }

        const { urlPrefix } = opt
        if (urlPrefix) {
            axiosConfig.url = `${urlPrefix}${config.url}`
        }

        return new Promise((resolve, reject): void => {
            this.axiosInstance
                .request<any, AxiosResponse<RequestData<T>>>(axiosConfig)
                .then((res): void => {
                    resolve(res)
                }).catch((err): void => {
                    reject(err)
                })
        })
    }
}
