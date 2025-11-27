/**
 * 系统日志列表类型
 */
interface SystemJournalListResponse {
    id: number;
    admin: string;
    summary: string;
    method: string;
    url: string;
    ip: string;
    ua: string;
    error: string;
    status: number;
    task_time: number;
    create_time: string;
}

/**
 * 系统日志详情类型
 */
interface SystemJournalDetailResponse {
    id: number;
    nickname: string;
    username: string;
    summary: string;
    method: string;
    url: string;
    ip: string;
    ua: string;
    user_agent: string;
    endpoint: string;
    params: string;
    error: string;
    status: number;
    task_time: number;
    start_time: string;
    end_time: string;
    create_time: string;
}
