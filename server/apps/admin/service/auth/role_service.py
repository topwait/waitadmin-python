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
from common.models.auth import AuthRoleModel
from common.models.auth import AuthPermModel
from apps.admin.cache.login_cache import LoginCache
from apps.admin.schemas.auth import role_schema as schema


class RoleService:
    """ 系统角色服务类 """

    @classmethod
    async def whole(cls) -> List[schema.AuthRoleWholeVo]:
        """
        所有角色。

        Returns:
            List[schema.AuthRoleWholeVo]: 所有角色列表。

        Author:
            zero
        """
        _lists = await AuthRoleModel\
            .filter(is_delete=0)\
            .order_by("-sort", "-id")\
            .all()\
            .values("id", "name", "is_disable")

        return [TypeAdapter(schema.AuthRoleWholeVo).validate_python(item) for item in _lists]

    @classmethod
    async def lists(cls, params: schema.AuthRoleSearchIn) -> PagingResult[schema.AuthRoleListVo]:
        """
        角色列表。

        Args:
            params (schema.AuthRoleSearchIn): 角色查询参数。

        Returns:
            PagingResult[schema.AuthRoleListVo]: 角色分页列表Vo。

        Author:
            zero
        """
        _model = AuthRoleModel.filter(is_delete=0).order_by("-sort", "-id")
        _pager = await AuthRoleModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            schema=schema.AuthRoleListVo,
            fields=AuthRoleModel.without_field("is_delete,delete_time"),
        )

        for item in _pager.lists:
            item.admin_sum = await AuthAdminModel.filter(role_id=item.id, is_delete=0).count()

        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.AuthRoleDetailVo:
        """
        角色详情。

        Args:
            id_ (int): 角色ID。

        Returns:
            AuthRoleDetailVo: 角色详情Vo。

        Author:
            zero
        """
        role = await AuthRoleModel.get(id=id_)

        perms = await AuthPermModel.filter(role_id=role.id).all()
        menu_ids = [item.menu_id for item in perms]

        detail = role.__dict__
        detail["menu_ids"] = menu_ids
        return TypeAdapter(schema.AuthRoleDetailVo).validate_python(detail)

    @classmethod
    async def add(cls, post: schema.AuthRoleAddIn):
        """
        角色新增。

        Args:
            post (schema.AuthRoleAddIn): 角色新增参数。

        Author:
            zero
        """
        params = post.dict()
        del params["menu_ids"]

        role = await AuthRoleModel.create(
            **params,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        if post.menu_ids:
            for mid in post.menu_ids:
                await AuthPermModel.create(role_id=role.id, menu_id=mid)

        await LoginCache.role_perms_del()

    @classmethod
    async def edit(cls, post: schema.AuthRoleEditIn):
        """
        角色编辑。

        Args:
            post (schema.AuthRoleEditIn): 角色编辑参数。

        Author:
            zero
        """
        params = post.dict()
        del params["id"]
        del params["menu_ids"]

        await AuthRoleModel.filter(id=post.id).update(
            **params,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        await AuthPermModel.filter(role_id=post.id).delete()
        if post.menu_ids:
            for mid in post.menu_ids:
                await AuthPermModel.create(role_id=post.id, menu_id=mid)

        await LoginCache.role_perms_del()

    @classmethod
    async def delete(cls, id_: int):
        """
        角色删除。

        Args:
            id_ (int): 角色ID。

        Author:
            zero
        """
        role = await AuthRoleModel.filter(id=id_, is_delete=0).first()
        if not role:
            raise AppException("角色不存在")

        admin = await AuthAdminModel.filter(role_id=id_, is_delete=0).first()
        if admin:
            raise AppException("角色已被使用不能删除")

        await AuthRoleModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
        await LoginCache.role_perms_del()
