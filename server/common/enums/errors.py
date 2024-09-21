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
from collections import namedtuple

__all__ = ["ErrorEnum"]

Enums = namedtuple("ErrorEnum", ["code", "msg"])


class ErrorEnum:
    SUCCESS = Enums(0, "OK")
    FAILED = Enums(1, "FAIL")

    TOKEN_EMPTY = Enums(310, "token参数为空")
    TOKEN_VALID = Enums(311, "token参数无效")

    PARAMS_TYPE_ERROR = Enums(320, "参数类型错误")
    PARAMS_VALID_ERROR = Enums(321, "参数校验错误")
    PARAMS_ASSERT_ERROR = Enums(322, "断言参数错误")

    PERMISSIONS_ERROR = Enums(403, "无相关权限")
    REQUEST_404_ERROR = Enums(404, "请求接口丢失")
    REQUEST_405_ERROR = Enums(405, "请求方法错误")

    SYSTEM_UNKNOWN_ERROR = Enums(500, "系统错误")
    SYSTEM_TIMEOUT_ERROR = Enums(504, "请求超时")

    DB_OPERATIONS_ERROR = Enums(600, "数据库操作异常")
    DB_EMPTY_DATA_ERROR = Enums(601, "查询数据不存在")
