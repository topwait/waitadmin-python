/**
 * 全局配置类型
 */
interface AppConfigResponse {
    name: string;
    title: string;
    cover: string;
    favicon: string;
    logo_black_big: string;
    logo_black_small: string;
    logo_white_big: string;
    logo_white_small: string;
    enable_captcha: boolean;
}

/**
 * 控制台数据类型
 */
interface AppWorkbenchResponse {
    version: {
        version: string;
        frame: string;
        tones: string;
        official: string;
    },
    today: {
        name: string;
        icon: string;
        value: number;
        total: number;
        yesterday: number;
    }[],
    shortcut: {
        name: string;
        icon: string;
        path: string;
    }[],
    backlogs: {
        name: string;
        value: number;
        path: string;
    }[],
    echartsVisitor: {
        date: string[];
        list: number[];
    },
    echartsWebsite: {
        value: number;
        name: string;
    }[]
}

/**
 * 文件上传类型
 */
interface AppUploadResponse {
    id: number;
    name: string;
    size: number;
    ext: string;
    path: string;
    url: string;
}
