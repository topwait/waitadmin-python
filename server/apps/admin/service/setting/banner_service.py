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
import time
from typing import List
from pydantic import TypeAdapter
from hypertext import PagingResult
from apps.admin.schemas.setting import banner_schema as schema
from common.models.dev import DevBannerModel
from common.enums.public import BannerEnum
from common.utils.urls import UrlUtil
from common.utils.times import TimeUtil


class BannerService:
    """ 轮播图服务类 """

    @classmethod
    async def sites(cls) -> List[schema.BannerSiteVo]:
        """
        轮播图位置列表

        Returns:
            List[schema.BannerSiteVo]: 轮播图位置列表Vo。

        Author:
            zero
                """
        options = []
        for key, val in BannerEnum.get_positions().items():
            options.append(schema.BannerSiteVo(id=key, name=val))
        return options

    @classmethod
    async def lists(cls, params: schema.BannerSearchIn) -> PagingResult[schema.BannerListVo]:
        """
        轮播图列表(分页)

        Args:
            params (schema.BannerSearchIn): 播图查询参数。

        Returns:
            PagingResult[schema.BannerListVo]: 轮播图分页列表Vo。

        Author:
            zero
        """
        _model = DevBannerModel.filter(is_delete=0).order_by("-sort", "-id")
        _pager = await DevBannerModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=DevBannerModel.without_field("is_delete,delete_time"),
        )

        _data = []
        for item in _pager.lists:
            item["image"] = await UrlUtil.to_absolute_url(item["image"])
            item["position"] = BannerEnum.get_msg_by_code(item["position"]) or "-"
            _data.append(TypeAdapter(schema.BannerListVo).validate_python(item))

        _pager.lists = _data
        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.BannerDetailVo:
        """
        轮播图详情。

        Args:
            id_ (int): 轮播图ID。

        Returns:
            BannerDetailVo: 轮播图详情Vo。

        Author:
            zero
        """

        data = await DevBannerModel.get(id=id_).values()
        data["image"] = await UrlUtil.to_absolute_url(data["image"])
        data["create_time"] = TimeUtil.timestamp_to_date(data["create_time"])
        data["update_time"] = TimeUtil.timestamp_to_date(data["update_time"])
        return TypeAdapter(schema.BannerDetailVo).validate_python(data)

    @classmethod
    async def add(cls, post: schema.BannerAddIn):
        """
        轮播图新增。

        Args:
            post (schema.BannerAddIn): 轮播图新增参数。

        Author:
            zero
        """
        params = post.dict()
        params["image"] = UrlUtil.to_relative_url(params["image"])
        await DevBannerModel.create(
            **params,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.BannerEditIn):
        """
        轮播图编辑。

        Args:
            post (schema.BannerEditIn): 轮播图参数。

        Author:
            zero
        """
        params = post.dict()
        params["image"] = UrlUtil.to_relative_url(params["image"])
        del params["id"]

        await DevBannerModel.filter(id=post.id).update(
            **params,
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
         轮播图删除。

        Args:
            id_ (int): 轮播图ID。

        Author:
            zero
        """
        banner = await DevBannerModel.filter(id=id_, is_delete=0).get()

        banner.is_delete = 1
        banner.delete_time = int(time.time())
        await banner.save()
