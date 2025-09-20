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
from common.core.cron import CronBase


class Command(CronBase):
    """
    垃圾清理器 (代码示例)
    这是一个计划任务的代码格约定模板,在您创建其它计划任务时请遵循该代码格式.
    技术文档:
        https://www.waitadmin.cn/docs/python/server.html
    PS:
        1、必须创建1个类,并且类名必须是 `Command`
        2、定义的类必须继承 `CronBase` 类
        3、必须实现类中的 `run` 方法
    """
    @classmethod
    async def run(cls, **kwargs):
        # 以下是定时任务参数
        # crontab_id: int = int(kwargs["w_id"])    # 定时任务ID
        # cron_index: int = int(kwargs["w_ix"])    # 并发下标ID
        # process_pid: int = int(kwargs["w_pid"])  # 来源进程ID
        # command_job: str = str(kwargs["w_job"])  # 任务的指令

        # 如果你开始多个`并发数量`,实际上是创建了多个一模一样的任务。
        # 并发数大于等于`2`时,请注意任务重复执行问题,虽然我们在基类实现了并发锁机制。

        # 下面是需要执行逻辑
        try:
            # 删除临时图片 ....
            # 删除过期日志 ....
            # 删除系统缓存 ....
            # 模拟延迟任务需要执行3秒
            await asyncio.sleep(3)
        except Exception as e:
            print(str(e))
