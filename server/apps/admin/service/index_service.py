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
from common.utils.urls import UrlUtil
from common.utils.times import TimeUtil
from common.utils.config import ConfigUtil
from common.models.users import UserVisitorModel
from apps.admin.schemas import common_schema as schema
from apps.admin.config import AdminConfig


class IndexService:
    """ 公共服务类 """

    @classmethod
    async def config(cls) -> schema.SysConfigVo:
        backs_conf = await ConfigUtil.get("backs") or {}
        return schema.SysConfigVo(
            name=backs_conf.get("name", ""),
            title=backs_conf.get("title", "fff"),
            cover=await UrlUtil.to_absolute_url(backs_conf.get("cover", "")),
            favicon=await UrlUtil.to_absolute_url(backs_conf.get("favicon", "")),
            logo_black_big=await UrlUtil.to_absolute_url(backs_conf.get("logo_black_big", "")),
            logo_black_small=await UrlUtil.to_absolute_url(backs_conf.get("logo_black_small", "")),
            logo_white_big=await UrlUtil.to_absolute_url(backs_conf.get("logo_white_big", "")),
            logo_white_small=await UrlUtil.to_absolute_url(backs_conf.get("logo_white_small", "")),
            enable_captcha=AdminConfig.enable_captcha
        )

    @classmethod
    async def workbench(cls) -> schema.WorkbenchVo:
        """
        控制台数据。

        Returns:
            schema.WorkbenchVo: 控制台数据Vo。

        Author:
            zero
        """
        visitor_list = []
        visitor_date = TimeUtil.near_to_date()
        for d in visitor_date:
            start_time: int = TimeUtil.date_to_timestamp(d, "%Y-%m-%d")
            end_time: int = start_time + 86400 - 1
            count: int = await UserVisitorModel.filter(create_time__gte=start_time, create_time__lte=end_time).count()
            visitor_list.append(count)

        ua_data = []
        for ua in ["chrome", "firefox", "ie", "safari", "wechat", "other"]:
            count: int = await UserVisitorModel.filter(
                create_time__gte=TimeUtil.today()[0],
                create_time__lte=TimeUtil.today()[1],
                ua=ua
            ).count()
            ua_data.append({"value": count, "name": ua.capitalize()})

        return schema.WorkbenchVo(
            version={
                "version": "1.0.0",
                "frame": "Fastapi + Vue3 + TypeScript",
                "tones": "零门槛 / 开源 / 商用 / 极简",
                "official": "https://www.waitadmin.cn"
            },
            today=[
                {
                    "name": "访问量",
                    "icon": await UrlUtil.to_absolute_url("static/images/gather_001.png"),
                    "value": 2000,
                    "total": 33,
                    "yesterday": 33
                },
                {
                    "name": "新增用户",
                    "icon": await UrlUtil.to_absolute_url("static/images/gather_002.png"),
                    "value": 20000,
                    "total": 33,
                    "yesterday": 33
                },
                {
                    "name": "文章数量",
                    "icon": await UrlUtil.to_absolute_url("static/images/gather_003.png"),
                    "value": 8000,
                    "total": 33,
                    "yesterday": 33
                },
                {
                    "name": "成交额",
                    "icon": await UrlUtil.to_absolute_url("static/images/gather_004.png"),
                    "value": 20303.00,
                    "total": 33,
                    "yesterday": 33
                }
            ],
            shortcut=[
                {"name": "内容", "icon": "el-icon-Tickets", "path": "/content/article"},
                {"name": "附件", "icon": "el-icon-Files", "path": "/system/materials"},
                {"name": "管理", "icon": "el-icon-Odometer", "path": "/auth/admin"},
                {"name": "菜单", "icon": "el-icon-SuitcaseLine", "path": "/auth/menu"},
                {"name": "任务", "icon": "el-icon-Box", "path": "/system/crontab"},
                {"name": "日志", "icon": "el-icon-Grape", "path": "/system/journal"},
                {"name": "缓存", "icon": "el-icon-Notification", "path": "/system/clear"},
                {"name": "设置", "icon": "el-icon-Setting", "path": "/setting/basics"},
            ],
            backlogs=[
                {"name": "待发货订单", "value": 60, "path": ""},
                {"name": "待核销订单", "value": 72, "path": ""},
                {"name": "待处理售后", "value": 22, "path": ""},
                {"name": "待回复评论", "value": 16, "path": ""},
            ],
            echartsVisitor={
                "date": visitor_date,
                "list": visitor_list
            },
            echartsWebsite=ua_data
        )
