/**
 * 附件列表类型
 */
interface AlbumListResponse {
    id: number;
    type: number;
    size: number;
    name: string;
    path: string;
    url: string;
    ext: string;
    create_time: string;
    update_time: string;
}

/**
 * 附件分类类型
 */
interface AlbumCateResponse {
    id: number;
    name: string;
}
