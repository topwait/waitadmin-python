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
from exception import AppException
from common.utils.urls import UrlUtil
from common.models.article import ArticleModel
from common.models.article import ArticleCategoryModel
from apps.admin.schemas.content import article_schema as schema


class ArticleService:
    """ 文章服务类 """

    @classmethod
    async def lists(cls, params: schema.ArticleSearchIn) -> PagingResult[schema.ArticleListVo]:
        """
        文章列表。

        Args:
            params (schema.ArticleSearchIn): 文章查询参数。

        Returns:
            PagingResult[schema.ArticleListVo]: 文章分页列表Vo。

        Author:
            zero
        """
        where = ArticleModel.build_search({
            "=": ["is_show"],
            "%like%": ["title"],
            "datetime": ["start_time|end_time@create_time"]
        }, params.__dict__)

        _model = ArticleModel.filter(is_delete=0).filter(*where).order_by("-sort", "-id")
        _pager = await ArticleModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            schema=schema.ArticleListVo,
            fields=ArticleModel.without_field("is_delete,delete_time")
        )

        for item in _pager.lists:
            item.image = await UrlUtil.to_absolute_url(item.image)

        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.ArticleDetailVo:
        """
        文章详情。

        Args:
            id_ (int): 文章ID。

        Returns:
            schema.ArticleDetailVo: 文章详情Vo。

        Author:
            zero
        """
        data = await ArticleModel.get(id=id_)
        data.image = await UrlUtil.to_absolute_url(data.image)
        return TypeAdapter(schema.ArticleDetailVo).validate_python(data.__dict__)

    @classmethod
    async def add(cls, post: schema.ArticleAddIn):
        """
        文章新增。

        Args:
            post (schema.ArticleAddIn): 文章新增参数。

        Author:
            zero
        """
        cate = await ArticleCategoryModel.filter(id=post.cid, is_delete=0).first()
        if not cate:
            raise AppException("文章分类不存在")

        await ArticleModel.create(
            **post.dict(),
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.ArticleEditIn):
        """
        文章编辑。

        Args:
            post (schema.ArticleEditIn): 文章编辑参数。

        Author:
            zero
        """
        _article = await ArticleModel.filter(id=post.id, is_delete=0).first().values("id")
        if not _article:
            raise AppException("文章不存在")

        cate = await ArticleCategoryModel.filter(id=post.cid, is_delete=0).first()
        if not cate:
            raise AppException("文章分类不存在")

        params = post.dict()
        del params["id"]

        await ArticleModel.filter(id=post.id).update(
            **params,
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        文章删除。

        Args:
            id_ (int): 文章ID。

        Author:
            zero
        """
        p = await ArticleModel.filter(id=id_, is_delete=0).first().values("id")
        if not p:
            raise AppException("文章不存在")

        await ArticleModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
