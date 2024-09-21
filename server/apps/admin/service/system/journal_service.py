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
from typing import List
from pydantic import TypeAdapter
from hypertext import PagingResult
from common.utils.times import TimeUtil
from common.models.sys import SysLogModel
from common.models.auth import AuthAdminModel
from apps.admin.schemas.system import journal_schema as schema


class JournalService:
    """ 系统日志服务类 """

    @classmethod
    async def lists(cls, params: schema.JournalSearchIn) -> PagingResult[schema.JournalListVo]:
        """
        系统日志列表。

        Args:
            params (schema.JournalSearchIn): 系统日志查询参数。

        Returns:
            PagingResult[schema.JournalListVo]: 系统日志分页列表Vo。

        Author:
            zero
        """
        where = SysLogModel.build_search({
            "=": ["method", "ip"],
            "%like%": ["url"],
            "datetime": ["start_time|end_time@create_time"]
        }, params.__dict__)

        _model = SysLogModel.filter(*where).order_by("-id")
        _pager = await SysLogModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=SysLogModel.without_field("params,endpoint,user_agent,start_time,end_time")
        )

        admin_ids: List[int] = [item["admin_id"] for item in _pager.lists if item["admin_id"]]
        admin_dict = {}
        if admin_ids:
            admin_objs = await AuthAdminModel.filter(id__in=list(set(admin_ids))).all().values_list("id", "nickname")
            admin_dict = {k: v for k, v in admin_objs}

        for item in _pager.lists:
            item["admin"] = admin_dict.get(item["admin_id"], "-")
            item["summary"] = item["summary"] if item["summary"] else "-"

        _pager.lists = [TypeAdapter(schema.JournalListVo).validate_python(item) for item in _pager.lists]
        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.JournalDetailVo:
        """
        系统日志详细。

        Args:
            id_ (int): 日志ID。

        Returns:
            PagingResult[schema.JournalDetailVo]: 系统日志详情Vo。

        Author:
            zero
        """
        log = await SysLogModel.get(id=id_).values()

        if log["admin_id"]:
            admin = await AuthAdminModel.filter(id=log["admin_id"]).first().values("nickname", "username")
            log["nickname"] = admin.get("nickname", "")
            log["username"] = admin.get("username", "")

        start_time = log["start_time"].split(".")
        end_time = log["end_time"].split(".")
        log["start_time"] = TimeUtil.timestamp_to_date(int(start_time[0])) + "." + start_time[1]
        log["end_time"] = TimeUtil.timestamp_to_date(int(end_time[0])) + "." + end_time[1]
        log["create_time"] = TimeUtil.timestamp_to_date(log["create_time"])

        return TypeAdapter(schema.JournalDetailVo).validate_python(log)
