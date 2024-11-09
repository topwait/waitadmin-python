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
import importlib
from typing import List, Dict
from fastapi import APIRouter, FastAPI, Depends

__all__ = ["configure_router"]

router_register = {}


class AutomaticRegRouter:
    def __init__(self):
        self.app_module: str = "apps"
        self.controller: str = "routers"
        self.root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
        self.apps_path: str = os.path.join(self.root_path, self.app_module)

        self.router_filters: Dict[str, any] = {}
        self.router_interceptor: Dict[str, any] = {}

        self.single_app_flag: bool = os.path.exists(os.path.join(self.apps_path, self.controller))

    def load_reg_api(self):
        """ Load and register routes """
        setting = self.__get_config()

        apps = []
        for app in self.__get_apps():
            self.__router_interceptor(app)
            apps.append(app)

        for module_name in self.__get_controller():
            module = importlib.import_module(module_name)
            if "router" not in module.__dict__:
                continue

            # Extracting information from the request path
            pathinfo = module_name.split(".")
            app_name: str = pathinfo[1]
            url_prefix: str = "/" + "/".join(pathinfo[3:-1]) if pathinfo[3:-1] else ""

            # Determine whether to register application routing
            if not router_register.get(app_name):
                prefix = setting.get("ROUTER_ALIAS").get(app_name)  # Set alias
                prefix = "" if prefix == "" else ("/"+prefix if prefix else "/"+app_name)
                router_register[app_name] = APIRouter(prefix=prefix)

            # Inject the processed route
            route = module.__dict__["router"]
            router_register[app_name].include_router(route, prefix=url_prefix)

        for app in apps:
            swagger_tags = setting.get("ROUTER_REMARK").get(app)
            _lz_url = self.router_filters.get(app, {})
            _lz_clz = self.router_interceptor.get(app, {})

            absolute_routers = []
            routes = router_register[app].__dict__.get("routes", [])
            for route in routes:
                # Routing prefix and style
                if route.path and setting.get("ROUTER_STYLES") == "dot":
                    urls = route.path.lstrip("/").split("/")
                    name = urls.pop(0)
                    if len(urls) >= 2:
                        route.path = "/" + name + "/" + ".".join(urls[0:-1]) + "/" + urls[-1]

                # Absolute custom routing
                if "$" in route.path:
                    _abs = route.path[route.path.index("$") + 1:]
                    if _abs:
                        absolute_routers.append(_abs)
                        route.path = _abs

                # Handling of routing packets
                if setting.get("ROUTER_GROUPS") == "app":
                    route.tags = [swagger_tags if swagger_tags else app]
                else:
                    if route.tags:
                        route.tags = [f"【{swagger_tags}】- {tag}" for tag in route.tags]
                    else:
                        route.tags = [swagger_tags if swagger_tags else app]

                # Filter routing interceptors
                intercept_obj_depends = []
                for obs, clz in _lz_clz.items():
                    i = 0 if route.path in absolute_routers else 1
                    urls = route.path.lstrip("/").split("/")
                    path: str = "/".join(urls[i:]).replace(".", "/")
                    _routers_perms: str = path.replace("/", ":").lstrip(":")
                    _filters_url_arr = _lz_url.get(obs, [])
                    if _routers_perms not in _filters_url_arr:
                        intercept_obj_depends.append(clz)

                # Load routing interceptor
                if intercept_obj_depends:
                    route.dependencies = intercept_obj_depends

        self.router_filters = {}
        self.router_interceptor = {}

    @classmethod
    def __get_config(cls):
        """ Obtain routing configuration """
        configs = {
            # Module alias
            "ROUTER_ALIAS": {},
            # Routing remarks
            "ROUTER_REMARK": {},
            # Routing grouping: [app, module]
            "ROUTER_GROUPS": "app",
            # Routing style: [line, dot]
            "ROUTER_STYLES": "line"
        }

        try:
            package = importlib.import_module("config")
            clz = getattr(package, "GlobalSetting", None)
            if not clz:
                return configs

            obj = clz().dict()
            configs["ROUTER_ALIAS"] = obj.get("ROUTER_ALIAS") or {}
            configs["ROUTER_REMARK"] = obj.get("ROUTER_REMARK") or {}
            configs["ROUTER_GROUPS"] = obj.get("ROUTER_GROUPS") or "app"
            configs["ROUTER_STYLES"] = obj.get("ROUTER_STYLES") or "line"
            configs["ROUTER_REPAIR"] = obj.get("ROUTER_REPAIR") or True
            return configs
        except ModuleNotFoundError:
            return configs

    def __get_apps(self):
        """
        Get a list of all application names in the apps_path directory (excluding directories starting with "__")
        and check if a specific controller file exists in each application module directory.

        Returns:
            List[str]: A list containing the names of all applications that meet the conditions.

        Author:
            zero
        """
        apps = []
        for app in os.listdir(self.apps_path):
            file_path = os.path.join(self.apps_path, app)
            if os.path.isdir(file_path) and app.startswith("__") is False:
                controller = os.path.join(self.apps_path, app + os.sep + self.controller)
                if os.path.exists(controller):
                    apps.append(app)

        return apps

    def __get_controller(self):
        """
        Recursively get the paths of controller packages for all application modules.

        Returns:
            List[str]: A list of strings containing the paths to all application controller packages.

        Author:
            zero
        """
        package = []
        if self.single_app_flag:
            catalogue = os.path.join(self.apps_path, self.controller)
            self.__recursion_controller(self.app_module, "", catalogue, package)
        else:
            for module in self.__get_apps():
                catalogue = os.path.join(self.apps_path, module + os.sep + self.controller)
                self.__recursion_controller(self.app_module, module, catalogue, package)

        return package

    def __recursion_controller(self, scene, module, catalogue, data):
        """
        Recursively traverse the directory, collect controller class names, and add them to the data list.

        Args:
            scene (str): The name of the application scene [addons, apps, ...].
            module (str): The name of the current application module [admin, api, ...].
            catalogue (str): The directory path where controller classes are located.
            data (List[str]): The list used to store the collected full names of controller classes.

        Returns:
            None: This method does not directly return the result.

        Author:
            zero
        """
        for modular in os.listdir(catalogue):
            if not modular.startswith("__") and not modular.startswith("."):
                if os.path.isdir(catalogue + os.sep + modular):
                    self.__recursion_controller(scene, module, catalogue + os.sep + modular, data)
                else:
                    app_module_package = ("." + module) if module else ""
                    app_module_package = scene + app_module_package + "." + self.controller + "."
                    controller_class_name = os.path.splitext(modular)[0]
                    sub_package = catalogue.split(app_module_package.replace(".", os.sep))
                    sub_package = sub_package[len(sub_package)-1] if len(sub_package) >= 2 else ""
                    if sub_package:
                        controller_class_name = (sub_package + "." + controller_class_name).replace(os.sep, ".")
                    data.append(app_module_package + controller_class_name)

    def __router_interceptor(self, app_name) -> bool:
        """
        Loads interceptors for the specified application module name and configures them as class attributes.
        These interceptors will be used in subsequent route group injections, based on filtering rules.

        Args:
            app_name (str): The name of the application module (e.g., admin, api).

        Returns:
            bool: Returns True if interceptors were successfully loaded and configured, False otherwise.

        Raises:
            Exception: If the interceptor class does not exist.
        """
        if self.router_interceptor.get(app_name) is not None:
            return False

        inter_pack: str = self.app_module + "." + app_name + ".interceptor"
        file_path: str = self.root_path + inter_pack.replace(".", os.sep) + ".py"
        if not os.path.exists(file_path):
            return False

        module = importlib.import_module(inter_pack)
        obstruction = getattr(module, "obstruction", None)

        if obstruction is None:
            return False

        if not isinstance(obstruction, dict):
            raise Exception("The interceptor [obstruction] attribute must be of List type")

        waylays: Dict[str, any] = {}
        filters: Dict[str, List[str]] = {}
        for key, value in obstruction.items():
            interceptor_class = getattr(module, key, None)
            if interceptor_class is None:
                raise Exception(f"The interceptor `construction` loaded does not exist. error_path: " + file_path)

            if value is None or not isinstance(value, list):
                raise Exception(f"The `construction` attribute type of the interceptor is incorrect, requiring it to "
                                "be: Dict[str, List[str]]. error_path: " + file_path)

            waylays[key] = Depends(interceptor_class.handler)
            filters[key] = value

        self.router_interceptor[app_name] = waylays
        self.router_filters[app_name] = filters
        return True


def configure_router(app: FastAPI):
    """ Configure Router """
    for key in router_register:
        app.include_router(router_register[key])


AutomaticRegRouter().load_reg_api()
