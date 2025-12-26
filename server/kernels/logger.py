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
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, TextIO, cast

_FORMAT_F = "[%(asctime)s][%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s"
_FORMAT_C = "[%(levelname)s]: [%(filename)s:%(lineno)d] [%(thread)d] - %(message)s"
_LEVEL_NUM = {
    "notset": logging.NOTSET,     # 0
    "debug": logging.DEBUG,       # 10
    "info": logging.INFO,         # 20
    "warning": logging.WARNING,   # 30
    "error": logging.ERROR,       # 40
    "critical": logging.CRITICAL  # 50
}

__all__ = ["configure_logger"]


class CompressedFileHandler(logging.FileHandler):
    """
    A custom file handler that automatically compresses log files when they reach a certain size
    and organizes logs into directories by year/month and day.
    """

    def __init__(self, filename: str, mode: str = "a", encoding: Optional[str] = None,
                 delay: bool = False, gzip_size: Optional[Union[int, str]] = None) -> None:
        """
        Initialize the handler with the specified parameters.

        Args:
            filename: Path to the log file
            mode: File opening mode
            encoding: File encoding
            delay: Whether to delay opening the file until the first log record is emitted
            gzip_size: Size threshold in bytes before compressing the log file
        """
        super().__init__(filename, mode, encoding, delay)
        self.gzip_size: int = int(gzip_size) if gzip_size else 1024 * 1024 * 5  # 5MB default
        self.filename: str = filename

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record with directory organization and compression support

        Args:
            record: The log record to emit
        """
        if self.stream is None:
            self.stream = cast(TextIO, self._open())

        if self.stream is not None and self.do_dir():
            self.stream.close()
            self.stream = cast(TextIO, self._open())

        self.do_zip()
        logging.StreamHandler.emit(self, record)

    def do_dir(self) -> bool:
        """
        Reorganize log files into year/month and day-based directory structure.

        Returns:
            bool: True if a new log file was created, False if using existing file
        """
        year: str = datetime.now().strftime("%Y%m")
        days: str = datetime.now().strftime("%d")
        path: str = os.path.dirname(os.path.dirname(self.baseFilename))
        dirs: str = os.path.join(path, year)
        self.baseFilename = os.path.join(dirs, f"{days}.log")

        if not os.path.exists(dirs):
            os.makedirs(dirs, exist_ok=True)

        if not os.path.exists(self.baseFilename):
            return True
        return False

    def do_zip(self) -> None:
        """
        Compress log file if it exceeds the size threshold.
        The original file is emptied after compression.
        """
        try:
            if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) > self.gzip_size:
                # Use safer file manipulation methods
                gz_filename = f"{self.baseFilename}.gz"
                with open(self.baseFilename, "rb") as f_in, gzip.open(gz_filename, "wb") as f_out:
                    f_out.writelines(f_in)
                # Clear the content of the source file
                with open(self.baseFilename, "w") as _:
                    pass
        except (IOError, OSError) as e:
            sys.stderr.write(f"Error compressing log file {self.baseFilename}: {str(e)}\n")


class RelativePathFormatter(logging.Formatter):
    """
    A custom formatter that converts absolute file paths to paths relative to the project root.
    This makes log messages more readable by showing paths relative to the project root.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, converting absolute paths to project-relative paths.

        Args:
            record: The log record to format

        Returns:
            str: The formatted log message
        """
        # 取项目根目录
        project_root = str(Path(__file__).resolve().parent.parent.parent)

        # 计算相对路径
        if hasattr(record, "pathname") and record.pathname:
            try:
                relative_path = os.path.relpath(record.pathname, project_root)
                record.pathname = relative_path
            except ValueError:
                # 处理路径在不同驱动器的情况
                pass

        return super().format(record)


def configure_logger() -> None:
    """
    Configure the application's logging system based on configuration settings.

    This function sets up file and/or console logging handlers with appropriate
    formatters and log levels. It also configures specific module loggers based
    on the rely_levels configuration.

    The logger configuration is loaded from the config module's GlobalSetting class.
    If the configuration is not available, sensible defaults are used.
    """
    config = __loading_logs_configs()
    path: str = config.get("path", "runtime/log")

    # Gzip
    gzip_size_config = config.get("gzip_size")
    gzip_size: int = int(gzip_size_config) if gzip_size_config else 1024 * 1024 * 5
    # Level
    level_file: int = _LEVEL_NUM[config.get("level_file", "debug")]
    level_sole: int = _LEVEL_NUM[config.get("level_sole", "info")]
    # Status
    enable_file: bool = config.get("enable_file", True)
    enable_sole: bool = config.get("enable_sole", True)
    # Format
    format_file: str = config.get("format_file", _FORMAT_F)
    format_sole: str = config.get("format_sole", _FORMAT_C)
    format_date: str = config.get("format_date", "%Y-%m-%d %H:%M:%S %p")
    # RELY
    rely_levels: Dict[str, List[str]] = config.get("rely_levels", {})

    handlers = []
    if enable_file:
        try:
            year: str = datetime.now().strftime("%Y%m")
            days: str = datetime.now().strftime("%d")
            log_dir: str = os.path.join(path, year)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            log_file = os.path.join(log_dir, f"{days}.log")
            file_handler = CompressedFileHandler(filename=log_file, gzip_size=gzip_size)
            file_handler.setFormatter(RelativePathFormatter(format_file, datefmt=format_date))
            file_handler.setLevel(level_file)
            handlers.append(file_handler)
        except (IOError, OSError) as e:
            sys.stderr.write(f"Error setting up file handler: {str(e)}\n")
            enable_sole = True

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


def __loading_logs_configs() -> dict:
    """
    Load Log configuration from config module

    Returns:
        dict: Logger configuration dictionary
    """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            sys.stderr.write("Warning: GlobalSetting class not found in config module\n")
            return configs

        try:
            obj = clz().dict()
            return obj.get("LOGGER", {})
        except Exception as e:
            sys.stderr.write(f"Error loading logger config: {str(e)}\n")
            return configs
    except ModuleNotFoundError:
        sys.stderr.write("Warning: config module not found\n")
        return configs
    except Exception as e:
        sys.stderr.write(f"Unexpected error loading config: {str(e)}\n")
        return configs
