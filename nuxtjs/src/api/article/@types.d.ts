/**
 * 文章列表类型
 */
interface ArticleListsResponse {
    // ID
    id: number;
    // 所属类目
    category: string;
    // 文章图片
    image: string;
    // 文章标题
    title: string;
    // 文章简介
    intro: string;
    // 访问数量
    browse: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 文章详情类型
 */
interface ArticleDetailResponse {
    // ID
    id: number;
    // 所属类目
    category: string;
    // 文章图片
    image: string;
    // 文章标题
    title: string;
    // 文章简介
    intro: string;
    // 文章内容
    content: string;
    // 访问数量
    browse: number;
    // 是否收藏: [0=否, 1=是]
    is_collect: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
    // 上一篇
    prev: {
        // ID
        id: number;
        // 标题
        title: string;
    };
    next: {
        // ID
        id: number;
        // 标题
        title: string;
    };
}

/**
 * 文章页面类型
 */
interface ArticlePagesResponse {
    // 推荐文章
    topping: ArticleListsResponse[];
    // 排名文章
    ranking: ArticleListsResponse[];
    // 轮播广告
    adv: {
        // 标题
        title: string;
        // 图片
        image: string;
        // 目标
        target: string;
        // 链接
        url: string;
    }[];
}
