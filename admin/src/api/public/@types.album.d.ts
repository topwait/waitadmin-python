/**
 * 附件列表类型
 */
interface AlbumListResponse {
    // ID
    id: number;
    // 文件类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]
    type: number | 10 | 20 | 30 | 40 | 50;
    // 文件大小
    size: number;
    // 文件名称
    name: string;
    // 文件路径
    path: string;
    // 文件地址
    url: string;
    // 文件扩展
    ext: string;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 附件分类类型
 */
interface AlbumCateResponse {
    // ID
    id: number;
    // 分类名称
    name: string;
}
