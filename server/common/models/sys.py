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
from tortoise import fields
from kernels.model import DbModel


class SysConfigModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    type = fields.CharField(null=False, max_length=100, default="", description="类型")
    key = fields.CharField(null=False, max_length=100, default="", description="键名")
    value = fields.TextField(default="", description="键名")
    remarks = fields.CharField(null=False, max_length=100, default="", description="备注")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")

    class Meta:
        table_description = "系统配置表"
        table = DbModel.table_prefix("sys_config")


class SysCrontabModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    name = fields.CharField(null=False, max_length=64, default="", description="任务名称")
    command = fields.CharField(null=False, max_length=200, default="", description="执行命令")
    params = fields.CharField(null=False, max_length=200, default="", description="附带参数")
    trigger = fields.CharField(null=False, max_length=200, default="", description="触发类型")
    rules = fields.TextField(null=False, default="", description="运行规则")
    remarks = fields.CharField(null=False, max_length=300, default="", description="备注信息")
    error = fields.TextField(default="", description="错误提示")
    concurrent = fields.SmallIntField(null=False, default=1, description="并发数量")
    status = fields.SmallIntField(null=False, default=1, description="执行状态: [1=运行, 2=暂停, 3=错误]")
    exe_time = fields.IntField(null=False, default=0, description="执行时长")
    max_time = fields.IntField(null=False, default=0, description="最大执行时长")
    last_time = fields.IntField(null=False, default=0, description="最后执行时间")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "系统任务表"
        table = DbModel.table_prefix("sys_crontab")

    @classmethod
    async def compute(cls, id_: int, start_time: float, status: int = 1, error: str = ""):
        cron: cls = await cls.filter(id=id_).first()
        end_time: int = int(str((time.time() - start_time)).split(".")[0])
        max_time: int = cron.max_time if cron.max_time > end_time else end_time
        await cls.filter(id=id_).update(
            exe_time=end_time,
            max_time=max_time,
            last_time=int(time.time()),
            status=status,
            error=error
        )


class SysLogModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    admin_id = fields.IntField(null=False, default=0, description="操作人员")
    summary = fields.CharField(null=False, max_length=100, default="", description="摘要信息")
    endpoint = fields.CharField(null=False, max_length=300, default="", description="请求函数")
    method = fields.CharField(null=False, max_length=30, default="", description="请求方法: [GET,POST]")
    url = fields.CharField(null=False, max_length=100, default="", description="请求路由")
    ip = fields.CharField(null=False, max_length=100, default="", description="请求IP")
    ua = fields.CharField(null=False, max_length=100, default="", description="请求UA")
    user_agent = fields.CharField(null=False, max_length=900, default="", description="UA详情")
    params = fields.TextField(default="", description="请求参数")
    error = fields.TextField(default="", description="错误信息")
    status = fields.SmallIntField(null=False, default=1, description="执行状态: [1=成功, 2=失败]")
    start_time = fields.CharField(null=False, default="0", max_length=20, description="开始时间: 毫秒")
    end_time = fields.CharField(null=False, default="0", max_length=20, description="结束时间: 毫秒")
    task_time = fields.CharField(null=False, default="0", max_length=20, description="耗时时间: 毫秒")
    create_time = fields.IntField(null=False, default=0, description="操作时间")

    class Meta:
        table_description = "系统日志表"
        table = DbModel.table_prefix("sys_log")
