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
from common.models.article import ArticleModel
from common.models.article import ArticleCategoryModel
from apps.admin.schemas.content import category_schema as schema


class ArticleCateService:
    """ 文章分类服务类 """

    @classmethod
    async def whole(cls) -> List[schema.ArticleCateWholeVo]:
        """
        所有文章分类。

        Returns:
            List[schema.ArticleCateWholeVo]: 所有文章分类Vo。

        Author:
            zero
        """
        _lists = await ArticleCategoryModel\
            .filter(is_delete=0)\
            .order_by("-sort", "-id")\
            .all()\
            .values("id", "name", "is_disable")

        return [TypeAdapter(schema.ArticleCateWholeVo).validate_python(item) for item in _lists]

    @classmethod
    async def lists(cls, params: schema.ArticleCateSearchIn) -> PagingResult[schema.ArticleCateListVo]:
        """
        文章分类列表。

        Args:
            params (schema.ArticleCateSearchIn): 文章分类查询参数。

        Returns:
            PagingResult[schema.ArticleCateListVo]: 文章分类分页列表Vo。

        Author:
            zero
        """
        where = ArticleCategoryModel.build_search({
            "=": ["is_disable"],
            "%like%": ["name"]
        }, params.__dict__)

        _model = ArticleCategoryModel.filter(is_delete=0).filter(*where).order_by("-sort", "-id")
        _pager = await ArticleCategoryModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            schema=schema.ArticleCateListVo,
            fields=ArticleCategoryModel.without_field("is_delete,delete_time")
        )

        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.ArticleCateDetailVo:
        """
        文章分类详情。

        Args:
            id_ (int): 文章分类ID。

        Returns:
            ArticleCateDetailVo: 文章分类详情Vo。

        Author:
            zero
        """
        data = await ArticleCategoryModel.get(id=id_)
        vo = TypeAdapter(schema.ArticleCateDetailVo).validate_python(data.__dict__)
        return vo

    @classmethod
    async def add(cls, post: schema.ArticleCateAddIn):
        """
        文章分类新增。

        Args:
            post (schema.ArticleCateAddIn): 文章分类新增参数。

        Author:
            zero
        """
        pn = await ArticleCategoryModel.filter(name=post.name, is_delete=0)
        if pn:
            raise AppException("文章分类名称已被占用")

        await ArticleCategoryModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.ArticleCateEditIn):
        """
        文章分类编辑。

        Args:
            post (schema.ArticleCateEditIn): 文章分类编辑参数。

        Author:
            zero
        """
        _post = await ArticleCategoryModel.filter(id=post.id, is_delete=0).first().values("id")
        if not _post:
            raise AppException("文章分类不存在")

        _post3 = await ArticleCategoryModel.filter(name=post.name, id__not=post.id, is_delete=0).values("id")
        if _post3:
            raise AppException("文章分类名称已被占用")

        params = post.dict()
        del params["id"]

        await ArticleCategoryModel.filter(id=post.id).update(
            **params,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        文章分类删除。

        Args:
            id_ (int): 文章分类ID。

        Author:
            zero
        """
        p = await ArticleCategoryModel.filter(id=id_, is_delete=0).first().values("id")
        if not p:
            raise AppException("文章分类不存在")

        admin = await ArticleModel.filter(cid=id_, is_delete=0).first().values("id")
        if admin:
            raise AppException("文章分类已被使用不能删除")

        await ArticleCategoryModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
