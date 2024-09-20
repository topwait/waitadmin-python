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
from common.models.users import UserModel
from common.models.users import UserGroupModel
from apps.admin.schemas.users import group_schema as schema


class UserGroupService:
    """ 用户分组服务类 """

    @classmethod
    async def whole(cls) -> List[schema.UserGroupWholeVo]:
        """
        所有用户分组列表

        Returns:
            List[AuthRoleWholeVo]: 所有用户分组列表Vo。

        Author:
            zero
        """
        _lists = await UserGroupModel.filter(is_delete=0).order_by("-sort", "-id").all().values("id", "name")
        return [TypeAdapter(schema.UserGroupWholeVo).validate_python(item) for item in _lists]

    @classmethod
    async def lists(cls, params: schema.UserGroupSearchIn) -> PagingResult[schema.UserGroupListVo]:
        """
        用户分组列表(分页)。

        Args:
            params (UserGroupSearchIn): 用户分组查询参数。

        Returns:
            PagingResult[UserGroupListVo]: 用户分组分页列表Vo。

        Author:
            zero
        """
        where = UserGroupModel.build_search({
            "%like%": ["name"]
        }, params.__dict__)

        _model = UserGroupModel.filter(is_delete=0).filter(*where).order_by("-sort", "-id")
        _pager = await UserGroupModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            schema=schema.UserGroupListVo,
            fields=UserGroupModel.without_field("is_delete,delete_time")
        )

        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.UserGroupDetailVo:
        """
        用户分组详情。

        Args:
            id_ (int): 用户分组ID。

        Returns:
            UserGroupDetailVo: 用户分组详情VO。

        Author:
            zero
        """
        data = await UserGroupModel.get(id=id_)
        return TypeAdapter(schema.UserGroupDetailVo).validate_python(data.__dict__)

    @classmethod
    async def add(cls, post: schema.UserGroupAddIn):
        """
        用户分组新增。

        Args:
            post (UserGroupAddIn): 用户分组新增参数。

        Author:
            zero
        """
        pn = await UserGroupModel.filter(name=post.name, is_delete=0)
        if pn:
            raise AppException("用户分组名称已被占用")

        await UserGroupModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.UserGroupEditIn):
        """
        用户分组编辑。

        Args:
            post (UserGroupEditIn): 用户分组编辑参数。

        Author:
            zero
        """
        _post = await UserGroupModel.filter(id=post.id, is_delete=0).first().values("id")
        if not _post:
            raise AppException("用户分组不存在")

        _post3 = await UserGroupModel.filter(name=post.name, id__not=post.id, is_delete=0).values("id")
        if _post3:
            raise AppException("用户分组名称已被占用")

        params = post.dict()
        del params["id"]

        await UserGroupModel.filter(id=post.id).update(
            **params,
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        用户分组删除。

        Args:
            id_ (int): 用户分组的ID。

        Author:
            zero
        """
        p = await UserGroupModel.filter(id=id_, is_delete=0).first().values("id")
        if not p:
            raise AppException("用户分组不存在")

        admin = await UserModel.filter(group_id=id_, is_delete=0).first().values("id")
        if admin:
            raise AppException("用户分组已被使用不能删除")

        await UserGroupModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
