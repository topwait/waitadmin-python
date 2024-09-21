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
import importlib
from typing import List, Dict
from datetime import datetime
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from common.models.sys import SysCrontabModel


scheduler = AsyncIOScheduler()


class AppEvents:
    @classmethod
    async def startup(cls, _app: FastAPI):
        scheduler.add_job(cls._inject_crontab, DateTrigger(run_date=datetime.now()))
        scheduler.start()

    @classmethod
    async def shutdown(cls, _app: FastAPI):
        scheduler.shutdown()

    @classmethod
    async def _inject_crontab(cls):
        crontab_lists = await SysCrontabModel.filter(is_delete=0).order_by("-id").all()
        for crontab in crontab_lists:
            try:
                module = importlib.import_module(crontab.command)
            except ModuleNotFoundError:
                raise Exception(f"The scheduled task module does not exist: {crontab.command}")

            func = getattr(module, "execute", None)
            if not func:
                raise Exception(f"Task execution method does not exist: {crontab.command}")

            # 获取任务参数
            params: Dict[str, any] = json.loads(crontab.params) if crontab.params else {}

            # 获取任务规则
            rules: List[dict] = json.loads(crontab.rules)

            # 处理触发条件
            condition = {}
            for item in rules:
                if crontab.trigger == "interval" and item.get("key") not in ["start_date", "end_date"]:
                    condition[item.get("key")] = int(item.get("value"))
                else:
                    condition[item.get("key")] = item.get("value")

            # 配置触发条件
            _trigger_fun: any = None
            if crontab.trigger == "interval":
                _trigger_fun = IntervalTrigger(**condition)
            elif crontab.trigger == "cron":
                _trigger_fun = CronTrigger(**condition)
            elif crontab.trigger == "date":
                _trigger_fun = DateTrigger(**condition)

            # 加入到任务中
            for i in range(crontab.concurrent):
                job = crontab.command + "." + str(i+1)
                params["w_id"] = crontab.id
                params["w_ix"] = int(i + 1)
                params["w_job"] = job
                scheduler.add_job(func, _trigger_fun, id=job, name=crontab.name, kwargs=params)
