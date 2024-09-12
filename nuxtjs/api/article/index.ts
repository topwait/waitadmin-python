const articleApi = {
    /**
     * 文章页面
     */
    pages(): Promise<ArticlePagesResponse> {
        return $request.get<ArticlePagesResponse>({
            url: '/article/pages'
        })
    },

    /**
     * 文章列表
     *
     * @param {Object} params
     * @param {number} params.page - 当前页码
     * @param {number} params.cid - 所属类目
     * @param {string} params.keyword - 文章标题
     * @returns {Promise<ArticleListsResponse>}
     * @author zero
     */
    lists(params: {
        page?: number,
        cid?: number,
        keyword?: string
    }): Promise<ArticleListsResponse> {
        return $request.get<ArticleListsResponse>({
            url: '/article/lists',
            params
        })
    },

    /**
     * 文章详情
     *
     * @param {number} id - 文章ID
     * @returns {Promise<ArticleDetailResponse>}
     */
    detail(id: number): Promise<ArticleDetailResponse> {
        return $request.get<ArticleDetailResponse>({
            url: '/article/detail',
            params: { id }
        })
    },

    /**
     * 文章收藏
     *
     * @param {number} id - 文章ID
     * @returns {Promise<any>}
     * @author zero
     */
    collect(id: number): Promise<any> {
        return $request.post({
            url: '/article/collect',
            params: {
                id
            }
        })
    }
}

export default articleApi
