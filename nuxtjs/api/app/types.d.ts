/** ------ [全局配置] ------ */
interface AppConfigResponse {
    login: _AppConfigLogin;
    website: _AppConfigWebsite;
    recharge: _AppConfigRecharge,
    pc: _AppConfigPc;
}

interface _AppConfigLogin {
    is_agreement: number;
    defaults: string;
    register: any[];
    means: string[];
    oauth: string[];
}

interface _AppConfigRecharge {
    status: number;
    min_recharge: number;
}

interface _AppConfigWebsite {
    icp: string;
    pcp: string;
    domain: string;
    analyse: string;
    copyright: string;
}

interface _AppConfigPc {
    favicon: string;
    logo: string;
    name: string;
    title: string;
    keywords: string;
    description: string;
}

/** ------ [网站首页] ------ */
interface AppHomingResponse {
    adv: _AppHomingAdv[];
    banner: _AppHomingAdv[];
    lately: _AppHomingArticles[];
    ranking: _AppHomingArticles[];
    topping: _AppHomingArticles[];
    everyday: _AppHomingArticles[];
}

interface _AppHomingAdv {
    title: string;
    image: string;
    target: string;
    url: string;
}

interface _AppHomingArticles {
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
