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
from tortoise.queryset import Q
from pydantic import TypeAdapter
from hypertext import PagingResult
from apps.api.schemas import article_schema as schema
from common.models.article import ArticleCategoryModel
from common.models.article import ArticleCollectModel
from common.models.article import ArticleModel
from common.models.dev import DevBannerModel
from common.enums.public import BannerEnum
from common.utils.times import TimeUtil
from common.utils.urls import UrlUtil


class ArticleService:
    """ 文章服务类 """

    @classmethod
    async def category(cls) -> List[schema.ArticleCategoryVo]:
        """
        文章分类

        Returns:
            List[schema.ArticleCategoryVo]: 文章分类Vo

        Author:
            zero
        """
        _lists = await ArticleCategoryModel \
            .filter(is_disable=0, is_delete=0) \
            .order_by("-sort", "-id") \
            .all() \
            .values("id", "name")

        return [TypeAdapter(schema.ArticleCategoryVo).validate_python(item) for item in _lists]

    @classmethod
    async def lists(cls, params: schema.ArticleSearchIn) -> PagingResult[schema.ArticleListsVo]:
        """
        文章列表

        Args:
            params (schema.ArticleSearchIn): 查询参数

        Returns:
            PagingResult[schema.ArticleListsVo]: 文章分页列表Vo

        Author:
            zero
        """
        order = ["-update_time", "-id"]
        where = ArticleModel.build_search({
            "=": ["cid"],
            "%like%": ["keyword@title"]
        }, params.__dict__)

        _model = ArticleModel.filter(*where).order_by(*order)
        _pager = await ArticleModel.paginate(
            model=_model,
            page_no=params.page,
            page_size=15,
            fields=["id", "cid", "image", "title", "intro", "browse", "create_time", "update_time"]
        )

        _category = {}
        cid_ids = [item["cid"] for item in _pager.lists if item["cid"]]
        if cid_ids:
            category_ = await ArticleCategoryModel.filter(id__in=list(set(cid_ids))).all().values_list("id", "name")
            _category = {k: v for k, v in category_}

        _results = []
        for item in _pager.lists:
            item["category"] = _category.get(item["cid"], "")
            item["image"] = await UrlUtil.to_absolute_url(item["image"])
            vo = TypeAdapter(schema.ArticleListsVo).validate_python(item)
            _results.append(vo)

        _pager.lists = _results
        return _pager

    @classmethod
    async def recommend(cls, type_: str, limit: int = 8) -> List[schema.ArticleListsVo]:
        """
        文章推荐

        Args:
            type_ (str): 查询参数
            limit (int): 限制条数

        Returns:
            PagingResult[schema.ArticleListsVo]: 文章推荐列表Vo

        Author:
            zero
        """
        where = []
        order = ["-sort", "-id"]
        if type_ == "everyday":
            where.append(Q(is_recommend=1))
        elif type_ == "topping":
            where.append(Q(is_topping=1))
        elif type_ == "lately":
            order = ["-update_time", "-id"]
        elif type_ == "ranking":
            order = ["-browse", "-collect", "-id"]

        _lists = await (ArticleModel
                        .filter(*where)
                        .filter(is_show=1, is_delete=0)
                        .order_by(*order)
                        .limit(limit)
                        .all()
                        .values("id", "cid", "title", "image", "intro", "browse", "create_time", "update_time"))

        _category = {}
        cid_ids = [item["cid"] for item in _lists if item["cid"]]
        if cid_ids:
            category_ = await ArticleCategoryModel.filter(id__in=list(set(cid_ids))).all().values_list("id", "name")
            _category = {k: v for k, v in category_}

        _results = []
        for item in _lists:
            item["image"] = await UrlUtil.to_absolute_url(item["image"])
            item["category"] = _category.get(item["cid"], "")
            item["create_time"] = TimeUtil.timestamp_to_date(item["create_time"])
            item["update_time"] = TimeUtil.timestamp_to_date(item["update_time"])
            vo = TypeAdapter(schema.ArticleListsVo).validate_python(item)
            _results.append(vo)

        return _results

    @classmethod
    async def detail(cls, id_: int, user_id: int) -> schema.ArticleDetailVo:
        """
        文章详情

        Args:
            id_ (int): 文章ID
            user_id (int): 用户ID

        Returns:
            PagingResult[schema.ArticleListsVo]: 文章详情Vo

        Author:
            zero
        """
        # 文章详情
        detail = await ArticleModel \
            .filter(id=id_, is_delete=0) \
            .get() \
            .values("id", "cid", "image", "title", "intro", "content", "browse", "create_time", "update_time")

        # 文章类目
        category = await ArticleCategoryModel.filter(id=detail["cid"]).first()
        check_category = category

        # 是否收藏
        collect = await ArticleCollectModel.filter(
            user_id=user_id,
            article_id=detail["id"],
            is_delete=0
        ).first()

        # 更新阅读
        await ArticleModel.filter(id=id_).update(browse=detail["browse"] + 1)

        # 上一条记录
        _prev = await (ArticleModel
                       .filter(id__lt=id_, is_delete=0)
                       .order_by("-sort", "-id")
                       .first()
                       .values("id", "title"))

        # 下一条记录
        _next = await (ArticleModel
                       .filter(id__gt=id_, is_delete=0)
                       .order_by("-sort", "-id")
                       .first()
                       .values("id", "title"))

        detail["category"] = category.name if check_category else ""
        detail["is_collect"] = 1 if collect else 0
        detail["create_time"] = TimeUtil.timestamp_to_date(detail["create_time"])
        detail["update_time"] = TimeUtil.timestamp_to_date(detail["update_time"])
        detail["prev"] = _prev if _prev else {}
        detail["next"] = _next if _next else {}
        return TypeAdapter(schema.ArticleDetailVo).validate_python(detail)

    @classmethod
    async def pages(cls) -> schema.ArticlePagesVo:
        """
        文章页面

        Returns:
            schema.ArticlePagesVo: 文章页面Vo

        Author:
            zero
        """
        adv_lists = await (DevBannerModel
                           .filter(position=BannerEnum.SIDE)
                           .filter(is_disable=0, is_delete=0)
                           .order_by("-sort", "-id")
                           .all().values("title", "image", "target", "url"))

        for adv in adv_lists:
            adv["image"] = await UrlUtil.to_absolute_url(adv["image"])

        return schema.ArticlePagesVo(
            adv=adv_lists,
            topping=await cls.recommend("topping"),
            ranking=await cls.recommend("ranking")
        )

    @classmethod
    async def collect(cls, id_: int, user_id: int):
        """
        文章收藏/取消收藏

        Args:
            id_ (int): 文章ID
            user_id (int): 用户ID

        Author:
            zero
        """
        collect = await ArticleCollectModel.filter(article_id=id_, user_id=user_id).first()
        if not collect:
            await ArticleCollectModel.create(
                user_id=user_id,
                article_id=id_,
                create_time=int(time.time()),
                update_time=int(time.time())
            )
        else:
            await (ArticleCollectModel
                   .filter(id=collect.id)
                   .update(
                        is_delete=0 if collect.is_delete else 1,
                        delete_time=0 if collect.is_delete else int(time.time()),
                        update_time=int(time.time())
                   ))

            article = await ArticleModel.filter(id=id_).first()
            if article:
                article.collect = max(0, (article.collect + 1) if collect.is_delete else (article.collect - 1))
                article.update_time = int(time.time())
                await article.save()
