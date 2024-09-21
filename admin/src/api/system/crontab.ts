import request from '@/utils/request'

const crontabApi = {
    /**
     * 定时任务列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/system/crontab/lists',
            params
        })
    },

    /**
     * 定时任务详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/system/crontab/detail',
            params: { id }
        })
    },

    /**
     * 定时任务新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/system/crontab/add',
            params
        })
    },

    /**
     * 定时任务编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/system/crontab/edit',
            params
        })
    },

    /**
     * 定时任务删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/system/crontab/delete',
            params: { id: id }
        })
    }
}

export default crontabApi
