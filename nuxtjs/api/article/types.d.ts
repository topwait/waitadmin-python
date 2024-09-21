/** ------ [文章列表] ------ */
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

/** ------[文章详情] ------ */
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
    prev: _ArticleDetailNext;
    next: _ArticleDetailNext;
}

interface _ArticleDetailNext {
    id: number;
    title: string;
}

/** ------ [文章页面] ------ */
interface ArticlePagesResponse {
    adv: _ArticlePagesAdv[];
    topping: ArticleListsResponse[];
    ranking: ArticleListsResponse[];
}

interface _ArticlePagesAdv {
    title: string;
    image: string;
    target: string;
    url: string;
}
