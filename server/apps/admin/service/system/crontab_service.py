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
import importlib
from events import scheduler
from typing import List, Dict
from pydantic import TypeAdapter
from tortoise.models import in_transaction
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from exception import AppException
from common.utils.valid import ValidUtils
from common.models.sys import SysCrontabModel
from apps.admin.schemas.system import crontab_schema as schema


class CrontabService:
    """ 定时任务服务类 """

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
            schema=schema.CrontabListVo,
            datetime_field=["last_time"],
            fields=SysCrontabModel.without_field("is_delete,delete_time")
        )

        for item in _pager.lists:
            item.params = item.params if item.params else "{ }"
            item.error = item.error if item.error else "-"
            item.remarks = item.remarks if item.remarks else "-"
            item.last_time = item.last_time if item.last_time else "-"

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
        data = await SysCrontabModel.filter(id=id_, is_delete=0).get()
        tasks = []
        for i in range(50):
            _id = data.command + "." + str(i+1)
            task = scheduler.get_job(job_id=_id)
            if not task:
                break
            next_run_time = task.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
            tasks.append({"id": _id, "next_run_time": next_run_time})

        result = data.__dict__
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
        params = post.dict()
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
                crontab = await SysCrontabModel.create(
                    **params,
                    create_time=int(time.time()),
                    update_time=int(time.time())
                )
                # 加入到任务中
                params: Dict[str, any] = json.loads(crontab.params) if crontab.params else {}
                func, trigger_fun = cls.__cron_trigger(crontab.trigger, crontab.command, crontab.rules)
                for i in range(crontab.concurrent):
                    job = crontab.command + "." + str(crontab.concurrent + i)
                    params["w_id"] = crontab.id
                    params["w_ix"] = crontab.concurrent + i
                    params["w_job"] = job
                    scheduler.add_job(func, trigger_fun, name=crontab.name, id=job, kwargs=params)
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
        cls.__check_module(cron.command)

        # 处理数据格式
        params = post.dict()
        params["rules"] = json.dumps(post.rules)
        del params["id"]
        if params.get("params"):
            try:
                json.loads(params.get("params"))
            except Exception as e:
                raise AppException(f"附带参数格式异常: {e}")

        try:
            async with in_transaction("mysql"):
                # 更新到数据库
                await SysCrontabModel.filter(id=post.id).update(
                    **params,
                    update_time=int(time.time())
                )
                # 更新任务信息
                crontab = await SysCrontabModel.filter(id=post.id).first()
                cls.__update_job(crontab, cron.command, cron.concurrent)
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
                for i in range(cron.concurrent):
                    job = cron.command + "." + str(cron.concurrent + 1 + i)
                    scheduler.remove_job(job_id=job)
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
                await SysCrontabModel.filter(id=id_).update(status=2, update_time=int(time.time()))
                # 从任务中暂停
                for i in range(cron.concurrent):
                    job = cron.command + "." + str(cron.concurrent + 1 + i)
                    scheduler.pause_job(job_id=job)
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
                await SysCrontabModel.filter(id=id_).update(status=1, update_time=int(time.time()))
                # 从任务中恢复
                for i in range(cron.concurrent):
                    job = cron.command + "." + str(cron.concurrent + 1 + i)
                    scheduler.resume_job(job_id=job)
        except Exception as e:
            raise AppException(str(e))

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
        except ModuleNotFoundError:
            raise AppException("定时任务模块不存在: " + command)

        func = getattr(module, "execute", None)
        if not func:
            raise AppException("任务执行方法不存在: " + command)

        return func

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
        trigger_fun: any = None
        if trigger == "interval":
            trigger_fun = IntervalTrigger(**condition)
        elif trigger == "cron":
            trigger_fun = CronTrigger(**condition)
        elif trigger == "date":
            trigger_fun = DateTrigger(**condition)

        return [func, trigger_fun]

    @classmethod
    def __update_job(cls, crontab: SysCrontabModel, old_command: str, old_concurrent: int):
        """
        根据最新的规则重载任务配置。
        但最新数据与旧数据不一致时采取更新添加等操作。

        Args:
           crontab (SysCrontabModel): 任务实体对象。
           old_command (str): 旧的包路径。
           old_concurrent (int): 旧的并发数。

        Author:
            zero
        """
        # 获取任务参数
        params: Dict[str, any] = json.loads(crontab.params) if crontab.params else {}

        # 获取触发条件
        func, trigger_fun = cls.__cron_trigger(crontab.trigger, crontab.command, crontab.rules)

        # 指令被改变了
        change: bool = False
        if crontab.command != old_command:
            change = True
            for i in range(old_concurrent):
                job = old_command + "." + str(crontab.concurrent + 1 + i)
                scheduler.remove_job(job_id=job)

        # 删除超出并发
        if crontab.concurrent < old_concurrent and not change:
            beyond: int = old_concurrent - crontab.concurrent
            for i in range(beyond):
                job = crontab.command + "." + str(crontab.concurrent + 1 + i)
                scheduler.remove_job(job_id=job)

        # 增加执行并发
        if crontab.concurrent > old_concurrent and not change:
            for i in range(crontab.concurrent + 10):
                job = crontab.command + "." + str(i + 1)
                task = scheduler.get_job(job_id=job)
                if not task:
                    break
                scheduler.reschedule_job(job_id=job, trigger=trigger_fun)

            beyond: int = crontab.concurrent - old_concurrent
            for i in range(beyond):
                job = crontab.command + "." + str(beyond + i)
                params["w_id"] = crontab.id
                params["w_ix"] = beyond + i
                params["w_job"] = job
                scheduler.add_job(func, trigger_fun, id=job, name=crontab.name, kwargs=params)

        # 更新执行规则
        if not change:
            for i in range(crontab.concurrent):
                job = crontab.command + "." + str(i + 1)
                params["w_id"] = crontab.id
                params["w_ix"] = i + 1
                params["w_job"] = job
                scheduler.modify_job(job_id=job, trigger=trigger_fun, kwargs=params)

        # 载入新的执行
        if change:
            for i in range(crontab.concurrent):
                job = crontab.command + "." + str(crontab.concurrent + i)
                params["w_id"] = crontab.id
                params["w_ix"] = crontab.concurrent + i
                params["w_job"] = job
                scheduler.add_job(func, trigger_fun, id=job, name=crontab.name, kwargs=params)
