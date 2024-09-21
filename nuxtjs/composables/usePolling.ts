interface Options {
    key: string,
    time?: number
    totalTime?: number
    count?: number
    callback?(): void
}

const pollingDict: any = {}

export default function usePolling(fun: () => Promise<any>, options?: Options) {
    const result = ref(null)
    const error = ref(null)
    const {
        key,
        time = 2000, // 多少毫秒轮询1次
        totalTime,   // 最大轮询时长: 毫秒
        count,       // 最大轮询次数: 默认不限制
        callback = () => false
    } = options ?? ({} as Options)

    let timer: any = null
    let endTime: number | null = null
    let totalCount = 0

    const run = () => {
        if (endTime && endTime <= Date.now()) {
            end()
            callback()
            return
        }

        if (count && totalCount >= count) {
            end()
            callback()
            return
        }

        totalCount++
        timer = setTimeout(() => {
            fun()
                .then((res) => {
                    result.value = res
                    run()
                })
                .catch((err) => {
                    error.value = err
                })
        }, time)
    }

    const start = () => {
        end()
        if (key && pollingDict[key]) {
            pollingDict[key].end()
            // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
            delete pollingDict[key]
        }
        endTime = totalTime ? Date.now() + totalTime : null
        run()
        if (key) {
            pollingDict[key] = { end }
        }
    }

    const end = () => {
        if (timer) {
            setTimeout(() => {
                clearTimeout(timer)
                timer = null
                endTime = null
                totalCount = 0
                if (key) {
                    // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
                    delete pollingDict[key]
                }
            }, 0)
        }
    }

    // onBeforeUnmount(() => {
    //     end()
    // })

    return {
        start,
        end,
        error,
        result
    }
}
