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
from pydantic import TypeAdapter
from hypertext import PagingResult
from apps.admin.schemas.setting import links_schema as schema
from common.models.dev import DevLinksModel
from common.utils.urls import UrlUtil
from common.utils.times import TimeUtil


class LinksService:
    """ 友情链接服务类 """

    @classmethod
    async def lists(cls, params: schema.LinksSearchIn) -> PagingResult[schema.LinksListVo]:
        """
         友情链接列表(分页)

        Args:
            params (schema.LinksSearchIn): 友链查询参数对象。

        Returns:
            PagingResult[schema.LinksListVo]:  友链分页列表Vo。

        Author:
            zero
        """
        _model = DevLinksModel.filter(is_delete=0).order_by("-sort", "-id")
        _pager = await DevLinksModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=DevLinksModel.without_field("is_delete,delete_time"),
        )

        _data = []
        for item in _pager.lists:
            item["image"] = await UrlUtil.to_absolute_url(item["image"])
            _data.append(TypeAdapter(schema.LinksListVo).validate_python(item))

        _pager.lists = _data
        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.LinksDetailVo:
        """
        友情链接详情。

        Args:
            id_ (int): 友情链接ID。

        Returns:
            LinksDetailVo: 友情链接详情Vo。

        Author:
            zero
        """
        data = await DevLinksModel.get(id=id_).values()
        data["create_time"] = TimeUtil.timestamp_to_date(data["create_time"])
        data["update_time"] = TimeUtil.timestamp_to_date(data["update_time"])
        data["image"] = await UrlUtil.to_absolute_url(data["image"])
        return TypeAdapter(schema.LinksDetailVo).validate_python(data)

    @classmethod
    async def add(cls, post: schema.LinksAddIn):
        """
         友情链接新增。

        Args:
            post (schema.LinksAddIn):  友链新增参数。

        Author:
            zero
        """
        await DevLinksModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.LinksEditIn):
        """
         友情链接编辑。

        Args:
            post (schema.LinksEditIn): 友链编辑参数。

        Author:
            zero
        """
        params = post.dict()
        del params["id"]

        await DevLinksModel.filter(id=post.id).update(
            **params,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        友情链接删除。

        Args:
            id_ (int): 友链ID。

        Author:
            zero
        """
        banner = await DevLinksModel.filter(id=id_, is_delete=0).get()
        banner.is_delete = 1
        banner.delete_time = int(time.time())
        await banner.save()
