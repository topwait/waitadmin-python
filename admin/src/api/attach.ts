import request from '@/utils/request'

const attachApi = {
    /**
     * 附件列表
     */
    albumLists(params: any): Promise<any> {
        return request.get({
            url: '/attach/album_lists',
            params
        })
    },

    /**
     * 附件移动
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
     */
    cateLists(type: number): Promise<any> {
        return request.get({
            url: '/attach/cate_lists',
            params: { type }
        })
    },

    /**
     * 分组创建
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
