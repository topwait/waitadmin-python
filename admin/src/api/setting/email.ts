import request from '@/utils/request'

const emailApi = {
    /**
     * 邮箱配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/email/detail'
        })
    },

    /**
     * 邮箱配置保存
     */
    save(params: {
        smtp_type: string;
        smtp_host: string;
        smtp_port: string;
        smtp_user: string;
        smtp_pass: string;
        verify_type: string;
    }): Promise<any> {
        return request.post({
            url: '/setting/email/save',
            params
        })
    }
}

export default emailApi
