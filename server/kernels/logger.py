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
import gzip
import logging
import importlib
from datetime import datetime
from typing import Dict, List, IO

_LEVEL_NUM = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

__all__ = ["configure_logger"]


class CompressedFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=False, gzip_size=None):
        super().__init__(filename, mode, encoding, delay)
        self.gzip_size: int = int(gzip_size) if gzip_size else 1024 * 1024 * 5
        self.filename: str = filename

    def emit(self, record):
        """ Emit a record """
        if self.stream is None:
            self.stream: IO = self._open()

        if self.stream is not None and self.do_dir():
            self.stream.close()
            self.stream = self._open()

        self.do_zip()
        logging.StreamHandler.emit(self, record)

    def do_dir(self):
        """ Rebuild log directory file """
        year: str = datetime.now().strftime("%Y%m")
        days: str = datetime.now().strftime("%d")
        path: str = "/".join(self.baseFilename.split("/")[:-2])
        dirs: str = f"{path}/{year}"
        self.baseFilename = f"{dirs}/{days}.log"

        if not os.path.exists(dirs):
            os.makedirs(dirs)

        if not os.path.exists(self.baseFilename):
            return True
        return False

    def do_zip(self):
        """ Compress and archive logs """
        if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) > self.gzip_size:
            with open(self.baseFilename, "rb") as f_in, gzip.open(self.baseFilename + ".gz", "wb") as f_out:
                f_out.writelines(f_in)
            open(self.baseFilename, "w").close()


def configure_logger():
    """ Configure Logger """
    config = __loading_logs_configs()
    path: str = config.get("path") or "runtime/log"
    gzip_size: int = int(config.get("gzip_size")) or 1024 * 1024 * 5
    level_file: int = _LEVEL_NUM[config.get("level_file") or "debug"]
    level_sole: int = _LEVEL_NUM[config.get("level_sole") or "info"]
    enable_file: bool = config.get("enable_file") or True
    enable_sole: bool = config.get("enable_sole") or True
    format_file: str = (config.get("format_file")
                        or "[%(asctime)s][%(levelname)s] [%(filename)s:%(lineno)d] [%(thread)d] - %(message)s")
    format_sole: str = (config.get("format_sole")
                        or "[%(levelname)s]: [%(filename)s:%(lineno)d] [%(thread)d] - %(message)s")
    format_date: str = config.get("format_date") or "%Y-%m-%d %H:%M:%S %p"
    rely_levels: Dict[str, List[str]] = config.get("rely_levels") or {}

    handlers = []
    if enable_file:
        year: str = datetime.now().strftime("%Y%m")
        days: str = datetime.now().strftime("%d")
        path: str = f"{path}/{year}"
        if not os.path.exists(path):
            os.makedirs(path)

        file_handler = CompressedFileHandler(filename=f"{path}/{days}.log", gzip_size=gzip_size)
        file_handler.setFormatter(logging.Formatter(format_file))
        file_handler.setLevel(level_file)
        handlers.append(file_handler)

    if enable_sole:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(format_sole))
        console_handler.setLevel(level_sole)
        handlers.append(console_handler)

    logging.basicConfig(
        level=logging.NOTSET,
        format=format_file,
        datefmt=format_date,
        handlers=handlers if handlers else None
    )

    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("tortoise").setLevel(logging.ERROR)
    logging.getLogger("apscheduler").setLevel(logging.ERROR)
    for key, rely in rely_levels.items():
        if _LEVEL_NUM.get(key) is None:
            raise Exception(f"`rely_levels` Unsupported error types [{key}]")

        for module in rely:
            if key == "error" and module in ["asyncio", "tortoise", "apscheduler"]:
                continue
            logging.getLogger(module).setLevel(key)


def __loading_logs_configs():
    """ Load Log configuration """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        return obj.get("LOGGER", {})
    except ModuleNotFoundError:
        return configs
