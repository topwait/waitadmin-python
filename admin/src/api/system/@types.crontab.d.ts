/**
 * 定时任务列表类型
 */
interface SystemCrontabListResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 命令
    command: string;
    // 参数
    params: string;
    // 错误
    error: string;
    // 备注
    remarks: string;
    // 条件
    condition: string[];
    // 并发
    concurrent: number;
    // 状态
    status: number;
    // 执行时间
    exe_time: number;
    // 最后执行时间
    last_time: string;
}

/**
 * 定时任务详情类型
 */
interface SystemCrontabDetailResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 命令
    command: string;
    // 参数
    params: string;
    // 规则
    rules: {
        key: string;
        value: string;
    }[],
    // 备注
    remarks: string;
    // 并发
    concurrent: number;
    // 状态
    status: number;
    // 任务
    tasks: {
        // ID
        id: string;
        // 下次执行时间
        next_run_time: string;
    }[]
}
