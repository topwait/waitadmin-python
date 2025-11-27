/**
 * 文章列表类型
 */
interface ContentArticleListResponse {
    id: number;
    image: string;
    title: string;
    category: string;
    browse: number;
    collect: number;
    sort: number;
    is_topping: number;
    is_recommend: number;
    is_show: number;
    create_time: string;
    update_time: string;
}

/**
 * 文章详情类型
 */
interface ContentArticleDetailResponse {
    id: number;
    cid: number;
    image: string;
    title: string;
    intro: string;
    content: string;
    browse: number;
    collect: number;
    sort: number;
    is_topping: number;
    is_recommend: number;
    is_show: number;
}
