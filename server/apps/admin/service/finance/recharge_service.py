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
from pydantic import TypeAdapter
from tortoise.queryset import Q
from hypertext import PagingResult
from common.utils.urls import UrlUtil
from common.enums.pay import PayEnum
from common.models.users import UserModel
from common.models.market import RechargeOrderModel
from apps.admin.schemas.finance import recharge_schema as schema


class RechargeService:

    @classmethod
    async def lists(cls, params: schema.RechargeSearchIn) -> PagingResult[schema.RechargeListVo]:
        """
        充值记录列表。

        Args:
            params (schema.RechargeSearchIn): 充值记录查询参数。

        Returns:
            PagingResult[schema.RechargeListVo]: 充值记录分页列表Vo。

        Author:
            zero
        """
        where = RechargeOrderModel.build_search({
            "=": ["pay_way", "pay_status"],
            "%like%": ["order_sn"],
            "datetime": ["start_time|end_time@create_time"]
        }, params.__dict__)

        if params.user:
            ids = await UserModel.search_by_keyword(params.user)
            where.append(Q(user_id__in=list(set(ids))))

        _model = RechargeOrderModel.filter(*where).order_by("-id")
        _pager = await RechargeOrderModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            datetime_field=["create_time", "pay_time"]
        )

        user_ids = [item["user_id"] for item in _pager.lists if item["user_id"]]
        users = await UserModel.fetch_info_by_ids(user_ids)

        list_vo = []
        for item in _pager.lists:
            user_dict = users.get(item["user_id"]) or {}
            item["pay_time"] = item["pay_time"] or "-"
            item["create_time"] = item["create_time"] or "-"
            item["pay_way"] = PayEnum.get_pay_way_msg(item["pay_way"])
            item["user"] = {
                "sn": user_dict.get("sn", ""),
                "avatar": await UrlUtil.to_absolute_url(user_dict.get("avatar", "")),
                "nickname": user_dict.get("nickname", ""),
                "mobile": user_dict.get("mobile", "")
            }

            vo = TypeAdapter(schema.RechargeListVo).validate_python(item)
            list_vo.append(vo)

        _pager.lists = list_vo
        _pager.extend = {
            "payWay": PayEnum.get_pay_way_msg(True),
            "payStatus": PayEnum.get_pay_status_msg(True)
        }
        return _pager
