import request from '@/utils/request'
import type { FileParams } from '@/utils/request/type'
import type { AxiosProgressEvent } from 'axios'

const appApi = {
    /**
     * 全局数据
     */
    config(): Promise<AppConfigResponse> {
        return request.get({
            url: '/index/config'
        })
    },

    /**
     * 工作台数据
     */
    workbench(): Promise<AppWorkbenchResponse> {
        return request.get({
            url: '/index/workbench'
        })
    },

    /**
     * 文件上传
     */
    upload(params: FileParams, onProgress?: any): Promise<AppUploadResponse> {
        return request.upload<AppUploadResponse>({
            url: '/upload/files',
            headers: {
                'Content-Type': 'multipart/form-data;charset=UTF-8'
            },
            onUploadProgress(progressEvent: AxiosProgressEvent): void {
                onProgress && onProgress(progressEvent)
            }
        }, params)
    }
}

export default appApi
