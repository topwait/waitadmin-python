import request from '@/utils/request'

const noticeApi = {
    /**
     * 通知配置列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        client: number;
    }): Promise<any> {
        return request.get({
            url: '/setting/notice/lists',
            params
        })
    },

    /**
     * 通知配置详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/notice/detail',
            params: { id }
        })
    },

    /**
     * 通知配置保存
     */
    save(params: {
        id: number;
        scene: number;
        name: string;
        type: string;
        client: string;
        remarks?: string;
        variable: any;
        sys_template: any;
        ems_template: any;
        sms_template: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/notice/save',
            params
        })
    }
}

export default noticeApi
