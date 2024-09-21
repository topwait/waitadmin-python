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
from typing import List, Dict
from pydantic import BaseModel, Field


class UploadResultVo(BaseModel):
    """ 上传结果Vo """
    id: int = Field(description="主键")
    name: str = Field(description="文件名称")
    size: int = Field(description="文件大小")
    ext: str = Field(description="文件扩展")
    path: str = Field(description="文件路径")
    url: str = Field(description="访问路径")


class SysConfigVo(BaseModel):
    """ 后台配置项Vo """
    name: str = Field(description="网站名称")
    title: str = Field(description="网站名称")
    cover: str = Field(description="登录封面")
    favicon: str = Field(description="站点图标")
    logo_black_big: str = Field(max_length=500, description="深色大logo")
    logo_black_small: str = Field(max_length=500, description="深色小logo")
    logo_white_big: str = Field(max_length=500, description="浅色大logo")
    logo_white_small: str = Field( max_length=500, description="浅色小logo")
    enable_captcha: bool = Field(description="启用验证码")


class WorkbenchVo(BaseModel):
    """ 控制台数据Vo """
    version: dict = Field(description="版本信息")
    today: List[dict] = Field(description="今日数据")
    shortcut: List[Dict] = Field(description="快捷方式")
    backlogs: List[Dict] = Field(description="待办事项")
    echartsVisitor: Dict[str, list] = Field(description="访客的趋势图")
    echartsWebsite: List[dict] = Field(description="浏览器趋势图")
