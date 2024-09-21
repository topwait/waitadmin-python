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
from common.enums.wallet import WalletEnum
from common.models.users import UserModel
from common.models.users import UserWalletModel
from apps.admin.schemas.finance import balance_schema as schema


class BalanceService:

    @classmethod
    async def lists(cls, params: schema.BalanceSearchIn) -> PagingResult[schema.BalanceListVo]:
        """
        余额明细列表。

        Args:
            params (schema.BalanceSearchIn): 余额明细查询参数。

        Returns:
            PagingResult[schema.BalanceListVo]: 余额明细分页列表Vo。

        Author:
            zero
        """
        where = UserWalletModel.build_search({
            "=": ["action", "source_type"],
            "%like%": ["source_sn"],
            "datetime": ["start_time|end_time@create_time"]
        }, params.__dict__)

        if params.user:
            user = await (UserModel
                          .filter(Q(sn=params.user) | Q(nickname=params.user) | Q(mobile=params.user))
                          .filter(is_delete=0)
                          .limit(100)
                          .values("id"))

            user_ids = [item["id"] for item in user if item["id"]]
            if user_ids:
                where.append(Q(user_id__in=list(set(user_ids))))

        _model = UserWalletModel.filter(*where).order_by("-id")
        _pager = await UserWalletModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
        )

        users = {}
        user_ids = [item["user_id"] for item in _pager.lists if item["user_id"]]
        if user_ids:
            user_ = await UserModel.filter(id__in=list(set(user_ids))).all().values("id", "sn", "nickname", "mobile", "avatar")
            for item in user_:
                users[item["id"]] = item

        list_vo = []
        for item in _pager.lists:
            user_dict = users.get(item["user_id"]) or {}
            item["create_time"] = item["create_time"] or "-"
            item["source_sn"] = item["source_sn"] or "-"
            item["source_type"] = WalletEnum.get_source_type_msg(item["source_type"])
            item["user"] = {
                "sn": user_dict.get("sn", ""),
                "avatar": await UrlUtil.to_absolute_url(user_dict.get("avatar", "")),
                "mobile": user_dict.get("mobile", ""),
                "nickname": user_dict.get("nickname", "")
            }

            vo = TypeAdapter(schema.BalanceListVo).validate_python(item)
            list_vo.append(vo)

        _pager.lists = list_vo
        _pager.extend = {"types": WalletEnum.get_source_type_msg(True)}
        return _pager
