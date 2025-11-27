/**
 * 全局配置类型
 */
interface AppConfigResponse {
    login: {
        is_agreement: number;
        defaults: string;
        register: any[];
        means: string[];
        oauth: string[];
    };
    website: {
        icp: string;
        pcp: string;
        domain: string;
        analyse: string;
        copyright: string;
    };
    recharge: {
        status: number;
        min_recharge: number;
    };
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
    adv: AppHomingAdv[];
    banner: AppHomingAdv[];
    lately: AppHomingArticles[];
    ranking: AppHomingArticles[];
    topping: AppHomingArticles[];
    everyday: AppHomingArticles[];
}

interface AppHomingAdv {
    title: string;
    image: string;
    target: string;
    url: string;
}

interface AppHomingArticles {
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
 * 政策协议类型
 */
interface AppPolicyResponse {
    content: string;
}

/**
 * 上传结果类型
 */
interface AppUploadResponse {
    id: number;
    name: string;
    ext: string;
    size: number;
    path: string;
    url: string;
}
