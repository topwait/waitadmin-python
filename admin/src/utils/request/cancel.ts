import axios, { type AxiosRequestConfig, type Canceler } from 'axios'

const cancelerMap: Map<string, Canceler> = new Map<string, Canceler>()

export class AxiosCancel {
    private static instance?: AxiosCancel

    static createInstance(): AxiosCancel {
        return this.instance ?? (this.instance = new AxiosCancel())
    }

    add(config: AxiosRequestConfig): void {
        const url: string = config.url!
        this.remove(url)
        config.cancelToken = new axios.CancelToken((cancel: Canceler): void => {
            if (!cancelerMap.has(url)) {
                cancelerMap.set(url, cancel)
            }
        })
    }

    remove(url: string): void {
        if (cancelerMap.has(url)) {
            const cancel: Canceler | undefined = cancelerMap.get(url)
            cancel && cancel(url)
            cancelerMap.delete(url)
        }
    }
}

const axiosCancel: AxiosCancel = AxiosCancel.createInstance()

export default axiosCancel
