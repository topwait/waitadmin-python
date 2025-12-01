/**
 * 定时任务列表类型
 */
interface SystemCrontabListResponse {
    // ID
    id: number;
    // 任务名称
    name: string;
    // 命令
    command: string;
    // 参数
    params: string;
    // 错误原因
    error: string;
    // 备注信息
    remarks: string;
    // 运行规则
    condition: string[];
    // 并发数量
    concurrent: number;
    // 执行状态: [1=运行, 2=暂停, 3=错误]
    status: number | 1 | 2 | 3;
    // 执行时长
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
    // 备注信息
    remarks: string;
    // 并发数量
    concurrent: number;
    // 执行状态: [1=运行, 2=暂停, 3=错误]
    status: number | 1 | 2 | 3;
    // 任务列表
    tasks: {
        // ID
        id: string;
        // 下次执行时间
        next_run_time: string;
    }[]
}
