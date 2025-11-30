/**
 * 后台配置参数类型
 */
interface SettingBacksResponse {
    // 网站名称
    name: string;
    // 网站标题
    title: string;
    // 登录封面
    cover: string;
    // 网站图标
    favicon: string;
    // 深色大logo
    logo_black_big: string;
    // 深色小logo
    logo_black_small: string;
    // 浅色大logo
    logo_white_big: string;
    // 浅色小logo
    logo_white_small: string;
    // 联系人名
    contacts: string;
    // 联系电话
    mobile: string;
}

/**
 * 网站配置参数类型
 */
interface SettingBasicsResponse {
    website: {
        // 备案号
        icp: string;
        // 营业执照
        pcp: string;
        // 版权
        copyright: string;
        // 分析
        analyse: string;
    },
    h5: {
        // 标题
        title: string;
        // 封面
        logo: string;
        // 状态
        status: number;
        // 关闭地址
        close_url: string;
    },
    pc: {
        // 图标
        favicon: string;
        // 封面
        logo: string;
        // 名称
        name: string;
        // 标题
        title: string;
        // 关键字
        keywords: string;
        // 描述
        description: string;
    }
}

/**
 * 渠道配置参数类型
 */
interface SettingChannelResponse {
    wx: {
        // 名称
        name: string;
        // 原始ID
        original_id: string;
        // 二维码
        qr_code: string;
        // AppID
        app_id: string;
        // AppSecret
        app_secret: string;
        // 请求域名
        request_domain: string;
        // Socket域名
        socket_domain: string;
        // 上传文件域名
        upload_file_domain: string;
        // 下载文件域名
        download_file_domain: string;
        // UDP域名
        udp_domain: string;
    },
    oa: {
        // 名称
        name: string;
        // 原始ID
        original_id: string;
        // 二维码
        qr_code: string;
        // AppID
        app_id: string;
        // AppSecret
        app_secret: string;
        // URL
        url: string;
        // Token
        token: string;
        // AES密钥
        aes_key: string;
        // 加密类型
        encryption_type: 1,
        // WK域名
        wk_domain: string;
        // JS域名
        js_domain: string;
        // Web域名
        web_domain: string;
    },
    op: {
        // AppID
        app_id: string;
        // AppSecret
        app_secret: string;
    }
}

/**
 * 存储配置参数类型
 */
interface SettingStorageResponse {
    // 驱动
    drive: string;
    // 本地
    local: any;
    // 七牛OSS
    qiniu: {
        // 存储空间
        bucket: string;
        // 域名
        domain: string;
        // 密钥
        access_key: string;
        // 密钥
        secret_key: string;
        // 区域
        region: string;
    },
    // 阿里云OSS
    aliyun: {
        // 存储空间
        bucket: string;
        // 域名
        domain: string;
        // 密钥
        access_key: string;
        // 密钥
        secret_key: string;
        // 区域
        region: string;
    },
    // 腾讯云COS
    qcloud: {
        // 存储空间
        bucket: string;
        // 域名
        domain: string;
        // 密钥
        access_key: string;
        // 密钥
        secret_key: string;
        // 区域
        region: string;
    }
}

/**
 * 登录配置参数类型
 */
interface SettingLoginResponse {
    // PC端登录配置
    pc: {
        // 显示授权协议
        is_agreement: boolean;
        // 默认登录方式: [account, mobile, wx]
        default_method: string;
        // 可用登录方式: [account, mobile, wx]
        usable_channel: string[];
        // 允许注册方式: [account, mobile, email]
        usable_register: string[];
    }
}

/**
 * 协议配置参数类型
 */
interface SettingPolicyResponse {
    // 服务协议
    service: string;
    // 隐私协议
    privacy: string;
    // 支付协议
    payment: string;
}

/**
 * 邮箱配置参数类型
 */
interface SettingEmailResponse {
    // SMTP类型
    smtp_type: string;
    // SMTP主机
    smtp_host: string;
    // SMTP端口
    smtp_port: string;
    // SMTP用户
    smtp_user: string;
    // SMTP密码
    smtp_pass: string;
    // 验证类型
    verify_type: string;
}

/**
 * 短信配置列表类型
 */
interface SettingSmsListResponse {
    // 短信别名
    alias: string;
    // 短信名称
    name: string;
    // 短信描述
    desc: string;
    // 短信图标
    image: string;
    // 短信状态: [0=禁用, 1=启用]
    status: number;
}

/**
 * 短信配置详情类型
 */
interface SettingSmsDetailResponse {
    // 短信别名
    alias: string;
    // 短信名称
    name: string;
    // 短信状态: [0=禁用, 1=启用]
    status: number;
    // 短信参数
    params: Record<string, string>
}
