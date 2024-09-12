import { isObject } from '@vue/shared'
import { cloneDeep } from 'lodash'

const toolsUtil = {
    /**
     * 树转数组
     *
     * @param {any[]} data
     * @param {any} props
     * @returns {any[]}
     */
    treeToArray(data: any[], props: any = { children: 'children' }): any[] {
        data = cloneDeep(data)
        const { children } = props
        const newData: any[] = []
        const queue: any[] = []
        data.forEach((child: any) => queue.push(child))
        while (queue.length) {
            const item: any = queue.shift()
            if (item[children]) {
                item[children].forEach((child: any) => queue.push(child))
                // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
                delete item[children]
            }
            newData.push(item)
        }
        return newData
    },

    /**
     * 数组转树
     *
     * @param {any[]} data
     * @param {any} props
     * @returns {any[]}
     */
    arrayToTree(data: any[], props: any = { id: 'id', parentId: 'pid', children: 'children' }): any[] {
        data = cloneDeep(data)
        const { id, parentId, children } = props
        const result: any[] = []
        const map: Map<any, any> = new Map()
        data.forEach((item): void => {
            map.set(item[id], item)
            const parent = map.get(item[parentId])
            if (parent) {
                parent[children] = parent[children] ?? []
                parent[children].push(item)
            } else {
                result.push(item)
            }
        })
        return result
    },

    /**
     * 添加单位
     *
     * @param {string|number} value (值: 100)
     * @param {string} unit (单位: [px,em,rem])
     * @returns {string} (带单位的值)
     */
    addUnit(value: string | number, unit: string = 'px'): string {
        return !Object.is(Number(value), NaN) ? `${value}${unit}` : value + ''
    },

    /**
     * 验证是否为空
     *
     * @param value
     * @returns {boolean} (ture=是,false=否)
     */
    isEmpty(value: unknown): boolean {
        return value === null && typeof value === 'undefined'
    },

    /**
     * 对象格式化为Query语法
     *
     * @param {object} params
     * @returns {string} Query语法
     */
    objectToQuery(params: Record<string, any>): string {
        let query: string = ''
        for (const props of Object.keys(params)) {
            const value = params[props]
            const part: string = encodeURIComponent(props) + '='
            if (!toolsUtil.isEmpty(value) && isObject(value)) {
                for (const key of Object.keys(value)) {
                    if (!toolsUtil.isEmpty(value[key])) {
                        const params: string = props + '[' + key + ']'
                        const subPart: string = encodeURIComponent(params) + '='
                        query += subPart + encodeURIComponent(value[key]) + '&'
                    }
                }
            }

            if (!toolsUtil.isEmpty(value) && !isObject(value)) {
                query += part + encodeURIComponent(value) + '&'
            }
        }
        return query.slice(0, -1)
    }
}

export default toolsUtil
