import request from '@/utils/request'

const loginApi = {
    /**
     * 登录配置详情
     *
     * @returns {Promise<SettingLoginResponse>}
     * @author zero
     */
    detail(): Promise<SettingLoginResponse> {
        return request.get<SettingLoginResponse>({
            url: '/setting/login/detail'
        })
    },

    /**
     * 登录配置保存
     *
     * @param {SettingLoginResponse} params
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: SettingLoginResponse): Promise<any> {
        return request.post({
            url: '/setting/login/save',
            params
        })
    }
}

export default loginApi
