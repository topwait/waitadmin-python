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
import asyncio
import os
import time
from common.enums.public import CrontabEnum
from common.models.sys import SysCrontabModel
from common.utils.cache import RedisUtil


class GcCron:
    def aa(self):
        pass


async def execute(**kwargs):
    start_time = time.time()
    crontab_id: int = int(kwargs["w_id"])   # 任务ID
    process_pid: int = int(kwargs["w_pid"])   # 任务ID
    task_index: int = int(kwargs["w_ix"]) # 任务编号
    # command_job: str = kwargs["w_job"]    # 任务指令
    # print(kwargs) # 其它附带参数

    lock_key = f"queues:lock_{str(crontab_id)}_{str(task_index)}"
    lock_acquired = await RedisUtil.set(lock_key, str(time.time()), 10)
    if not lock_acquired:
        print("当前任务正在消费: " + str(task_index) + " => 跳过")
        return False

    try:
        await asyncio.sleep(10)
        print("任务来了: " + str(task_index))
    except Exception as e:
        print(str(e))
    finally:
        pass
        # await RedisUtil.delete(str(task_index))

    # if locks.get(process_id)

    #
    # try:
    #     lists = []
    #     for _ in range(10):
    #         v = await RedisUtil.sPop("queues")
    #         if v is None:
    #             break
    #         lists.append(str(v))
    #
    #     if not lists:
    #         return False
    #
    #     await asyncio.sleep(10)
    #     print("任务下标=" + str(process_id) + ": " + ",".join(lists))
    #     # await SysCrontabModel.compute(crontab_id, start_time)
    #     return {"msg": "垃圾清理完成"}
    # except Exception as e:
    #     print(str(e))
    #     # await SysCrontabModel.compute(crontab_id, start_time, status=CrontabEnum.CRON_ERROR, error=str(e))


