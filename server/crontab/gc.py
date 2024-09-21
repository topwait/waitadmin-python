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
from common.models.sys import SysCrontabModel


async def execute(**kwargs):
    start_time = time.time()
    crontab_id: int = int(kwargs["w_id"])  # 任务ID
    # process_id: int = int(kwargs["w_ix"])  # 任务编号
    # command_job: str = kwargs["w_job"]     # 任务指令
    # print(kwargs) #其它附带参数

    await SysCrontabModel.compute(crontab_id, start_time)
    return {"msg": "垃圾清理完成"}
