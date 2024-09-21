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
from tortoise.queryset import Q
from hypertext import PagingResult
from exception import AppException
from common.utils.urls import UrlUtil
from apps.admin.schemas import attach_schema as schema
from common.models.attach import AttachModel
from common.models.attach import AttachCateModel


class AttachService:
    """ 附件服务类 """

    @classmethod
    async def album_lists(cls, params: schema.AlbumSearchIn) -> PagingResult[schema.AlbumListVo]:
        """
        附件列表。

        Args:
           params (schema.AlbumSearchIn): 附件搜索参数。

        Returns:
            PagingResult[AlbumListVo]: 附件分页列表Vo。

        Author:
            zero
        """
        where = [Q(is_delete=0), Q(is_attach=1), Q(is_user=0)]
        if params.cid is not None and params.cid >= 0:
            where.append(Q(cid=params.cid))
        if params.type:
            where.append(Q(file_type=params.type))
        if params.keyword:
            where.append(Q(file_name__contains=params.keyword))

        _model = AttachModel.filter(*where).order_by("-id")
        _pager = await AttachModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=["id", "file_type", "file_size", "file_name", "file_path", "file_ext", "create_time", "update_time"],
            datetime_field=["create_time", "update_time"]
        )

        data = []
        for item in _pager.lists:
            data.append(schema.AlbumListVo(
                id=item["id"],
                type=item["file_type"],
                size=item["file_size"],
                name=item["file_name"],
                path=item["file_path"],
                url=await UrlUtil.to_absolute_url(item["file_path"]),
                ext=item["file_ext"],
                create_time=item["create_time"],
                update_time=item["update_time"]
            ))

        _pager.lists = data
        return _pager

    @classmethod
    async def album_move(cls, post: schema.AlbumMoveIn):
        """
        附件移动。

        Args:
           post (schema.AlbumMoveIn): 附件移动参数。

        Author:
            zero
        """
        if post.cid > 0:
            cate = await AttachCateModel.filter(id=post.cid).first().values("id")
            if not cate:
                raise AppException("目标分类不存在")
        else:
            post.cid = 0

        await AttachModel.filter(id__in=post.ids).update(
            cid=post.cid,
            update_time=int(time.time())
        )

    @classmethod
    async def album_rename(cls, post: schema.AlbumRenameIn):
        """
        附件重命名。

        Args:
           post (schema.AlbumRenameIn): 附件重命名参数。

        Author:
            zero
        """
        attach = await AttachModel.filter(id=post.id).first().values("id")
        if not attach:
            raise AppException("当前文件已丢失")

        await AttachModel.filter(id=post.id).update(
            file_name=post.name,
            update_time=int(time.time())
        )

    @classmethod
    async def album_delete(cls, post: schema.AlbumDeleteIn):
        """
        附件删除。

        Args:
           post (schema.AlbumDeleteIn): 附件删除参数。

        Author:
            zero
        """
        await AttachModel.filter(id__in=post.ids).update(
            is_delete=1,
            delete_time=int(time.time())
        )

    @classmethod
    async def cate_lists(cls, params: schema.AlbumCateSearchIn) -> List[schema.AlbumCateListVo]:
        """
        附件分类列表。

        Args:
           params (schema.AlbumCateSearchIn): 搜索参数。

        Returns:
            List[schema.AlbumCateListVo]: 附件分类列表Vo。

        Author:
            zero
        """
        where = [Q(is_delete=0)]
        if params.type:
            where.append(Q(type=params.type))

        lists = await AttachCateModel.filter(*where).order_by("-id").all().values("id", "name")
        return [TypeAdapter(schema.AlbumCateListVo).validate_python(item) for item in lists]

    @classmethod
    async def cate_add(cls, post: schema.AlbumCateCreateIn):
        """
        附件分类创建。

        Args:
           post (schema.AlbumCateCreateIn): 附件分类创建参数。

        Author:
            zero
        """
        await AttachCateModel.create(
            type=post.type,
            name=post.name,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def cate_rename(cls, post: schema.AlbumCateRenameIn):
        """
        附件分类重命名。

        Args:
           post (schema.AlbumCateRenameIn): 附件分类重命名参数。

        Author:
            zero
        """
        cate = await AttachCateModel\
            .filter(id=post.id, type=post.type, is_delete=0)\
            .first().values("id")

        if not cate:
            raise AppException("当前分类已丢失")

        await AttachCateModel.filter(id=post.id).update(
            name=post.name,
            update_time=int(time.time())
        )

    @classmethod
    async def cate_delete(cls, post: schema.AlbumCateDeleteIn):
        """
        附件分类重删除。

        Args:
           post (schema.AlbumCateDeleteIn): 附件分类删除参数。

        Author:
            zero
        """
        cate = await AttachCateModel \
            .filter(id=post.id, type=post.type, is_delete=0) \
            .first().values("id")

        if not cate:
            raise AppException("当前分类不存在")

        await AttachCateModel.filter(id=post.id).update(
            is_delete=1,
            delete_time=int(time.time())
        )
