interface Options {
    [propName: string]: {
        api: PromiseFun
        params?: Record<string, any>
        transformData?(data: any): any
    }
}

export function useDictOptions<T = any>(options: Options): any {
    const optionsData: any = reactive({})
    const optionsKey: string[] = Object.keys(options)

    const apiLists = optionsKey.map((key: string) => {
        const value: any = options[key]
        optionsData[key] = []
        return () => value.api(toRaw(value.params) || {})
    })

    const refresh = async (): Promise<void> => {
        const res: PromiseSettledResult<any>[] = await Promise.allSettled<Promise<any>>(apiLists.map((api) => api()))
        res.forEach((item: PromiseSettledResult<any>, index: number): void => {
            const key: string = optionsKey[index]

            if (item.status === 'fulfilled') {
                const { transformData } = options[key]
                optionsData[key] = transformData ? transformData(item.value) : item.value
            }
        })
    }

    refresh().then((): void => { })

    return {
        optionsData: optionsData as T,
        refresh
    }
}
