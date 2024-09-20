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
from exception import AppException
from common.models.auth import AuthAdminModel
from common.models.auth import AuthPostModel
from apps.admin.schemas.auth import post_schema as schema


class PostService:
    """ 系统岗位服务类 """

    @classmethod
    async def whole(cls) -> List[schema.AuthPostWholeVo]:
        """
        所有岗位。

        Returns:
            List[schema.AuthPostWholeVo]: 所有岗位列表Vo。

        Author:
            zero
        """
        fields = ["id", "code", "name"]
        lists = await AuthPostModel.filter(is_delete=0).order_by("-sort", "-id").all().values(*fields)
        return [TypeAdapter(schema.AuthPostWholeVo).validate_python(item) for item in lists]

    @classmethod
    async def lists(cls, params: schema.AuthPostSearchIn) -> PagingResult[schema.AuthPostListVo]:
        """
        岗位列表。

        Args:
            params (schema.AuthPostSearchIn): 岗位查询参数。

        Returns:
            PagingResult[schema.AuthPostListVo]: 岗位分页列表Vo。

        Author:
            zero
        """
        where = AuthPostModel.build_search({
            "%like%": ["code", "name"],
            "=": ["is_disable"]
        }, params.__dict__)

        _model = AuthPostModel.filter(is_delete=0).filter(*where).order_by("-sort", "-id")
        _pager = await AuthPostModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            schema=schema.AuthPostListVo,
            fields=AuthPostModel.without_field("is_delete,delete_time")
        )

        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.AuthPostDetailVo:
        """
        岗位详情。

        Args:
            id_ (int): 岗位ID。

        Returns:
            schema.AuthRoleDetailVo: 岗位详情Vo。

        Author:
            zero
        """
        data = await AuthPostModel.get(id=id_)
        return TypeAdapter(schema.AuthPostDetailVo).validate_python(data.__dict__)

    @classmethod
    async def add(cls, post: schema.AuthPostAddIn):
        """
        岗位新增。

        Args:
            post (schema.AuthRoleAddIn): 岗位新增参数。

        Author:
            zero
        """
        pc = await AuthPostModel.filter(code=post.code, is_delete=0)
        if pc:
            raise AppException("岗位编号已被占用")

        pn = await AuthPostModel.filter(name=post.name, is_delete=0)
        if pn:
            raise AppException("岗位名称已被占用")

        await AuthPostModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.AuthPostEditIn):
        """
        岗位编辑。

        Args:
            post (schema.AuthRoleEditIn): 岗位编辑参数。

        Author:
            zero
        """
        _post = await AuthPostModel.filter(id=post.id, is_delete=0).first().values("id")
        if not _post:
            raise AppException("岗位不存在")

        _post2 = await AuthPostModel.filter(code=post.code, id__not=post.id, is_delete=0).values("id")
        if _post2:
            raise AppException("岗位编号已被占用")

        _post3 = await AuthPostModel.filter(name=post.name, id__not=post.id, is_delete=0).values("id")
        if _post3:
            raise AppException("岗位名称已被占用")

        params = post.dict()
        del params["id"]

        await AuthPostModel.filter(id=post.id).update(
            **params,
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        岗位删除。

        Args:
            id_ (int): 岗位的ID。

        Author:
            zero
        """
        p = await AuthPostModel.filter(id=id_, is_delete=0).first().values("id")
        if not p:
            raise AppException("岗位不存在")

        admin = await AuthAdminModel.filter(post_id=id_, is_delete=0).first().values("id")
        if admin:
            raise AppException("岗位已被使用不能删除")

        await AuthPostModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
