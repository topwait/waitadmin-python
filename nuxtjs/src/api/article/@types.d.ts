/**
 * 文章列表类型
 */
interface ArticleListsResponse {
    id: number;
    category: string;
    image: string;
    title: string;
    intro: string;
    browse: number;
    create_time: string;
    update_time: string;
}

/**
 * 文章详情类型
 */
interface ArticleDetailResponse {
    id: number;
    category: string;
    image: string;
    title: string;
    intro: string;
    content: string;
    browse: number;
    is_collect: number;
    create_time: string;
    update_time: string;
    prev: {
        id: number;
        title: string;
    };
    next: {
        id: number;
        title: string;
    };
}

/**
 * 文章页面类型
 */
interface ArticlePagesResponse {
    topping: ArticleListsResponse[];
    ranking: ArticleListsResponse[];
    adv: {
        title: string;
        image: string;
        target: string;
        url: string;
    }[];
}
