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
from typing import List, Dict
from pydantic import TypeAdapter
from tortoise.queryset import Q
from common.utils.times import TimeUtil
from common.utils.array import ArrayUtil
from common.models.auth import AuthMenuModel
from common.models.auth import AuthPermModel
from apps.admin.cache.login_cache import LoginCache
from apps.admin.schemas.auth import menu_schema as schema


class MenuService:
    """ 系统菜单服务类 """

    @classmethod
    async def whole(cls) -> List[schema.AuthMenuWholeVo]:
        """
        获取所有菜单(树型)。

        Returns:
            List[schema.AuthMenuWholeVo]: 菜单树型列表Vo。

        Author:
            zero
        """
        fields = ["id", "pid", "name"]
        lists = await AuthMenuModel.filter(is_delete=0).order_by("-sort", "id").all().values(*fields)

        vo_list = [TypeAdapter(schema.AuthMenuWholeVo).validate_python(item) for item in lists]
        vo_dict = [i.__dict__ for i in vo_list]
        return ArrayUtil.list_to_tree(vo_dict, "id", "pid", "children")

    @classmethod
    async def routes(cls, admin_id: int, role_id: int) -> List[schema.AuthMenuRoutesVo]:
        """
        根据角色获取菜单。

        Args:
            admin_id (int): 管理员ID。
            role_id (int): 角色ID。

        Returns:
            List[schema.AuthMenuRoutesVo]: 菜单树型路由列表Vo。

        Author:
            zero
        """
        menu_ids = await AuthPermModel.filter(role_id=role_id).all().values("menu_id")
        menu_ids = [item["menu_id"] for item in menu_ids] or [0]

        where = [Q(is_delete=0), Q(type__in=("M", "C"))]
        if admin_id != 1:
            where.append(Q(id__in=menu_ids))

        fields = AuthMenuModel.without_field("sort,is_delete,create_time,update_time.delete_time")
        menus = await AuthMenuModel.filter(*where).order_by("-sort", "id").all().values(*fields)

        vo_list = [TypeAdapter(schema.AuthMenuRoutesVo).validate_python(item) for item in menus]
        vo_dict: List[Dict] = [i.__dict__ for i in vo_list]
        return ArrayUtil.list_to_tree(vo_dict, "id", "pid", "children")

    @classmethod
    async def lists(cls) -> List[schema.AuthMenuListVo]:
        """
        菜单列表(树型)。

        Returns:
            List[schema.AuthMenuListVo]: 菜单树型列表Vo。

        Author:
            zero
        """
        fields = AuthMenuModel.without_field("is_delete,delete_time")
        lists = await AuthMenuModel.filter(is_delete=0).order_by("-sort", "id").all().values(*fields)
        for item in lists:
            item["create_time"] = TimeUtil.timestamp_to_date(item["create_time"])
            item["update_time"] = TimeUtil.timestamp_to_date(item["update_time"])

        vo_list = [TypeAdapter(schema.AuthMenuListVo).validate_python(item) for item in lists]
        vo_dict = [i.__dict__ for i in vo_list]
        return ArrayUtil.list_to_tree(vo_dict, "id", "pid", "children")

    @classmethod
    async def detail(cls, id_: int) -> schema.AuthMenuDetailVo:
        """
        菜单详情。

        Args:
            id_ (int): 菜单ID。

        Returns:
            schema.AuthMenuDetailVo: 菜单详情Vo。

        Author:
            zero
        """
        menu = await AuthMenuModel.get(id=id_)
        return TypeAdapter(schema.AuthMenuDetailVo).validate_python(menu.__dict__)

    @classmethod
    async def add(cls, post: schema.AuthMenuAddIn):
        """
        菜单新增。

        Args:
            post (schema.AuthMenuAddIn): 菜单新增参数。

        Author:
            zero
        """
        await AuthMenuModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        await LoginCache.role_perms_del()

    @classmethod
    async def edit(cls, post: schema.AuthMenuEditIn):
        """
        菜单编辑。

        Args:
            post (schema.AuthMenuEditIn): 菜单新增参数。

        Author:
            zero
        """
        params = post.dict()
        params["update_time"] = time.time()
        del params["id"]

        await AuthMenuModel.filter(id=post.id).update(**params)
        await LoginCache.role_perms_del()

    @classmethod
    async def delete(cls, id_: int):
        """
        菜单删除。

        Args:
            id_ (int): 菜单ID。

        Author:
            zero
        """
        await AuthMenuModel.filter(id=id_).update(
            is_delete=1,
            delete_time=int(time.time())
        )
        await LoginCache.role_perms_del()
