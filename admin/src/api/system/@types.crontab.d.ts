/**
 * 定时任务列表类型
 */
interface SystemCrontabListResponse {
    id: number;
    name: string;
    command: string;
    params: string;
    error: string;
    remarks: string;
    condition: string[],
    concurrent: number;
    status: number;
    exe_time: number;
    last_time: string;
}

/**
 * 定时任务详情类型
 */
interface SystemCrontabDetailResponse {
    id: number;
    name: string;
    command: string;
    params: string;
    rules: {
        key: string;
        value: string;
    }[],
    remarks: string;
    concurrent: number;
    status: number;
    tasks: {
        id: string;
        next_run_time: string;
    }[]
}
