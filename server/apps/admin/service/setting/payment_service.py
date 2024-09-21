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
import json
import time
from typing import List
from apps.admin.schemas.setting import payment_schema as schema
from common.models.dev import DevPayConfigModel
from common.enums.pay import PayEnum
from common.utils.urls import UrlUtil


class PaymentService:
    """ 支付配置服务类 """

    @classmethod
    async def lists(cls) -> List[schema.PaymentListVo]:
        """
        支付渠道列表

        Returns:
            List[schema.PaymentListVo]: 支付渠道列表Vo。

        Author:
            zero
        """
        _lists = await DevPayConfigModel.filter().order_by("-sort", "-id").all()
        _data = []
        for item in _lists:
            _data.append(schema.PaymentListVo(
                id=item.id,
                channel=item.channel,
                shorter=item.shorter,
                logo=await UrlUtil.to_absolute_url(item.logo),
                icon=await UrlUtil.to_absolute_url(item.icon),
                sort=item.sort,
                status=item.status
            ))

        return _data

    @classmethod
    async def detail(cls, id_: int) -> schema.PaymentDetailVo:
        """
        支付配置详情。

        Args:
            id_ (int): 支付配置ID。

        Returns:
            schema.PaymentDetailVo: 支付配置详情Vo。

        Author:
            zero
        """
        detail = await DevPayConfigModel.filter(id=id_).get()
        vo = schema.PaymentDetailVo(
            id=detail.id,
            channel=detail.channel,
            shorter=detail.shorter,
            name=detail.name,
            icon=await UrlUtil.to_absolute_url(detail.icon),
            sort=detail.sort,
            status=detail.status
        )

        params = json.loads(detail.params)
        if detail.channel == PayEnum.WAY_MNP:
            vo.params = {
                "merchant_type": params.get("merchant_type", "ordinary_merchant"),
                "interface_version": params.get("interface_version", "v3"),
                "mch_id": params.get("mch_id", ""),
                "secret_key": params.get("secret_key", ""),
                "apiclient_cert": params.get("apiclient_cert", ""),
                "apiclient_key": params.get("apiclient_key", "")
            }
        elif detail.channel == PayEnum.WAY_ALI:
            vo.params = {
                "mode": params.get("mode", "secret_key"),
                "merchant_type": params.get("merchant_type", "ordinary_merchant"),
                "app_id": params.get("app_id", ""),
                "private_key": params.get("private_key", ""),
                "public_key": params.get("public_key", "")
            }

        return vo

    @classmethod
    async def save(cls, post: schema.PaymentDetailVo):
        """
        支付配置保存。

        Args:
            post (schema.PaymentDetailVo): 支付配置保存参数。

        Author:
            zero
        """
        model = await DevPayConfigModel.filter(id=post.id).get()

        params = "{}"
        if model.channel == PayEnum.WAY_MNP:
            params = json.dumps({
                "merchant_type": "ordinary_merchant",
                "interface_version": "v3",
                "mch_id": post.params.get("mch_id", ""),
                "secret_key": post.params.get("secret_key", ""),
                "apiclient_cert": post.params.get("apiclient_cert", ""),
                "apiclient_key": post.params.get("apiclient_key", "")
            })
        elif model.channel == PayEnum.WAY_ALI:
            params = json.dumps({
                "merchant_type": "ordinary_merchant",
                "app_id": post.params.get("app_id", ""),
                "private_key": post.params.get("private_key", ""),
                "public_key": post.params.get("public_key", "")
            })

        await DevPayConfigModel.filter(id=post.id).update(
            shorter=post.shorter,
            icon=UrlUtil.to_relative_url(post.icon),
            sort=post.sort,
            status=post.status,
            update_time=int(time.time()),
            params=params
        )
