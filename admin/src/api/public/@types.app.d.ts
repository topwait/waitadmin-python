/**
 * 全局配置类型
 */
interface AppConfigResponse {
    // 网站名称
    name: string;
    // 网站标题
    title: string;
    // 网站封面
    cover: string;
    // 网站图标
    favicon: string;
    // 网站logo(黑色大图)
    logo_black_big: string;
    // 网站logo(黑色小图)
    logo_black_small: string;
    // 网站logo(白色大图)
    logo_white_big: string;
    // 网站logo(白色小图)
    logo_white_small: string;
    // 是否启用验证码
    enable_captcha: boolean;
}

/**
 * 控制台数据类型
 */
interface AppWorkbenchResponse {
    // 版本信息
    version: {
        version: string;
        frame: string;
        tones: string;
        official: string;
    },
    // 今日数据
    today: {
        name: string;
        icon: string;
        value: number;
        total: number;
        yesterday: number;
    }[],
    // 快捷方式
    shortcut: {
        name: string;
        icon: string;
        path: string;
    }[],
    // 待办事项
    backlogs: {
        name: string;
        value: number;
        path: string;
    }[],
    // 访客统计
    echartsVisitor: {
        date: string[];
        list: number[];
    },
    // 网站统计
    echartsWebsite: {
        value: number;
        name: string;
    }[]
}

/**
 * 文件上传类型
 */
interface AppUploadResponse {
    // ID
    id: number;
    // 文件名
    name: string;
    // 文件大小
    size: number;
    // 文件扩展名
    ext: string;
    // 文件路径
    path: string;
    // 文件URL
    url: string;
}
