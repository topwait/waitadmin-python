import request from '@/utils/request'

const storageApi = {
    /**
     * 存储配置详情
     *
     * @returns {Promise<SettingStorageResponse>}
     * @author zero
     */
    detail(): Promise<SettingStorageResponse> {
        return request.get<SettingStorageResponse>({
            url: '/setting/storage/detail'
        })
    },

    /**
     * 存储配置保存
     *
     * @param {Object} params
     * @param {string} params.drive
     * @param {any} params.local
     * @param {any} params.qiniu
     * @param {any} params.aliyun
     * @param {any} params.qcloud
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: {
        drive: string;
        local: any;
        qiniu: any;
        aliyun: any;
        qcloud: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/storage/save',
            params
        })
    }
}

export default storageApi
