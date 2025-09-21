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
import os
import sys
import time
import json
import asyncio
import logging
import importlib
from typing import List, Dict
from datetime import datetime, timedelta
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from common.models.sys import SysCrontabModel
from common.enums.public import CrontabEnum
from common.utils.config import ConfigUtil
from common.utils.cache import RedisUtil
from common.utils.times import TimeUtil


scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)


class AppEvents:
    @classmethod
    async def startup(cls, _app: FastAPI):
        with open("scheduler.pid", "w") as f:
            f.write(str(os.getpid()))

        asyncio.create_task(cls._redis_subscribe())
        run_date = datetime.now() + timedelta(seconds=5)
        scheduler.add_job(cls._init_crontab, DateTrigger(run_date=run_date))
        scheduler.start()

    @classmethod
    async def shutdown(cls, _app: FastAPI):
        scheduler.shutdown()

    @classmethod
    async def _init_crontab(cls):
        """ Initialize scheduled """
        with open("scheduler.pid", "r") as f:
            pid = f.read()
            if pid != str(os.getpid()):
                return False

        await ConfigUtil.set("sys", "process_id", pid)

        tasks = []
        enums = {1: "Success", 2: "Stop", 3: "kError"}
        crontabs = await SysCrontabModel.filter(is_delete=0).order_by("-id").all()
        for crontab in crontabs:
            task = [crontab.id, crontab.name, crontab.command, crontab.concurrent]
            if crontab.status != CrontabEnum.CRON_ING:
                continue

            try:
                module = importlib.import_module(crontab.command)
                clz = getattr(module, "Command", None)
                if not clz:
                    raise AttributeError(f"Cron: '{crontab.command}' has no 'Command' class")
                fun = getattr(clz, "execute", None)
                if not fun:
                    raise AttributeError(f"Cron: '{crontab.command}' has no 'execute' method")
            except ModuleNotFoundError:
                wrong: str = f"Crontab 'module' not found '{crontab.command}'"
                logger.error(wrong)
                crontab.error = wrong
                crontab.status = CrontabEnum.CRON_ERROR
                tasks.append(task + [crontab.status])
                await crontab.save()
                continue
            except AttributeError as e:
                if crontab.command in sys.modules:
                    del sys.modules[crontab.command]
                logger.error(str(e))
                crontab.error = str(e)
                crontab.status = CrontabEnum.CRON_ERROR
                tasks.append(task + [crontab.status])
                await crontab.save()
                continue

            rules: List[dict] = json.loads(crontab.rules or "[]")
            params: Dict[str, any] = json.loads(crontab.params or "{}")

            condition = {}
            for item in rules:
                if crontab.trigger == "interval" and item.get("key") not in ["start_date", "end_date"]:
                    condition[item.get("key")] = int(item.get("value"))
                else:
                    condition[item.get("key")] = item.get("value")

            _trigger_fun = None
            if crontab.trigger == "interval":
                _trigger_fun = IntervalTrigger(**condition)
            elif crontab.trigger == "cron":
                _trigger_fun = CronTrigger(**condition)
            elif crontab.trigger == "date":
                _trigger_fun = DateTrigger(**condition)

            tasks.append(task + [crontab.status])
            for i in range(crontab.concurrent):
                job = crontab.command + "." + str(i + 1)
                params["w_id"] = crontab.id
                params["w_ix"] = int(i + 1)
                params["w_pid"] = int(os.getpid())
                params["w_job"] = job
                scheduler.add_job(fun, _trigger_fun, id=job, name=crontab.name, kwargs=params)

        if os.path.exists("./banner.txt"):
            startup_time = TimeUtil.timestamp_to_date(int(time.time()))
            with open("./banner.txt", "r") as f:
                template = f.read()
                template = template.replace("{{startup_time}}", startup_time)
                template = template.replace("{{process_id}}", str(os.getpid()))
                print(template)

        for job in tasks:
            job[4] = enums[job[4]]
            print(job)

        print("-" * 57)
        return True

    @classmethod
    async def _redis_subscribe(cls):
        """ Redis/Push/Sub"""
        try:
            pubsub = await RedisUtil.subscribe("topical")
            async for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                event = json.loads(str(message["data"] or "{}"))
                scene = event.get("scene")
                if scene == "cron":
                    from apps.admin.service.system.crontab_service import CrontabService
                    await CrontabService.cron_subscribe(str(event["data"]))
        except Exception as e:
            print(str(e))



