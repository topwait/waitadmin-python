/** ------ [全局配置] ------ */
interface AppConfigResponse {
    login: AppConfigLogin;
    website: AppConfigWebsite;
    recharge: AppConfigRecharge;
    pc: AppConfigPc;
}

interface AppConfigLogin {
    is_agreement: number;
    defaults: string;
    register: any[];
    means: string[];
    oauth: string[];
}

interface AppConfigRecharge {
    status: number;
    min_recharge: number;
}

interface AppConfigWebsite {
    icp: string;
    pcp: string;
    domain: string;
    analyse: string;
    copyright: string;
}

interface AppConfigPc {
    favicon: string;
    logo: string;
    name: string;
    title: string;
    keywords: string;
    description: string;
}

/** ------ [网站首页] ------ */
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

/** ------ [政策协议] ------ */
interface AppPolicyResponse {
    content: string;
}

/** ------ [上传结果] ------ */
interface AppUploadResponse {
    id: number;
    name: string;
    ext: string;
    size: number;
    path: string;
    url: string;
}
