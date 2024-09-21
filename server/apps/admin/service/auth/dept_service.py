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
from tortoise.expressions import RawSQL
from exception import AppException
from common.utils.times import TimeUtil
from common.utils.array import ArrayUtil
from common.models.auth import AuthAdminModel
from common.models.auth import AuthDeptModel
from apps.admin.schemas.auth import dept_schema as schema


class DeptService:
    """ 系统部门服务类 """

    @classmethod
    async def whole(cls) -> List[schema.AuthDeptWholeVo]:
        """
        所有部门。

        Returns:
            List[schema.AuthDeptWholeVo]: 所有部门列表Vo。

        Author:
            zero
        """
        fields = ["id", "pid", "name", "is_disable"]
        lists = await AuthDeptModel.filter(is_delete=0).order_by("-sort", "-id").all().values(*fields)

        vo_list = [TypeAdapter(schema.AuthDeptWholeVo).validate_python(item) for item in lists]
        return ArrayUtil.list_to_tree([i.__dict__ for i in vo_list], "id", "pid", "children")

    @classmethod
    async def lists(cls, params: schema.AuthDeptSearchIn) -> List[schema.AuthDeptListVo]:
        """
        部门列表。

        Args:
            params (schema.AuthDeptSearchIn): 部门搜索参数。

        Returns:
            List[schema.AuthDeptListVo]: 部门树型列表Vo。

        Author:
            zero
        """
        where = AuthDeptModel.build_search({
            "%like%": ["name", "mobile"],
            "=": ["is_disable"]
        }, params.__dict__)

        fields = AuthDeptModel.without_field("level,relation,is_delete,delete_time")
        lists = await AuthDeptModel.filter(is_delete=0).filter(*where).order_by("-sort", "-id").all().values(*fields)

        for item in lists:
            item["update_time"] = TimeUtil.timestamp_to_date(item["update_time"])
            item["create_time"] = TimeUtil.timestamp_to_date(item["create_time"])

        vo_list = [TypeAdapter(schema.AuthDeptListVo).validate_python(item) for item in lists]
        return ArrayUtil.list_to_tree([i.__dict__ for i in vo_list], "id", "pid", "children")

    @classmethod
    async def detail(cls, id_: int) -> schema.AuthDeptDetailVo:
        """
        部门详情。

        Args:
            id_ (int): 部门ID。

        Returns:
            schema.AuthDeptDetailVo: 部门详情Vo。

        Author:
            zero
        """
        menu = await AuthDeptModel.get(id=id_)
        return TypeAdapter(schema.AuthDeptDetailVo).validate_python(menu.__dict__)

    @classmethod
    async def add(cls, post: schema.AuthDeptAddIn):
        """
        部门新增。

        Args:
            post (schema.AuthDeptAddIn): 部门新增参数。

        Author:
            zero
        """
        # 验证唯一
        if post.pid == 0:
            _top_dept = await AuthDeptModel.filter(is_delete=0).first().values("id")
            if _top_dept:
                raise AppException("只允许存在一个顶级部门")

        # 验证父级
        if post.pid > 0:
            _parent_dept = await AuthDeptModel.filter(id=post.pid, is_delete=0).first().values("id")
            if not _parent_dept:
                raise AppException("父级部门已不存在")

        # 创建部门
        dept = await AuthDeptModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        # 更新关系
        if post.pid == 1:
            relation_str = "0," + str(dept.id)
            await AuthDeptModel.filter(id=dept.id).update(level=1, relation=relation_str)
        else:
            parent_dept = await AuthDeptModel.filter(id=post.pid, is_delete=0).first()
            await AuthDeptModel.filter(id=dept.id).update(
                level=parent_dept.level + 1,
                relation=parent_dept.relation + "," + str(dept.id)
            )

    @classmethod
    async def edit(cls, post: schema.AuthDeptEditIn):
        """
        部门编辑。

        Args:
            post (schema.AuthDeptEditIn): 部门编辑参数。

        Author:
            zero
        """
        # 验证数据
        exist_dept = await AuthDeptModel.filter(id=post.id, is_delete=0).first().values("id")
        if not exist_dept:
            raise AppException("部门数据不存在")

        # 验证父级
        if post.id > 1:
            _parent_dept = await AuthDeptModel.filter(id=post.pid, is_delete=0).first().values("id")
            if not _parent_dept:
                raise AppException("父级部门已不存在了")

            if post.id == post.pid:
                raise AppException("父级部门不能是自己")

        params = post.dict()
        del params["id"]

        # 更新部门
        await AuthDeptModel.filter(id=post.id).update(
            **params,
            update_time=int(time.time())
        )

        # 当前部门
        dept = await AuthDeptModel.filter(id=post.id, is_delete=0).first()

        # 父级部门
        parent_dept = await AuthDeptModel.filter(id=post.pid, is_delete=0).first()

        # 处理关系
        if parent_dept:
            relation = dept.relation
            if post.id == 0:
                replace_level = dept.level - 1
                replace_paths = "0," + str(dept.id)
            else:
                replace_level = dept.level - (parent_dept.level + 1)
                replace_paths = parent_dept.relation + "," + str(dept.id)

            # 更新关系
            update_sql = AuthDeptModel.filter() \
                .update(
                    level=RawSQL(f"`level` - {replace_level}"),
                    relation=RawSQL(f"REPLACE(`relation`, '{relation}', '{replace_paths}')")
                ).sql() + f" WHERE FIND_IN_SET({dept.id}, `relation`)"

            await AuthDeptModel.raw(update_sql)

    @classmethod
    async def delete(cls, id_: int):
        """
        部门删除。

        Args:
            id_ (int): 部门ID。

        Author:
            zero
        """
        exist_dept = await AuthDeptModel.filter(id=id_, is_delete=0).first().values("id")
        if not exist_dept:
            raise AppException("部门数据不存在")

        child_dept = await AuthDeptModel.filter(pid=id_, is_delete=0).first().values("id")
        if child_dept:
            raise AppException("请先删除子部门")

        admin = await AuthAdminModel.filter(dept_id=id_, is_delete=0).first().values("id")
        if admin:
            raise AppException("部门已被使用不能删除")

        await AuthDeptModel.filter(id=id_).update(
            is_delete=1,
            delete_time=int(time.time())
        )
