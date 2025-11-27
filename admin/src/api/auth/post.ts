import request from '@/utils/request'

const authPostApi = {
    /**
     * 所有岗位
     */
    whole(): Promise<AuthPostWholeResponse[]> {
        return request.get<AuthPostWholeResponse[]>({
            url: '/auth/post/whole'
        })
    },

    /**
     * 岗位列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.code]
     * @param {string} [params.name]
     * @param {number} [params.is_disable]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        code?: string;
        name?: string;
        is_disable?: number;
    }): Promise<AuthPostListResponse[]> {
        return request.get<AuthPostListResponse[]>({
            url: '/auth/post/lists',
            params
        })
    },

    /**
     * 岗位详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<AuthPostDetailResponse> {
        return request.get<AuthPostDetailResponse>({
            url: '/auth/post/detail',
            params: { id }
        })
    },

    /**
     * 岗位新增
     *
     * @param {Object} params
     * @param {string} params.code
     * @param {string} params.name
     * @param {string} [params.remarks]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    add(params: {
        code: string;
        name: string;
        remarks?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/post/add',
            params
        })
    },

    /**
     * 岗位编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.code
     * @param {string} params.name
     * @param {string} [params.remarks]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: {
        id: number;
        code: string;
        name: string;
        remarks?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/post/edit',
            params
        })
    },

    /**
     * 岗位删除
     *
     * @param {number} id
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/post/delete',
            params: { id }
        })
    }
}

export default authPostApi
