import request from '@/utils/request'

const attachApi = {
    /**
     * 附件列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {number} [params.cid]
     * @param {number} [params.type]
     * @param {string} [params.keyword]
     */
    albumLists(params: {
        page_no?: number;
        page_size?: number;
        cid?: number;
        type?: number;
        keyword?: string;
    }): Promise<any> {
        return request.get({
            url: '/attach/album_lists',
            params
        })
    },

    /**
     * 附件移动
     *
     * @param {number[]} ids
     * @param {number} cid
     */
    albumMove(ids: number[], cid: number): Promise<any> {
        return request.post({
            url: '/attach/album_move',
            params: {
                ids,
                cid
            }
        })
    },

    /**
     * 附件命名
     *
     * @param {number} id
     * @param {string} name
     */
    albumRename(id: number, name: string): Promise<any> {
        return request.post({
            url: '/attach/album_rename',
            params: {
                id,
                name
            }
        })
    },

    /**
     * 附件删除
     *
     * @param {number[]} ids
     */
    albumDelete(ids: number[]): Promise<any> {
        return request.post({
            url: '/attach/album_delete',
            params: {
                ids
            }
        })
    },

    /**
     * 分组列表
     *
     * @param {number} type
     */
    cateLists(type: number): Promise<any> {
        return request.get({
            url: '/attach/cate_lists',
            params: { type }
        })
    },

    /**
     * 分组创建
     *
     * @param {number} type
     * @param {string} name
     */
    cateAdd(type: number, name: string): Promise<any> {
        return request.post({
            url: '/attach/cate_add',
            params: {
                type,
                name
            }
        })
    },

    /**
     * 分组编辑
     *
     * @param {number} type
     * @param {string} name
     * @param {number} id
     */
    cateRename(type: number, name: string, id: number): Promise<any> {
        return request.post({
            url: '/attach/cate_rename',
            params: {
                type,
                name,
                id
            }
        })
    },

    /**
     * 分组删除
     *
     * @param {number} type
     * @param {number} id
     */
    cateDelete(type: number, id: number): Promise<any> {
        return request.post({
            url: '/attach/cate_delete',
            params: {
                type,
                id
            }
        })
    }
}

export default attachApi
