import request from '@/utils/request'

const loginApi = {
    /**
     * 登录配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/login/detail'
        })
    },

    /**
     * 登录配置保存
     */
    save(params: {
        is_agreement: number;
        defaults: string;
        registers: string[];
        login_modes: string[];
        login_other: string[];
    }): Promise<any> {
        return request.post({
            url: '/setting/login/save',
            params
        })
    }
}

export default loginApi
