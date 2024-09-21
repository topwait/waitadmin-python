import { merge } from 'lodash-es'
import { isFunction } from 'lodash'
import { $fetch } from 'ofetch'
import type {
    $Fetch,
    FileParams,
    FetchOptions,
    FetchResponse,
    RequestOptions,
    RequestEventStreamOptions
} from 'ofetch'

export class Request {
    private readonly fetchInstance: $Fetch
    private readonly requestOptions: RequestOptions | any

    /**
     * 构造函数
     * @param fetchOptions
     */
    constructor(private fetchOptions: FetchOptions) {
        this.fetchInstance = $fetch.create(fetchOptions)
        this.requestOptions = fetchOptions.requestOptions
    }

    /**
     * 取请求实例
     */
    getInstance(): $Fetch {
        return this.fetchInstance
    }

    /**
     * GET请求
     *
     * @param {FetchOptions} fetchOptions
     * @param {Partial<RequestOptions>} requestOptions
     * @returns {Promise<any>}
     * @author zero
     */
    get<T = any>(fetchOptions: FetchOptions, requestOptions?: Partial<RequestOptions>): Promise<T> {
        return this.request<T>(
            { ...fetchOptions, method: 'GET' },
            requestOptions
        )
    }

    /**
     * POST请求
     *
     * @param {FetchOptions} fetchOptions
     * @param {Partial<RequestOptions>} requestOptions
     * @returns {Promise<any>}
     * @author zero
     */
    post<T = any>(fetchOptions: FetchOptions, requestOptions?: Partial<RequestOptions>): Promise<T> {
        return this.request<T>(
            { ...fetchOptions, method: 'POST' },
            requestOptions
        )
    }

    /**
     * 上传请求
     *
     * @param {FetchOptions} options
     * @param {FileParams} params
     * @returns {Promise<any>}
     * @author zero
     */
    uploadFile<T = any>(options: FetchOptions, params: FileParams): Promise<T> {
        const formData: FormData = new FormData()
        const customFilename: string = params.name || 'file'
        formData.append(customFilename, params.file)
        if (params.data) {
            Object.keys(params.data).forEach((key: string): void => {
                const value: ArrayConstructor = params.data![key]
                if (Array.isArray(value)) {
                    value.forEach((item): void => {
                        formData.append(`${key}[]`, item)
                    })
                    return
                }

                formData.append(key, params.data![key])
            })
        }
        return this.request<T>({
            ...options,
            method: 'POST',
            body: formData
        })
    }

    /**
     * SSE流请求
     *
     * @param {FetchOptions} fetchOptions
     * @param {Partial<RequestEventStreamOptions>} requestOptions
     * @returns {Promise<any>}
     * @author zero
     */
    async eventStream<T = any>(fetchOptions: FetchOptions, requestOptions?: Partial<RequestEventStreamOptions>): Promise<T> {
        let mergeOptions: any = merge({}, this.fetchOptions, fetchOptions)
        mergeOptions.requestOptions = merge({}, this.requestOptions, requestOptions)

        const { requestInterceptorsHook, responseInterceptorsHook } = this.requestOptions
        if (requestInterceptorsHook && isFunction(requestInterceptorsHook)) {
            mergeOptions = requestInterceptorsHook(mergeOptions)
        }

        const { onmessage, onclose, onstart }: any = requestOptions
        return new Promise((resolve, reject): void => {
            const push = async (controller: any, reader: any): Promise<void> => {
                try {
                    const { value, done } = await reader.read()
                    if (done) {
                        controller.close()
                        onclose?.()
                    } else {
                        onmessage?.(new TextDecoder().decode(value))
                        controller.enqueue(value)
                        await push(controller, reader)
                    }
                } catch {
                    onclose?.()
                }
            }

            let body = undefined
            let url: string = `${mergeOptions.baseURL}${mergeOptions.url}`
            if (mergeOptions.method.toUpperCase() === 'GET') {
                url = `${url}?${this.objectToQuery(mergeOptions.params)}`
            }

            if (mergeOptions.method.toUpperCase() === 'POST') {
                body = JSON.stringify(mergeOptions.body)
            }

            fetch(url, {
                ...mergeOptions,
                body,
                headers: {
                    'accept': 'text/event-stream',
                    'Content-Type': 'application/json',
                    ...mergeOptions.headers
                }
            }).then(async (response: any): Promise<any> => {
                if (response.status === 200) {
                    if (response.headers.get('content-type')?.includes('text/event-stream')) {
                        const reader = response.body!.getReader()
                        onstart?.(reader)
                        new ReadableStream({
                            start(controller: ReadableStreamDefaultController): void {
                                push(controller, reader)
                            }
                        })
                    } else {
                        response._data = await response.json()
                        return response
                    }
                } else {
                    reject(response.statusText)
                }
            }).then(async (response): Promise<void> => {
                if (!response) {
                    resolve(response)
                }
                if (responseInterceptorsHook && isFunction(responseInterceptorsHook)) {
                    try {
                        response = await responseInterceptorsHook(response, mergeOptions)
                        resolve(response)
                    } catch (error) {
                        reject(error)
                    }
                    return
                }
                resolve(response)
            }).catch((): void => {
                reject()
            })
        })
    }

    /**
     * 请求逻辑封装
     *
     * @param {FetchOptions} fetchOptions
     * @param {Partial<RequestOptions>} requestOptions
     * @returns {Promise<any>}
     * @author zero
     */
    request<T = any>(fetchOptions: FetchOptions, requestOptions?: Partial<RequestOptions>): Promise<T> {
        let mergeOptions: any = merge({}, this.fetchOptions, fetchOptions)
        mergeOptions.requestOptions = merge({}, this.requestOptions, requestOptions)

        const {
            requestInterceptorsHook,
            responseInterceptorsHook,
            responseInterceptorsCatchHook
        } = this.requestOptions

        if (requestInterceptorsHook && isFunction(requestInterceptorsHook)) {
            mergeOptions = requestInterceptorsHook(mergeOptions)
        }

        return new Promise((resolve, reject) => this.fetchInstance.raw(mergeOptions.url, mergeOptions)
            .then(async (response: FetchResponse<any>): Promise<void> => {
                if (responseInterceptorsHook && isFunction(responseInterceptorsHook)) {
                    try {
                        response = await responseInterceptorsHook(response, mergeOptions)
                        resolve(response as T)
                    } catch (error) {
                        reject(error)
                    }
                    return
                }
                resolve(response as T)
            }).catch((err): void => {
                if (responseInterceptorsCatchHook && isFunction(responseInterceptorsCatchHook)) {
                    reject(responseInterceptorsCatchHook(err))
                    return
                }
                reject(err)
            }))
    }

    /**
     * 对象格式化为Query语法
     *
     * @param {Record<string, any>} params (参数)
     * @returns {string} Query语法
     * @author zero
     */
    objectToQuery(params: Record<string, any>): string {
        let query: string = ''
        for (const props of Object.keys(params)) {
            const value = params[props]
            const isEmpty: boolean = !(value !== null && value !== '' && typeof value !== 'undefined')
            if (!isEmpty) {
                query += props + '=' + value + '&'
            }
        }
        return query.slice(0, -1)
    }
}
