import time
import asyncio
import logging
import traceback
from abc import abstractmethod, ABC
from common.utils.cache import RedisUtil
from common.enums.public import CrontabEnum
from common.models.sys import SysCrontabModel

logger = logging.getLogger(__name__)


class CronBase(ABC):
    """ 计划任务基类 """
    # 完成更新DB
    FINISH_UPDATE: bool = True
    # 并发锁打印
    UNLOCK_PRINTS: bool = False
    # 并发锁时长(s)
    UNLOCK_DURATION: int = 30

    @classmethod
    async def execute(cls, **kwargs):
        """ Lock execution """
        crontab_id: int = int(kwargs["w_id"])
        cron_index: int = int(kwargs["w_ix"])
        command_job: str = str(kwargs["w_job"])

        lock_key: str = f"crontab:lock_{str(crontab_id)}&{str(cron_index)}"
        if cls.UNLOCK_DURATION > 0:
            lock_val: str = command_job + "@" + str(time.time())
            lock_ack: bool = await RedisUtil.set(lock_key, lock_val, cls.UNLOCK_DURATION, nx=True)
            if not lock_ack:
                if cls.UNLOCK_PRINTS:
                    print(f"[{str(int(time.time()))}] {lock_key}@{command_job}")
                return False

        try:
            await cls.run(**kwargs)
            if cron_index == 1 and cls.FINISH_UPDATE:
                await cls.finish(crontab_id, time.time())
            return True
        except asyncio.CancelledError:
            error_msg: str = f"Task asyncio.CancelledError: {lock_key}"
            logger.error(error_msg)
            await asyncio.shield(cls.error(crontab_id, error_msg))
        except Exception as e:
            logger.error(f"Task failed: {str(e)}\n{traceback.format_exc()}")
            await cls.error(crontab_id, str(e))
        finally:
            if cls.UNLOCK_DURATION > 0:
                try:
                    await RedisUtil.delete(lock_key)
                except Exception as e:
                    logger.error(str(e))

    @classmethod
    async def finish(cls, crontab_id: int, start_time):
        """ finish handling """
        try:
            end_time = time.time()
            exe_time = (end_time - start_time) * 1000
            await SysCrontabModel.filter(id=crontab_id).update(
                exe_time=exe_time,
                last_time=int(end_time)
            )
        except Exception as e:
            logger.error("Crontab finish abnormal " + str(e))

    @classmethod
    async def error(cls, crontab_id: int, error: str):
        """ error handling """
        try:
            await SysCrontabModel.filter(id=crontab_id).update(
                error=error,
                status=CrontabEnum.CRON_ERROR,
                update_time=time.time()
            )
        except Exception as e:
            logger.error("Crontab error abnormal " + str(e))

    @classmethod
    @abstractmethod
    async def run(cls, **kwargs):
        """ Run Task """
        pass
