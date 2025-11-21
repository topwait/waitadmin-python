const cacheUtil = {
    namespace: 'wap_',

    /**
     * 设置缓存
     *
     * @param {string} key    (键)
     * @param {any} value     (值)
     * @param {number} expire (时效时长: 秒)
     * @returns {boolean}
     */
    set(key: string, value: any, expire?: number): boolean {
        key = this.namespace + key
        let data = value
        if (expire) {
            const time: number = Math.round(new Date().getTime() / 1000)
            data = {
                expire: time + expire,
                value: value
            }
        }

        if (typeof data === 'object') {
            data = JSON.stringify(data)
        }

        try {
            window.localStorage.setItem(key, data)
            return true
        } catch {
            return false
        }
    },

    /**
     * 获取缓存
     *
     * @param key (键)
     * @param isShowExpire (是否显示过期时间)
     * @returns {any}
     */
    get(key: string, isShowExpire: boolean = false): any {
        key = this.namespace + key
        const data: string | null = window.localStorage.getItem(key)
        if (data === undefined || data === null) {
            if (!isShowExpire) {
                return undefined
            }
            return { expire: undefined, value: undefined }
        }

        try {
            const time: number = Math.round(new Date().getTime() / 1000)
            const { value, expire } = JSON.parse(data)
            if (expire && expire < time) {
                window.localStorage.removeItem(key)
                return undefined
            }

            if (value) {
                if (!isShowExpire) {
                    return value
                }
                return { expire, value }
            }

            const val = JSON.parse(data)
            if (val !== undefined) {
                return val
            }

            return data
        } catch {
            return data
        }
    },

    /**
     * 移除缓存
     *
     * @param key (键)
     * @returns {void}
     */
    remove(key: string): void {
        key = this.namespace + key
        window.localStorage.removeItem(key)
    },

    /**
     * 清空缓存
     */
    clear(): void {
        window.localStorage.clear()
    }
}

export default cacheUtil
