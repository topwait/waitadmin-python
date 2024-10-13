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
import time
import inspect
import importlib
import operator
from functools import reduce
from typing import Union, TypeVar, Type, Any, List, Tuple
from pydantic import TypeAdapter
from tortoise.models import Model
from tortoise.queryset import Q
from hypertext import PagingResult

__all__ = ["DbModel"]


class DbModel(Model):
    """ Model base class """
    MODEL = TypeVar("MODEL", bound="Model")

    DB_CONFIGS = {}

    class Meta:
        abstract = True

    @classmethod
    async def paginate(
            cls, model: Type[MODEL],
            page_no: int = 1,
            page_size: int = 15,
            schema: Any = None,
            fields: List = None,
            auto_timestamp: bool = True,
            datetime_field: List = None,
            datetime_format: str = "%Y-%m-%d %H:%M:%S",
    ):
        fields = [] if not fields else fields
        _count = await model.count()
        _lists = await model.limit(page_size).offset((page_no - 1) * page_size).values(*fields)

        for item in _lists:
            if auto_timestamp:
                tf = datetime_field if datetime_field else ["create_time", "update_time", "delete_time"]
                for s in tf:
                    if item.get(s) is not None and not item.get(s):
                        item[s] = ""
                    elif item.get(s):
                        time_array = time.localtime(item.get(s))
                        item[s] = time.strftime(datetime_format, time_array)

        if schema:
            _lists = [TypeAdapter(schema).validate_python(item) for item in _lists]

        return PagingResult.create(_lists, _count, page_no, page_size)

    @classmethod
    def without_field(cls, fields: Union[str, List, Tuple]):
        _fields = []
        _values = fields.split(",") if isinstance(fields, str) else fields
        for field in cls._meta.fields:
            if field not in _values:
                _fields.append(field.strip())
        return _fields

    @classmethod
    def build_search(cls, search: dict, params: dict):
        factor = {
            "=": "",
            ">": "gt",
            "<": "lt",
            ">=": "__gte",
            "<=": "__lte",
            "<>": "__not",
            "%like%": "__contains",
            "%ilike%": "__icontains",
            "like%": "__startswith",
            "ilike%": "__istartswith",
            "%like": "__endswith",
            "%ilike": "__iendswith",
            "isnull": "__isnull",
            "not_isnull": "__not_isnull",
            "iexact": "__iexact",
            "search": "__search",
            "year": "__year",
            "month": "__month",
            "day": "__day",
        }

        where = []
        for whereType, whereFields in search.items():
            for whereField in whereFields:
                w = whereField.split("@")
                key = w[0] if len(w) >= 2 else whereField
                field = w[1] if len(w) >= 2 else whereField

                if factor.get(whereType) or whereType == "=":
                    if params.get(key, None) is None or params.get(key, None) == "":
                        continue
                    suffix = factor.get(whereType)
                    fields = field.split("|")
                    if len(fields) > 1:
                        or_where = []
                        for f in fields:
                            or_where.append(Q(**{(f.strip())+suffix: params.get(key)}))
                        where.append(reduce(operator.or_, or_where))
                    else:
                        where.append(Q(**{field+suffix: params.get(key)}))

                elif whereType == "datetime":
                    d = key.split("|")
                    s_: str = d[0] if len(d) >= 2 else key
                    e_: str = d[1] if len(d) >= 2 else None
                    # StartTime
                    if s_ and params.get(s_):
                        value = params.get(s_)
                        if not is_number(value):
                            formats = "%Y-%m-%d %H:%M:%S" if len(value.split(" ")) >= 2 else "%Y-%m-%d"
                            time_array = time.strptime(value, formats)
                            value = int(time.mktime(time_array))
                        where.append(Q(**{field + "__gte": value}))
                    # EndTime
                    if e_ and params.get(e_):
                        value = params.get(e_)
                        if not is_number(value):
                            formats = "%Y-%m-%d %H:%M:%S" if len(value.split(" ")) >= 2 else "%Y-%m-%d"
                            time_array = time.strptime(value, formats)
                            value = int(time.mktime(time_array))
                        where.append(Q(**{field + "__lte": value}))

        return where

    @classmethod
    def table_prefix(cls, table: str = "", engine: str = None):
        if not cls.DB_CONFIGS:
            cls.DB_CONFIGS = loading_db_configs()
            if not cls.DB_CONFIGS or not cls.DB_CONFIGS.get("connections") or not cls.DB_CONFIGS.get("apps"):
                return table

        apps = cls.DB_CONFIGS.get("apps", {})
        if engine is None:
            if not cls.__module__.startswith("kernels.model"):
                for key in apps.keys():
                    if cls.__module__.startswith(apps[key].get("models")):
                        engine = key
                        break
            if engine is None:
                caller_file_path = inspect.stack()[1].filename
                caller_pack_path = caller_file_path.replace(os.sep + caller_file_path.split(os.sep)[-1], "")
                system_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
                module_apps_path = caller_pack_path.replace(system_root_path, "").replace(os.sep, ".")
                engine = next((key for key in apps.keys() if apps[key].get("models") == module_apps_path), None)

        conn = cls.DB_CONFIGS.get("connections", {}).get(engine, {})
        return conn.get("prefix", "") + table


def is_number(s: any) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def loading_db_configs():
    """ Load Db configuration """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        db_config = obj.get("DATABASES", {})

        return db_config
    except ModuleNotFoundError:
        return configs
