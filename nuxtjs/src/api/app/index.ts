import type { FileParams } from 'ofetch'

const appApi = {
    /**
     * 主页数据
     */
    homing(): Promise<AppHomingResponse> {
        return $request.get<AppHomingResponse>({
            url: '/index/homing'
        })
    },

    /**
     * 系统配置
     */
    config(): Promise<AppConfigResponse> {
        return $request.get<AppConfigResponse>({
            url: '/index/config'
        })
    },

    /**
     * 政策协议
     */
    policy(type: string): Promise<AppPolicyResponse> {
        return $request.get<AppPolicyResponse>({
            url: '/index/policy',
            params: {
                type
            }
        })
    },

    /**
     * 上传附件
     *
     * @param {FileParams} params
     * @param {File} params.file - 要上传的文件对象
     * @param {string} [params.name] - 文件的名称[可选]
     * @param {any} [params.data] - 附加的上传数据[可选]
     * @returns {Promise<AppUploadResponse>}
     * @author zero
     */
    upload(params: FileParams): Promise<AppUploadResponse> {
        return $request.uploadFile<AppUploadResponse>({
            url: '/upload/files'
        }, {
            file: params.file,
            name: params?.name,
            data: params?.data
        })
    },

    /**
     * 发送短信
     *
     * @param {Object} params
     * @param {number} params.scene - 发送场景
     * @param {string} params.mobile - 接收手机
     * @returns {Promise<any>}
     * @author zero
     */
    sendSms(params: { scene: number, mobile: string }): Promise<any> {
        return $request.post({
            url: '/index/send_sms',
            params: {
                scene: params.scene,
                mobile: params.mobile
            }
        })
    },

    /**
     * 发送邮件
     *
     * @param {Object} params
     * @param {number} params.scene - 发送场景
     * @param {string} params.email - 接收邮箱
     * @returns {Promise<any>}
     * @author zero
     */
    sendEmail(params: { scene: number, email: string }): Promise<any> {
        return $request.post({
            url: '/index/send_email',
            params: {
                scene: params.scene,
                email: params.email
            }
        })
    }
}

export default appApi