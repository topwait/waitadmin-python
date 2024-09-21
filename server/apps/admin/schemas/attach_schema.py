# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin-python
# | github:  https://github.com/topwait/waitadmin-python
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
from typing import Union, List
from fastapi import Query
from pydantic import BaseModel, Field


class AlbumSearchIn(BaseModel):
    """ 附件搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    cid: Union[int, None] = Query(default=None, description="所属分类")
    type: Union[int, None] = Query(default=None, description="文件类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")
    keyword: Union[str, None] = Query(default=None, description="关键词")


class AlbumMoveIn(BaseModel):
    """ 附件移动参数 """
    ids: List[int] = Field(..., description="文件ID")
    cid: int = Field(..., ge=-1, description="分类ID")

    class Config:
        json_schema_extra = {
            "example": {
                "ids": [1, 2],
                "cid": 1
            }
        }


class AlbumRenameIn(BaseModel):
    """ 附件命名参数 """
    id: int = Field(..., gt=0, description="文件ID")
    name: str = Field(..., max_length=200, description="文件名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id:": 1,
                "name": "poster.png"
            }
        }


class AlbumDeleteIn(BaseModel):
    """ 附件删除参数 """
    ids: List[int] = Field(..., description="文件ID")

    class Config:
        json_schema_extra = {
            "example": {
                "ids:": [1, 2]
            }
        }


class AlbumCateSearchIn(BaseModel):
    """ 分类搜索参数 """
    type: Union[int, None] = Query(default=10, description="分类类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")


class AlbumCateCreateIn(BaseModel):
    """ 分类新增参数 """
    type: int = Field(..., description="分类类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")
    name: str = Field(..., max_length=20, description="分类名称")

    class Config:
        json_schema_extra = {
            "example": {
                "type:": 10,
                "name:": "Renovation"
            }
        }


class AlbumCateRenameIn(BaseModel):
    """ 分类命名参数 """
    id: int = Field(..., gt=0, description="分类ID")
    type: int = Field(..., gt=0, description="分类类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")
    name: str = Field(..., max_length=20, description="分类名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "type:": 10,
                "name:": "Renovation"
            }
        }


class AlbumCateDeleteIn(BaseModel):
    """ 分类删除参数 """
    id: int = Field(..., gt=0, description="分类ID")
    type: int = Field(..., gt=0, description="分类类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "type:": 10
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class AlbumListVo(BaseModel):
    """ 附件列表Vo """
    id: int = Field(description="主键")
    type: int = Field(description="文件类型: [10=图片, 20=视频, 30=音频, 40=压缩, 50=文件]")
    size: int = Field(description="文件大小")
    name: str = Field(description="文件名称")
    path: str = Field(description="文件路径")
    url: str = Field(description="文件地址")
    ext: str = Field(description="登录账号")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "type": 10,
                "size": 692774,
                "name": "poster.png",
                "path": "storage/image/poster.png",
                "url": "https://xx.com/storage/image/poster.png",
                "ext": "png",
                "create_time": "2024-04-23 11:19:49",
                "update_time": "2024-04-23 11:19:49"
            }
        }


class AlbumCateListVo(BaseModel):
    """ 分类列表Vo """
    id: int = Field(description="主键")
    name: str = Field(description="分类名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "poster"
            }
        }
