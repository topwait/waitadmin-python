import request from '@/utils/request'
import type { FileParams } from '@/utils/request/type'

const appApi = {
    /**
     * 全局数据
     */
    config(): Promise<any> {
        return request.get({
            url: '/index/config'
        })
    },

    /**
     * 工作台数据
     */
    workbench(): Promise<any> {
        return request.get({
            url: '/index/workbench'
        })
    },

    /**
     * 文件上传
     */
    upload(params: FileParams, onProgress?: any): Promise<any> {
        return request.upload({
            url: '/upload/files',
            headers: {
                'Content-Type': 'multipart/form-data;charset=UTF-8'
            },
            onUploadProgress(progressEvent): void {
                onProgress && onProgress(progressEvent)
            }
        }, params)
    }
}

export default appApi
