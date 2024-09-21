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
from exception import AppException
from common.models.notice import NoticeSetting
from apps.admin.schemas.setting import notice_schema as schema


class NoticeService:
    """ 通知配置服务类 """

    @classmethod
    async def lists(cls) -> List[schema.NoticeListVo]:
        """
        通知配置列表。

        Returns:
            List[schema.NoticeListVo]: 通知配置列表Vo。

        Author:
           zero
        """
        lists = await NoticeSetting.filter().all()\
            .values("id", "scene", "name", "is_captcha", "sys_template", "sms_template", "ems_template")

        data = []
        for item in lists:
            sys = json.loads(item["sys_template"])
            ems = json.loads(item["ems_template"])
            sms = json.loads(item["sms_template"])

            sys_status = sys.get("status") if sys else 2
            ems_status = ems.get("status") if ems else 2
            sms_status = sms.get("status") if sms else 2

            data.append(schema.NoticeListVo(
                id=item["id"],
                scene=item["scene"],
                name=item["name"],
                type="验证码" if item["is_captcha"] else "通知型",
                sys_status=sys_status,
                ems_status=ems_status,
                sms_status=sms_status
            ))

        return data

    @classmethod
    async def detail(cls, id_: int) -> schema.NoticeDetailVo:
        """
        通知配置详情。

        Returns:
            schema.NoticeDetailVo: 配置详情Vo。

        Author:
            zero
        """
        fields = NoticeSetting.without_field("is_delete,create_time,update_time,delete_time")
        detail = await NoticeSetting.filter(id=id_, is_delete=0).first().values(*fields)

        if not detail:
            raise AppException("通知配置不存在")

        return schema.NoticeDetailVo(
            id=detail["id"],
            scene=detail["scene"],
            name=detail["name"],
            type="验证码" if detail["is_captcha"] else "通知型",
            client="用户端" if detail["get_client"] == 1 else "平台端",
            remarks=detail["remarks"],
            variable=json.loads(detail["variable"]) or {},
            sys_template=json.loads(detail["sys_template"]) or {},
            ems_template=json.loads(detail["ems_template"]) or {},
            sms_template=json.loads(detail["sms_template"]) or {}
        )

    @classmethod
    async def save(cls, post: schema.NoticeDetailVo):
        """
        通知配置保存。

         Args:
            post (schema.NoticeDetailVo): 通知配置参数。

        Author:
            zero
        """
        detail = await NoticeSetting.filter(id=post.id, is_delete=0).first().values("id")
        if not detail:
            raise AppException("通知配置不存在")

        update_data = {}
        if post.sys_template:
            update_data["sys_template"] = json.dumps({
                "status": post.sys_template.get("status", 0),
                "content": post.sys_template.get("content", "")
            })

        if post.ems_template:
            update_data["ems_template"] = json.dumps({
                "status": post.ems_template.get("status", 0),
                "content": post.ems_template.get("content", "")
            })

        if post.sms_template:
            update_data["sms_template"] = json.dumps({
                "status": post.sms_template.get("status", 0),
                "content": post.sms_template.get("content", ""),
                "template_code": post.sms_template.get("template_code", "")
            })

        await NoticeSetting.filter(id=post.id).update(
            **update_data,
            update_time=int(time.time())
        )
