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
from tortoise.queryset import Q
from hypertext import PagingResult
from exception import AppException
from common.utils.urls import UrlUtil
from common.utils.tools import ToolsUtil
from apps.admin.service.auth.menu_service import MenuService
from apps.admin.schemas.auth import admin_schema as schema
from common.models.auth import (
    AuthAdminModel,
    AuthRoleModel,
    AuthDeptModel,
    AuthMenuModel,
    AuthPermModel
)


class AdminService:
    """ 系统管理员服务类 """

    @classmethod
    async def lists(cls, params: schema.AuthAdminSearchIn) -> PagingResult[schema.AuthAdminListVo]:
        """
        管理员列表。

        Args:
            params (schema.AuthAdminSearchIn): 管理员查询参数。

        Returns:
            PagingResult[schema.AuthAdminListVo]: 管理员分页列表Vo。

        Author:
            zero
        """
        where = [Q(is_delete=0)]
        if params.username:
            where.append(Q(username__icontains=params.username))
        if params.mobile:
            where.append(Q(mobile__icontains=params.mobile))
        if params.role:
            where.append(Q(role_id=int(params.role)))

        _model = AuthAdminModel.filter(*where).order_by("-id")
        _pager = await AuthAdminModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=AuthAdminModel.without_field("password,salt,is_delete,delete_time"),
            datetime_field=["create_time", "update_time", "last_login_time"]
        )

        role_ids = [item["role_id"] for item in _pager.lists if item["role_id"]]
        dept_ids = [item["dept_id"] for item in _pager.lists if item["dept_id"]]

        role_ = {}
        if role_ids:
            role_ = await AuthRoleModel.filter(id__in=list(set(role_ids))).all().values_list("id", "name")
            role_ = {k: v for k, v in role_}

        dept_ = {}
        if dept_ids:
            dept_ = await AuthDeptModel.filter(id__in=list(set(dept_ids))).all().values_list("id", "name")
            dept_ = {k: v for k, v in dept_}

        list_vo = []
        for item in _pager.lists:
            item["role"] = "系统管理员" if item["id"] == 1 else role_.get(item["role_id"], "-")
            item["dept"] = dept_.get(item["dept_id"], "-")
            item["mobile"] = item["mobile"] or "-"
            item["avatar"] = await UrlUtil.to_absolute_url(item["avatar"])
            item["last_login_ip"] = item["last_login_ip"] or "-"
            item["last_login_time"] = item["last_login_time"] or "-"

            vo = TypeAdapter(schema.AuthAdminListVo).validate_python(item)
            list_vo.append(vo)

        _pager.lists = list_vo
        return _pager

    @classmethod
    async def oneself(cls, id_: int) -> schema.AuthAdminOneselfVo:
        """
        管理员自身。

        Args:
            id_ (int): 管理员ID。

        Returns:
            schema.AuthAdminOneselfVo: 管理员信息Vo。

        Author:
            zero
        """
        # 管理员信息
        admin = await AuthAdminModel.get(id=id_)
        if not admin or admin.is_delete == 1:
            raise AppException("管理员不存在")

        if admin.is_disable == 1:
            raise AppException("管理员被禁用")

        # 管理员角色
        role_name = "-"

        # 管理员权限
        perms = []
        if admin.id == 1:
            perms.append("*")
        else:
            role = await AuthRoleModel.filter(id=admin.role_id).first()
            if role:
                role_name = role.name
                menu_ids = await AuthPermModel.filter(role_id=admin.role_id).all().values("menu_id")
                menu_ids = [item["menu_id"] for item in menu_ids]
                if menu_ids:
                    menus = await AuthMenuModel.filter(id__in=menu_ids).all().values("perms")
                    perms = [item["perms"] for item in menus]
            else:
                admin.role_id = 0
                await admin.save()

        admin_vo = TypeAdapter(schema.AuthAdminDetailVo).validate_python(admin.__dict__)
        admin_vo.avatar = await UrlUtil.to_absolute_url(admin.avatar)
        admin_vo.role = "系统管理员" if admin.id == 1 else role_name

        routes = await MenuService.routes(admin.id, admin.role_id)
        return schema.AuthAdminOneselfVo(
            user=admin_vo,
            perms=perms,
            menus=routes
        )

    @classmethod
    async def detail(cls, id_: int) -> schema.AuthAdminDetailVo:
        """
        管理员详细。

        Args:
            id_ (int): 管理员ID。

        Returns:
            schema.AuthAdminDetailVo: 管理员详细Vo。

        Author:
            zero
        """
        admin = await AuthAdminModel.get(id=id_)
        admin.avatar = await UrlUtil.to_absolute_url(admin.avatar)
        return TypeAdapter(schema.AuthAdminDetailVo).validate_python(admin.__dict__)

    @classmethod
    async def add(cls, post: schema.AuthAdminAddIn):
        """
        管理员新增

        Args:
            post (schema.AuthAdminAddIn): 管理员新增参数。

        Author:
            zero
        """
        if await AuthAdminModel.filter(nickname=post.nickname, is_delete=0).first().only("id"):
            raise AppException("昵称已被占用")

        if await AuthAdminModel.filter(username=post.nickname, is_delete=0).first().only("id"):
            raise AppException("账号已被占用")

        if post.mobile:
            if await AuthAdminModel.filter(mobile=post.mobile, is_delete=0).first().only("id"):
                raise AppException("手机号已被占用")

        if post.email:
            if await AuthAdminModel.filter(email=post.email, is_delete=0).first().only("id"):
                raise AppException("邮箱号已被占用")

        params = post.dict()
        params["salt"] = ToolsUtil.make_rand_char(6)
        params["avatar"] = UrlUtil.to_relative_url(post.avatar)
        params["password"] = ToolsUtil.make_md5_str(post.password, params["salt"])
        params["create_time"] = int(time.time())
        params["update_time"] = int(time.time())

        await AuthAdminModel.create(**params)

    @classmethod
    async def edit(cls, post: schema.AuthAdminEditIn, admin_id: int):
        """
        管理员编辑。

        Args:
            post (schema.AuthAdminEditIn): 管理编辑参数。
            admin_id (int): 当前操作的管理员的ID。

        Author:
            zero
        """
        pass
        admin = await AuthAdminModel.filter(id=post.id, is_delete=0).first()
        if not admin:
            raise AppException("管理员不存在")

        if post.id == 1 and admin_id != 1:
            raise AppException("您无权限操作")

        if admin.nickname != post.nickname:
            if await AuthAdminModel.filter(id__not=admin.id, nickname=post.nickname, is_delete=0).first().only("id"):
                raise AppException("昵称已被占用")

        if admin.username != post.username:
            if await AuthAdminModel.filter(id__not=admin.id, username=post.nickname, is_delete=0).first().only("id"):
                raise AppException("账号已被占用")

        if post.mobile:
            if await AuthAdminModel.filter(id__not=admin.id, mobile=post.mobile, is_delete=0).first().only("id"):
                raise AppException("手机号已被占用")

        if post.email:
            if await AuthAdminModel.filter(id__not=admin.id, email=post.email, is_delete=0).first().only("id"):
                raise AppException("邮箱号已被占用")

        params = post.dict()
        params["avatar"] = UrlUtil.to_relative_url(post.avatar)
        params["update_time"] = time.time()
        params["password"] = admin.password
        if post.password:
            params["salt"] = ToolsUtil.make_rand_char(6)
            params["password"] = ToolsUtil.make_md5_str(post.password, params["salt"])

        del params["id"]
        await AuthAdminModel.filter(id=post.id).update(**params)

    @classmethod
    async def delete(cls, id_: int, admin_id: int):
        """
        管理员删除。

        Args:
            id_ (int): 要删除的管理员的主键ID。
            admin_id (int): 当前操作的管理员的ID。

        Author:
            zero
        """
        admin = await AuthAdminModel.filter(id=id_, is_delete=0).first()
        if not admin:
            raise AppException("管理员不存在")

        if id_ == admin_id:
            raise AppException("不能删除自己")

        if id_ == 1:
            raise AppException("系统管理员禁止删除")

        await AuthAdminModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))

    @classmethod
    async def set_info(cls, post: schema.AuthAdminInfoIn, admin_id: int):
        """
        管理员设置。

        Args:
            post (schema.AuthAdminInfoIn): 管理编辑参数。
            admin_id (int): 当前操作的管理员的ID。

        Author:
            zero
        """
        admin = await AuthAdminModel.filter(id=admin_id, is_delete=0).first()
        if not admin:
            raise AppException("管理员不存在")

        update_dict = {"update_time": int(time.time())}
        if post.password:
            password_old = ToolsUtil.make_md5_str(post.password_old, admin.salt)
            if admin.password != password_old:
                raise AppException("旧密码不正确")
            if len(post.password) < 6:
                raise AppException("新密码不能少于6位数")

        if post.password:
            update_dict["salt"] = ToolsUtil.make_rand_char(6)
            update_dict["password"] = ToolsUtil.make_md5_str(post.password, update_dict["salt"])

        if post.avatar:
            update_dict["avatar"] = UrlUtil.to_relative_url(post.avatar)

        if post.nickname != admin.nickname:
            if await AuthAdminModel.filter(id__not=admin_id, nickname=post.nickname, is_delete=0).first().only("id"):
                raise AppException("昵称已被占用")
            update_dict["nickname"] = post.nickname

        if post.mobile:
            if await AuthAdminModel.filter(id__not=admin_id, mobile=post.mobile, is_delete=0).first().only("id"):
                raise AppException("手机号已被占用")

        if post.email:
            if await AuthAdminModel.filter(id__not=admin_id, email=post.email, is_delete=0).first().only("id"):
                raise AppException("邮箱号已被占用")

        await AuthAdminModel.filter(id=admin_id).update(**update_dict)
