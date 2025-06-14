import request from '@/utils/request'

const crontabApi = {
    /**
     * 定时任务列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
    }): Promise<any> {
        return request.get({
            url: '/system/crontab/lists',
            params
        })
    },

    /**
     * 定时任务详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/system/crontab/detail',
            params: { id }
        })
    },

    /**
     * 定时任务新增
     *
     * @param {Object} params
     * @param {string} params.name
     * @param {string} params.command
     * @param {string} [params.params]
     * @param {string} [params.trigger]
     * @param {any[]} [params.rules]
     * @param {number} [params.concurrent]
     * @param {string} [params.remarks]
     * @param {number} [params.status]
     */
    add(params: {
        name: string;
        command: string;
        params?: string;
        trigger?: string;
        rules?: any[];
        concurrent?: number;
        remarks?: string;
        status?: number;
    }): Promise<any> {
        return request.post({
            url: '/system/crontab/add',
            params
        })
    },

    /**
     * 定时任务编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.name
     * @param {string} params.command
     * @param {string} [params.params]
     * @param {string} [params.trigger]
     * @param {any[]} [params.rules]
     * @param {number} [params.concurrent]
     * @param {string} [params.remarks]
     * @param {number} [params.status]
     */
    edit(params: {
        id: number;
        name: string;
        command: string;
        params?: string;
        trigger?: string;
        rules?: any[];
        concurrent?: number;
        remarks?: string;
        status?: number;
    }): Promise<any> {
        return request.post({
            url: '/system/crontab/edit',
            params
        })
    },

    /**
     * 定时任务删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/system/crontab/delete',
            params: { id: id }
        })
    }
}

export default crontabApi
