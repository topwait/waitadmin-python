/**
 * 全局配置类型
 */
interface AppConfigResponse {
    // 登录配置
    login: {
        pc: {
            is_agreement: boolean;
            default_method: string;
            usable_channel: string[];
            usable_register: string[];
        }
    };
    // 网站配置
    website: {
        icp: string;
        pcp: string;
        domain: string;
        analyse: string;
        copyright: string;
    };
    // 充值配置
    recharge: {
        status: number;
        min_recharge: number;
    };
    // PC配置
    pc: {
        favicon: string;
        logo: string;
        name: string;
        title: string;
        keywords: string;
        description: string;
    };
}

/**
 * 网站首页类型
 */
interface AppHomingResponse {
    // 广告
    adv: AppHomingAdv[];
    // 轮播
    banner: AppHomingAdv[];
    // 最新
    lately: AppHomingArticles[];
    // 排行
    ranking: AppHomingArticles[];
    // 置顶
    topping: AppHomingArticles[];
    everyday: AppHomingArticles[];
}

interface AppHomingAdv {
    // 标题
    title: string;
    // 图片
    image: string;
    // 目标
    target: string;
    // 链接
    url: string;
}

interface AppHomingArticles {
    // ID
    id: number;
    // 分类
    category: string;
    // 图片
    image: string;
    // 标题
    title: string;
    // 简介
    intro: string;
    // 浏览
    browse: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 政策协议类型
 */
interface AppPolicyResponse {
    // 内容
    content: string;
}

/**
 * 上传结果类型
 */
interface AppUploadResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 扩展名
    ext: string;
    // 大小
    size: number;
    // 路径
    path: string;
    // 链接
    url: string;
}
