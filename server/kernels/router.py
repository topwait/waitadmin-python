# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin_fastapi
# | github:  https://github.com/topwait/waitadmin_fastapi
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
import os
import re
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

        self.router_filters: Dict[str, Dict[str, List[str]]] = {}
        self.router_interceptor: Dict[str, any] = {}

        self.single_app_flag: bool = os.path.exists(os.path.join(self.apps_path, self.controller))

    def load_reg_api(self):
        """ Load and register routes """
        for module_name in self.__get_controller():
            module = importlib.import_module(module_name)
            if "router" in module.__dict__:
                # Extracting information from the request path
                pathinfo = module_name.split(".")
                app_name = pathinfo[1]
                url_prefix = "/" + "/".join(pathinfo[3:-1]) if pathinfo[3:-1] else ""
                contr_name = re.sub(r"Controller$", "", pathinfo[-1])
                contr_name = contr_name[0].lower() + contr_name[1:]

                # Obtain routing related configuration parameters
                setting = self.__get_config()

                # Get if there is a routing interceptor present
                self.__router_interceptor(app_name)
                _lz_url = self.router_filters.get(app_name, {})
                _lz_clz = self.router_interceptor.get(app_name, {})

                # Obtain the group note name for the path
                tags = setting.get("ROUTER_REMARK").get(app_name)

                # Determine whether to register application routing
                if not router_register.get(app_name):
                    # Routing alias
                    prefix = setting.get("ROUTER_ALIAS").get(app_name)
                    prefix = "" if prefix == "" else ("/"+prefix if prefix else "/"+app_name)
                    # Routing style
                    if setting.get("ROUTER_STYLES") == "dot" and url_prefix:
                        url_prefix = url_prefix.replace("/", ".")
                        url_prefix = ("/"+url_prefix[1:]) if url_prefix.startswith(".") else url_prefix

                    router_register[app_name] = APIRouter(prefix=prefix)

                # Loop processing path style and interception
                route = module.__dict__["router"]
                for i in range(len(route.routes)):
                    # Routing prefix and style
                    if url_prefix and (setting.get("ROUTER_PREFIX") or setting.get("ROUTER_STYLES") == "dot"):
                        paths = route.routes[i].path.split("/")
                        contr = paths.pop()
                        if not route.prefix and setting.get("ROUTER_PREFIX"):
                            route.prefix = "/" + contr_name
                            paths.append(contr_name)
                        symbol = "." if setting.get("ROUTER_STYLES") == "dot" else "/"
                        route.routes[i].path = symbol.join(paths) + "/" + contr

                    # Filter routing interceptors
                    intercept_obj_depends = []
                    for obs, clz in _lz_clz.items():
                        _routers_perms: str = route.routes[i].path.replace("/", ":").lstrip(":")
                        _filters_url_arr = _lz_url.get(obs, [])
                        if _routers_perms not in _filters_url_arr:
                            intercept_obj_depends.append(clz)

                    # Load routing interceptor
                    if intercept_obj_depends:
                        route.routes[i].dependencies = intercept_obj_depends

                    # Handling of routing packets
                    if setting.get("ROUTER_GROUPS") == "app":
                        route.routes[i].tags = [tags if tags else app_name]
                    else:
                        if route.routes[i].tags:
                            route.routes[i].tags = [f"【{tags}】- {tag}" for tag in route.routes[i].tags]
                        else:
                            route.routes[i].tags = [tags if tags else app_name]

                # Handling of routing packets
                if route.tags:
                    route.tags = [f"【{tags}】- {tag}" for tag in route.tags]
                else:
                    route.tags = [tags if tags else app_name]

                # Inject the processed route
                router_register[app_name].include_router(route, prefix=url_prefix)

        # Release unnecessary parameters that have been exhausted
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
            "ROUTER_STYLES": "line",
            # Routing prefix: [Automatic completion]
            "ROUTER_PREFIX": True
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
            configs["ROUTER_PREFIX"] = obj.get("ROUTER_STYLES") or True
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
        Recursively traverse the specified directory, collect the full names of controller classes, and add them to the data list.

        Args:
            scene (str): The name of the application scene [addons, apps, ...].
            module (str): The name of the current application module [admin, api, ...].
            catalogue (str): The directory path where controller classes are located.
            data (List[str]): The list used to store the collected full names of controller classes.

        Returns:
            None: This method does not return a result directly, but collects information by modifying the passed-in data list.

        Author:
            zero
        """
        for modular in os.listdir(catalogue):
            if not modular.startswith("__"):
                if os.path.isdir(catalogue + os.sep + modular):
                    self.__recursion_controller(scene, module, catalogue + os.sep + modular, data)
                else:
                    app_module_package = ("." + module) if module else ""
                    app_module_package = scene + app_module_package + "." + self.controller + "."
                    controller_class_name = os.path.splitext(modular)[0]

                    sub_package = catalogue.split(app_module_package.replace(".", "/"))
                    sub_package = sub_package[len(sub_package)-1] if len(sub_package) >= 2 else ""
                    if sub_package:
                        controller_class_name = (sub_package + "." + controller_class_name).replace("/", ".")
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
            Exception: If the interceptor"s "obstruction" attribute is not a dictionary or if the interceptor class does not exist.
        """
        if self.router_interceptor.get(app_name) is not None:
            return False

        inter_pack: str = self.app_module + "." + app_name + ".interceptor"
        file_path: str = self.root_path + inter_pack.replace(".", "/") + ".py"
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
