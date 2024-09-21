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
import inspect
from pydantic import ValidationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise.exceptions import DoesNotExist, BaseORMException
from kernels.validator import CustomValidate
from common.enums.errors import ErrorEnum
from hypertext import R


__all__ = ["AppException", "configure_exception"]

logger = logging.getLogger(__name__)


class AppException(Exception):
    """ 自定义操作异常 """
    def __init__(self, msg: str = None, code: int = None, args=None, echo_exc: bool = False, **kwargs):
        super().__init__()
        _args = args if args is not None else []
        _code = code if code is not None else ErrorEnum.FAILED.code
        _message = msg if msg is not None else ErrorEnum.FAILED.msg
        self._code = _code
        self._message = _message
        self.echo_exc = echo_exc
        self.args = _args or []
        self.kwargs = kwargs or {}

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._message

    def __str__(self):
        return "{}: {}".format(self.code, self.msg)


def configure_exception(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """ 处理全局系统异常 """
        logger.error("GlobalException: url=[%s]", request.url.path)
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.SYSTEM_UNKNOWN_ERROR.code,
                msg=ErrorEnum.SYSTEM_UNKNOWN_ERROR.msg
            ).__dict__)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """ 处理客户端请求异常 """
        code: int = ErrorEnum.SYSTEM_UNKNOWN_ERROR.code
        errs: str = exc.detail
        if exc.status_code == 403:
            code = ErrorEnum.TOKEN_EMPTY.code
            errs = ErrorEnum.TOKEN_EMPTY.msg
        elif exc.status_code == 404:
            code = ErrorEnum.REQUEST_404_ERROR.code
            errs = ErrorEnum.REQUEST_404_ERROR.msg
        elif exc.status_code == 405:
            code = ErrorEnum.REQUEST_405_ERROR.code
            errs = ErrorEnum.REQUEST_405_ERROR.msg

        logger.warning("StarletteHTTPException: url=[%s], status_code=[%s]", request.url.path, exc.status_code)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=code,
                msg=errs
            ).__dict__)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 请求参数验证异常 """
        errs = exc.errors()[0]
        messages_arr = {}
        model_fields = {}

        body_field = request.scope.get("route").__dict__["body_field"]
        if body_field:
            __annotation = body_field.field_info.annotation
            model_fields = __annotation.model_fields
            if getattr(__annotation, "messages", None):
                messages_arr = __annotation.messages()
        else:
            view_function = request.__dict__["scope"].get("route").__dict__["endpoint"]
            module = inspect.signature(view_function)
            for name in module.parameters:
                if module.parameters.get(name).annotation.__dict__.get("model_fields"):
                    model_fields = module.parameters.get(name).annotation.model_fields
                    if getattr(module.parameters.get(name).annotation, "messages", None):
                        messages_arr = module.parameters.get(name).annotation.messages()

        error = CustomValidate(messages_arr, model_fields).format_error(errs)
        print(error)

        logger.warning("RequestValidationError: url=[%s], errs=[%s]", request.url.path, error)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.PARAMS_VALID_ERROR.code,
                msg=error[0].get("err", error[0].get("msg"))
            ).__dict__)

    @app.exception_handler(ValidationError)
    async def objects_validation_exception_handler(request: Request, exc: ValidationError):
        """ 实体参数验证异常 (除请求参数验证之外的) """
        errs = exc.errors()[0]
        _err = errs.get("msg")
        _loc = errs.get("loc")[0]

        error = f"entity {_loc} {_err}"
        logger.error("ValidationError: url=[%s]", request.url.path)
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.SYSTEM_UNKNOWN_ERROR.code,
                msg=error
            ).__dict__)

    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request: Request, exc: AssertionError):
        """ 处理断言参数异常 """
        errs = ",".join(exc.args) if exc.args else ErrorEnum.PARAMS_ASSERT_ERROR.msg
        logger.warning("AssertionError: url=[%s], errs=[%s]", request.url.path, errs)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.PARAMS_ASSERT_ERROR.code,
                msg=errs
            ).__dict__)

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """ 处理自定义异常 """
        if exc.echo_exc:
            logger.error("AppException: url=[%s]", request.url.path)
            logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=exc.code,
                msg=exc.msg
            ).__dict__)

    @app.exception_handler(BaseORMException)
    async def db_error_handler(_request: Request, exc: BaseORMException):
        """ 处理数据库操作的异常 """
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.DB_OPERATIONS_ERROR.code,
                msg=str(exc)
            ).__dict__)

    @app.exception_handler(DoesNotExist)
    async def does(_request: Request, _exc: DoesNotExist):
        """ 处理查询数据为空异常 """
        return JSONResponse(
            status_code=200,
            content=R.fail(
                code=ErrorEnum.DB_EMPTY_DATA_ERROR.code,
                msg=ErrorEnum.DB_EMPTY_DATA_ERROR.msg
            ).__dict__)
