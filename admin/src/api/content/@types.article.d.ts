/**
 * 文章列表类型
 */
interface ContentArticleListResponse {
    // ID
    id: number;
    // 封面
    image: string;
    // 标题
    title: string;
    // 分类
    category: string;
    // 浏览量
    browse: number;
    // 收藏量
    collect: number;
    // 排序
    sort: number;
    // 是否置顶: [0=否, 1=是]"
    is_topping: number;
    // 是否推荐: [0=否, 1=是]"
    is_recommend: number;
    // 是否显示: [0=否, 1=是]"
    is_show: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 文章详情类型
 */
interface ContentArticleDetailResponse {
    // ID
    id: number;
    // 分类ID
    cid: number;
    // 封面
    image: string;
    // 标题
    title: string;
    // 简介
    intro: string;
    // 内容
    content: string;
    // 浏览量
    browse: number;
    // 收藏量
    collect: number;
    // 排序
    sort: number;
    // 是否置顶: [0=否, 1=是]"
    is_topping: number;
    // 是否推荐: [0=否, 1=是]"
    is_recommend: number;
    // 是否显示: [0=否, 1=是]"
    is_show: number;
}
