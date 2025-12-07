import request from '@/utils/request'

const emailApi = {
    /**
     * 邮箱配置详情
     *
     * @returns {Promise<SettingEmailResponse>}
     * @author zero
     */
    detail(): Promise<SettingEmailResponse> {
        return request.get<SettingEmailResponse>({
            url: '/setting/email/detail'
        })
    },

    /**
     * 邮箱配置保存
     *
     * @param {Object} params
     * @param {string} params.smtp_type
     * @param {string} params.smtp_host
     * @param {string} params.smtp_port
     * @param {string} params.smtp_user
     * @param {string} params.smtp_pass
     * @param {string} params.verify_type
     * @returns {Promise<any>}
     * @author zero
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
