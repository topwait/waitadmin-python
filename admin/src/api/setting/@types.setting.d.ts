/**
 * 后台配置参数类型
 */
interface SettingBacksResponse {
    name: string;
    title: string;
    cover: string;
    favicon: string;
    logo_black_big: string;
    logo_black_small: string;
    logo_white_big: string;
    logo_white_small: string;
    contacts: string;
    mobile: string;
}

/**
 * 网站配置参数类型
 */
interface SettingBasicsResponse {
    website: {
        icp: string;
        pcp: string;
        copyright: string;
        analyse: string;
    },
    h5: {
        title: string;
        logo: string;
        status: number;
        close_url: string;
    },
    pc: {
        favicon: string;
        logo: string;
        name: string;
        title: string;
        keywords: string;
        description: string;
    }
}

/**
 * 渠道配置参数类型
 */
interface SettingChannelResponse {
    wx: {
        name: string;
        original_id: string;
        qr_code: string;
        app_id: string;
        app_secret: string;
        request_domain: string;
        socket_domain: string;
        upload_file_domain: string;
        download_file_domain: string;
        udp_domain: string;
    },
    oa: {
        name: string;
        original_id: string;
        qr_code: string;
        app_id: string;
        app_secret: string;
        url: string;
        token: string;
        aes_key: string;
        encryption_type: 1,
        wk_domain: string;
        js_domain: string;
        web_domain: string;
    },
    op: {
        app_id: string;
        app_secret: string;
    }
}

/**
 * 存储配置参数类型
 */
interface SettingStorageResponse {
    drive: string;
    local: any;
    qiniu: {
        bucket: string;
        domain: string;
        access_key: string;
        secret_key: string;
        region: string;
    },
    aliyun: {
        bucket: string;
        domain: string;
        access_key: string;
        secret_key: string;
        region: string;
    },
    qcloud: {
        bucket: string;
        domain: string;
        access_key: string;
        secret_key: string;
        region: string;
    }
}

/**
 * 登录配置参数类型
 */
interface SettingLoginResponse {
    is_agreement: number;
    defaults: string;
    registers: string[];
    login_modes: string[];
    login_other: string[];
}

/**
 * 协议配置参数类型
 */
interface SettingPolicyResponse {
    service: string;
    privacy: string;
    payment: string;
}

/**
 * 邮箱配置参数类型
 */
interface SettingEmailResponse {
    smtp_type: string;
    smtp_host: string;
    smtp_port: string;
    smtp_user: string;
    smtp_pass: string;
    verify_type: string;
}

/**
 * 短信配置列表类型
 */
interface SettingSmsListResponse {
    alias: string;
    name: string;
    desc: string;
    image: string;
    status: number;
}

/**
 * 短信配置详情类型
 */
interface SettingSmsDetailResponse {
    alias: string;
    name: string;
    status: number;
    params: Record<string, string>
}
