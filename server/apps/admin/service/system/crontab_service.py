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
import logging
import os
import sys
import time
import json
import asyncio
import importlib
from typing import List, Dict, Any
from pydantic import TypeAdapter
from tortoise.models import in_transaction
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from events import scheduler
from exception import AppException
from common.enums.public import CrontabEnum
from common.utils.config import ConfigUtil
from common.utils.valid import ValidUtils
from common.utils.cache import RedisUtil
from common.models.sys import SysCrontabModel
from apps.admin.schemas.system import crontab_schema as schema

logger = logging.getLogger(__name__)


class CrontabService:
    """ 定时任务服务类 """

    # REDIS消息订阅KEY
    REDIS_CHANNEL: str = "topical"
    # REDIS计划任务KEY
    REDIS_CRON_TASKS: str = "crontab:jobs_"

    @classmethod
    async def lists(cls, params: schema.CrontabSearchIn) -> List[schema.CrontabListVo]:
        """
        定时任务列表。

        Args:
           params (schema.CrontabSearchIn): 定时任务搜索参数。

        Returns:
            List[schema.CrontabListVo]: 定时任务分页列表Vo。

        Author:
            zero
        """
        _model = SysCrontabModel.filter(is_delete=0).order_by("-id")
        _pager = await SysCrontabModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            datetime_field=["last_time"],
            fields=SysCrontabModel.without_field("is_delete,delete_time")
        )

        interval = {
            "weeks": "间隔{n}周",
            "days": "间隔{n}天",
            "hours": "间隔{n}小时",
            "minutes": "间隔{n}分钟",
            "seconds": "间隔{n}秒",
            "start_date": "开始日期: {n}",
            "end_date": "结束日期: {n}",
        }

        period = {
            "year": "{n}年",
            "month": "{n}月",
            "day": "{n}日",
            "week": "第{n}周",
            "day_of_week": "星期{n}",
            "hour": "{n}时",
            "minute": "{n}分",
            "start_date": "最早触发: {n}",
            "end_date": "最晚触发: {n}",
        }

        lists = []
        for item in _pager.lists:
            condition = []
            rules_lists = json.loads(item["rules"])
            for rule in rules_lists:
                if item["trigger"] == "interval":
                    template = interval[rule["key"]]
                    template = template.replace("{n}", str(rule["value"]))
                    condition.append(template)
                elif item["trigger"] == "cron":
                    template = period[rule["key"]]
                    template = template.replace("{n}", str(rule["value"]))
                    condition.append(template)
                elif item["trigger"] == "date":
                    template = str(rule["value"]) + "(触发)"
                    condition.append(template)

            item["condition"] = condition
            item["params"] = item["params"] or "{ }"
            item["error"] = item["error"] or "-"
            item["remarks"] = item.get("remarks") or "-"
            item["last_time"] = item.get("last_time") or "-"
            vo = TypeAdapter(schema.CrontabListVo).validate_python(item)
            lists.append(vo)

        _pager.lists = lists
        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.CrontabDetailVo:
        """
        定时任务详情。

        Args:
           id_ (int): 任务ID。

        Returns:
           schema.CrontabDetailVo: 定时任务详情Vo。

        Author:
            zero
        """
        # 获取任务信息
        cron = await SysCrontabModel.filter(id=id_, is_delete=0).get()

        # 通知获取进程任务
        await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
            "op": "process",
            "cron_id": cron.id,
            "status": cron.status,
            "command": cron.command,
            "concurrent": cron.concurrent
        }))

        # 从Redis中读取进程
        index: int = 0
        while True:
            await asyncio.sleep(0.01)
            key: str = f"{cls.REDIS_CRON_TASKS}{str(cron.id)}@{cron.command}"
            res: str = await RedisUtil.get(key)
            if res is not None or index >= 10:
                tasks = json.loads(res or "[]")
                await RedisUtil.delete(key)
                break

        # 任计划任务信息
        result = cron.__dict__
        result["rules"] = json.loads(result["rules"])
        result["tasks"] = tasks
        return TypeAdapter(schema.CrontabDetailVo).validate_python(result)

    @classmethod
    async def add(cls, post: schema.CrontabAddIn):
        """
        定时任务新增。

        Args:
           post (schema.CrontabAddIn): 定时任务新增参数。

        Author:
            zero
        """
        # 验证任务数据
        cls.__check_rules(post.trigger, post.rules)
        cls.__check_module(post.command)
        params = post.__dict__
        params["rules"] = json.dumps(post.rules)
        if params.get("id"):
            del params["id"]
        if params.get("params"):
            try:
                json.loads(params.get("params"))
            except Exception as e:
                raise AppException(f"附带参数格式异常: {e}")

        try:
            async with in_transaction("mysql"):
                # 保存到数据库
                cron = await SysCrontabModel.create(
                    **params,
                    create_time=int(time.time()),
                    update_time=int(time.time())
                )
                # 加入到任务中
                if post.status == CrontabEnum.CRON_ING:
                    await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
                        "op": "create",
                        "cron_id": cron.id,
                        "status": post.status,
                        "command": cron.command,
                        "concurrent": cron.concurrent
                    }))
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def edit(cls, post: schema.CrontabEditIn):
        """
        定时任务编辑。

        Args:
           post (schema.CrontabEditIn): 定时任务编辑参数。

        Author:
            zero
        """
        # 查询验证数据
        cron = await SysCrontabModel.filter(id=post.id, is_delete=0).get()
        cls.__check_rules(post.trigger, post.rules)
        cls.__check_module(post.command)

        # 处理数据格式
        params = post.model_dump()
        params["rules"] = json.dumps(post.rules)
        del params["id"]
        if params.get("params"):
            try:
                json.loads(params.get("params"))
            except Exception as e:
                raise AppException(f"附带参数格式异常: {e}")

        try:
            old_command: str = cron.command
            old_concurrent: int = cron.concurrent

            async with in_transaction("mysql"):
                # 更新到数据库
                await SysCrontabModel.filter(id=post.id).update(
                    **params,
                    update_time=int(time.time())
                )

                # 通知更新任务
                await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
                    "op": "update",
                    "cron_id": cron.id,
                    "status": post.status,
                    "command": old_command,
                    "concurrent": old_concurrent
                }))
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def delete(cls, id_: int):
        """
        定时任务删除。

        Args:
           id_ (int): 定时任务ID。

        Author:
            zero
        """
        cron = await SysCrontabModel.filter(id=id_, is_delete=0).get()
        try:
            async with in_transaction("mysql"):
                # 从数据库删除
                await SysCrontabModel.filter(id=id_).update(is_delete=1, delete_time=int(time.time()))
                # 从任务中删除
                await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
                    "op": "delete",
                    "cron_id": cron.id,
                    "status": cron.status,
                    "command": cron.command,
                    "concurrent": cron.concurrent
                }))
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def stop(cls, id_: int):
        """
        定时任务停止。

        Args:
           id_ (int): 定时任务ID。

        Author:
            zero
        """
        cron = await SysCrontabModel.filter(id=id_, is_delete=0).get()
        try:
            async with in_transaction("mysql"):
                # 从数据库暂停
                await SysCrontabModel.filter(id=id_).update(
                    status=CrontabEnum.CRON_STOP,
                    update_time=int(time.time())
                )
                # 从任务中删除
                await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
                    "op": "delete",
                    "cron_id": cron.id,
                    "status": cron.status,
                    "command": cron.command,
                    "concurrent": cron.concurrent
                }))
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def run(cls, id_: int):
        """
        定时任务运行。

        Args:
           id_ (int): 定时任务ID。

        Author:
            zero
        """
        cron = await SysCrontabModel.filter(id=id_, is_delete=0).get()
        cls.__check_module(cron.command)
        try:
            async with in_transaction("mysql"):
                # 从数据库恢复
                await SysCrontabModel.filter(id=id_).update(
                    error="",
                    status=CrontabEnum.CRON_ING,
                    update_time=int(time.time())
                )
                # 从新启动任务
                await RedisUtil.publish(cls.REDIS_CHANNEL, scene="cron", data=json.dumps({
                    "op": "create",
                    "cron_id": cron.id,
                    "status": cron.status,
                    "command": cron.command,
                    "concurrent": cron.concurrent
                }))
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def cron_subscribe(cls, data: str):
        """
        基于Redis的消息订阅处理计划任务
        原因:
            fastapi开启多进程模式后,实际上每个进程都独立运行了一套计划任务(会存在重复消费)。
            为了解决这个问题，我们通过技术手段，在多进程下，保证只有1个进程运行计划任务，其它进程则不运行。
            那么问题就出现了，后台请求接口调整计划任务信息时，调用的进程是随机的，那访问的进程没有运行任务，
            那岂不是会报错吗？所以我们采用Redis的消息订阅模式，让所有进程都监听一个特定的消息，只有运行了
            计划任务的进程去处理该做的事情，没有运行的进程则忽消息。
        订阅监听代码在哪里呢?
            server/events.py 下 startup() -> _redis_subscribe
        """
        try:
            pid = await ConfigUtil.get("sys", "process_id", "0")
            if str(pid) != str(os.getpid()):
                return False

            params = json.loads(data or "{}")
            operate: str = params.get("op", "")
            cron_id: int = int(params.get("cron_id", 0))
            command: str = str(params.get("command", ""))
            concurrent: int = int(params.get("concurrent", 0))

            if operate == "update":
                for i in range(concurrent):
                    job = command + "." + str(1 + i)
                    if scheduler.get_job(job) is not None:
                        scheduler.remove_job(job_id=job)

            if operate in ["create", "update"]:
                crontab = await SysCrontabModel.filter(id=cron_id).first()
                if not crontab or crontab.status != CrontabEnum.CRON_ING:
                    return False
                params: Dict[str, any] = json.loads(crontab.params or "{}") if crontab.params else {}
                func, trigger_fun = cls.__cron_trigger(crontab.trigger, crontab.command, crontab.rules)
                for i in range(crontab.concurrent):
                    job = crontab.command + "." + str(i + 1)
                    params["w_id"] = int(crontab.id)
                    params["w_ix"] = int(i + 1)
                    params["w_pid"] = int(os.getpid())
                    params["w_job"] = job
                    scheduler.add_job(func, trigger_fun, name=crontab.name, id=job, kwargs=params)
            elif operate == "delete":
                for i in range(concurrent):
                    job = command + "." + str(1 + i)
                    if scheduler.get_job(job) is not None:
                        scheduler.remove_job(job_id=job)
            elif operate == "process":
                tasks = []
                for i in range(70):
                    _id = command + "." + str(i + 1)
                    task = scheduler.get_job(job_id=_id)
                    if not task:
                        break
                    next_run_time = task.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                    tasks.append({"id": _id, "next_run_time": next_run_time})

                key: str = f"{cls.REDIS_CRON_TASKS}{str(cron_id)}@{command}"
                val: str = json.dumps(tasks, ensure_ascii=False)
                await RedisUtil.set(key, val, 10)
        except Exception as e:
            logger.error("Error: cron_subscribe " + str(e))

    @classmethod
    def __check_rules(cls, trigger: str, rules: List[Dict[str, any]]):
        """
        检测定时任务规则参数。

        Args:
           trigger (str): 触发的类型。
           rules (List[Dict[str, any]]): 触发的规则。

        Author:
            zero
        """
        interval: List[str] = ["weeks", "days", "hours", "minutes", "seconds", "start_date", "end_date"]
        cron: List[str] = ["year", "month", "day", "day_of_week", "hour", "start_date", "end_date"]
        dates: List[str] = ["run_date"]

        for item in rules:
            key = item.get("key")
            val = item.get("value")
            if not key:
                raise AppException("请填写完善触发类型")

            if not val:
                raise AppException("请填写完善触发规则")

            if key == "interval" and key not in interval:
                raise AppException("不被支持的触发类型: " + key)

            if key == "cron" and key not in cron:
                raise AppException("不被支持的触发类型: " + key)

            if key == "date" and key not in dates:
                raise AppException("不被支持的触发类型: " + key)

            if key in ["start_date", "end_date"] and not ValidUtils.is_datetime(val):
                raise AppException("触发规则要求是日期格式,而您的是: " + val)
            elif trigger == "interval" and not ValidUtils.is_integer(val):
                raise AppException("触发规则的值要求正则数,而您的是: " + val)

    @classmethod
    def __check_module(cls, command: str):
        """
        检测定时任务模块是否存在。

        Args:
           command (str): 模块包的路径。

        Author:
            zero
        """
        try:
            module = importlib.import_module(command)

            clz = getattr(module, "Command", None)
            if not clz:
                raise AttributeError("任务执行的类不存在: " + command)

            fun = getattr(clz, "execute", None)
            if not fun:
                raise AttributeError("任务执行方法不存在: " + command)

            return fun
        except ModuleNotFoundError:
            raise AppException("定时任务模块不存在: " + command)
        except AttributeError as e:
            if command in sys.modules:
                del sys.modules[command]
            raise AppException(str(e))

    @classmethod
    def __cron_trigger(cls, trigger: str, command: str, rules: str):
        """
        根据规则生成对应的触发条件。

        Args:
           trigger (str): 触发类型。
           command (str): 模块包的路径。
           rules (str): 触发的规则。

        Author:
            zero
        """
        # 检验包正确
        func = cls.__check_module(command)

        # 处理触发条件
        condition = {}
        rules: List[dict] = json.loads(rules)
        for item in rules:
            if trigger == "interval" and item.get("key") not in ["start_date", "end_date"]:
                condition[item.get("key")] = int(item.get("value"))
            else:
                condition[item.get("key")] = item.get("value")

        # 配置触发条件
        trigger_fun: Any = None
        if trigger == "interval":
            trigger_fun = IntervalTrigger(**condition)
        elif trigger == "cron":
            trigger_fun = CronTrigger(**condition)
        elif trigger == "date":
            trigger_fun = DateTrigger(**condition)

        return [func, trigger_fun]
