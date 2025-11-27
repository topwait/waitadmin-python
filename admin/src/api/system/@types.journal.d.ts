/**
 * 系统日志列表类型
 */
interface SystemJournalListResponse {
    // ID
    id: number;
    // 操作人
    admin: string;
    // 摘要信息
    summary: string;
    // 请求方式: [GET, POST, PUT, DELETE, OPTION]
    method: string;
    // 请求路由
    url: string;
    // 请求IP
    ip: string;
    // 请求UA
    ua: string;
    // 错误信息
    error: string;
    // 执行状态: [1=运行, 2=失败]
    status: number;
    // 最大执行时长
    task_time: number;
    // 创建时间
    create_time: string;
}

/**
 * 系统日志详情类型
 */
interface SystemJournalDetailResponse {
    // ID
    id: number;
    // 操作昵称
    nickname: string;
    // 操作账号
    username: string;
    // 摘要信息
    summary: string;
    // 请求方式: [GET, POST, PUT, DELETE, OPTION]
    method: string;
    // 请求路由
    url: string;
    // 请求IP
    ip: string;
    // 请求UA
    ua: string;
    // UA详情
    user_agent: string;
    // 执行函数
    endpoint: string;
    // 请求参数
    params: string;
    // 错误信息
    error: string;
    // 执行状态: [1=运行, 2=失败]
    status: number;
    // 最大执行时长
    task_time: number;
    // 开始执行结束执行时间时间
    start_time: string;
    // 结束执行时间
    end_time: string;
    // 创建时间
    create_time: string;
}
