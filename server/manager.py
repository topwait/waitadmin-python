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
from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from kernels.database import register_db
from kernels.logger import configure_logger
from kernels.events import configure_event
from kernels.router import configure_router
from kernels.statics import configure_static
from kernels.middleware import configure_middleware
from exception import configure_exception
from config import get_settings


router = APIRouter()


def create_app() -> FastAPI:
    application = FastAPI(
        debug=get_settings().APP_DEBUG,
        version=get_settings().VERSION,
        name=get_settings().PROJECT_NAME,
        description=get_settings().DESCRIPTION,
        docs_url=None
    )

    configure_logger()
    configure_event(application)
    configure_exception(application)
    configure_middleware(application)
    configure_router(application)
    configure_static(application)
    register_db(application)
    application.include_router(router)

    return application


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=get_settings().PROJECT_NAME,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("manager:app",
                host=get_settings().SERVER_HOST,
                port=get_settings().SERVER_PORT,
                workers=get_settings().SERVER_WORKERS,
                reload=get_settings().SERVER_RELOAD)
