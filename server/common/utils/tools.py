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
import hashlib
import string
import random
import time
import uuid
from datetime import datetime
from typing import Optional, Tuple


class ToolsUtil:
    """ 通用工具 """

    @staticmethod
    def make_uuid() -> str:
        """
        生成UUID的十六进制字符串表示。

        Returns:
            str: UUID的十六进制字符串。

        Author:
            zero
        """
        return uuid.uuid4().hex

    @staticmethod
    def make_token(salt: str = "") -> str:
        """
        生成一个唯一的Token字符串。

        Args:
            salt (str): 加密的盐。

        Returns:
            str: 唯一的Token字符串。

        Author:
            zero
        """
        ms = int(time.time() * 1000)
        token = ToolsUtil.make_md5_str(f"{ToolsUtil.make_uuid()}{ms}{ToolsUtil.make_rand_char(8)}")
        token_secret = f"{token}{ToolsUtil.make_rand_char(20)}{salt}"
        return f"{ToolsUtil.make_md5_str(token_secret)}{ToolsUtil.make_rand_char(6)}"

    @staticmethod
    def make_md5_str(val: str, salt: str = "") -> str:
        """
        生成一个给定值和盐的MD5加密字符串。

        Args:
            val (str): 需要加密的字符串。
            salt (str): 用于增加加密复杂度的盐值。默认为空字符串。

        Returns:
            str: 加密后的MD5字符串。

        Author:
            zero
        """
        m = hashlib.md5()
        m.update((val + salt).encode("utf-8"))
        return m.hexdigest()

    @classmethod
    def make_md5_pwd(cls, pwd: str, salt: Optional[str] = None) -> Tuple[str, str] or str:
        """
        生成加密后的密码。

        Args:
            pwd (str): 需要加密的密码。
            salt (str): 用于增加加密复杂度的盐值。

        Returns:
            str or tuple: 加密后的MD5字符串 和 盐。

        Author:
            zero
        """
        _salt: str = ToolsUtil.make_rand_char(6) if salt is None else salt
        password: str = ToolsUtil.make_md5_str(pwd, _salt)
        if salt is None:
            return _salt, password
        return password

    @staticmethod
    def make_rand_char(length: int) -> str:
        """
        生成指定长度的随机字母和数字字符串。

        Args:
            length (int): 字符串的长度。

        Returns:
            str: 随机生成的字符串。

        Author:
            zero
        """
        str_list = random.sample(string.digits + string.ascii_letters, length)
        random_str = "".join(str_list)
        return random_str

    @staticmethod
    def make_rand_digit(length: int) -> str:
        """
        生成指定长度的随机数字字符串。

        Args:
            length (int): 字符串的长度。

        Returns:
            str: 随机生成的数字字符串。

        Author:
            zero
        """
        random_digits = "".join(random.choices(string.digits, k=length))
        return random_digits

    @staticmethod
    async def make_rand_sn(model, field: str, length: int = 10, scene: str = "digits") -> str:
        """
        生成不重复的随机字符串。

        Args:
            model (any): 模型实体。
            field (str): 字段名。
            length (int): 长度。
            scene (str): 场景: [digits, string, char]。

        Returns:
            str: 随机生成的不重复字符串。

        Author:
            zero
        """
        if scene == "digits":    # 纯数字(0~9)
            random_digits = "".join(random.choices(string.digits, k=length))
        elif scene == "string":  # 纯英文字母
            random_digits = "".join(random.choices(string.ascii_letters, k=length))
        elif scene == "char":    # 数字+字母
            str_list = random.sample(string.digits + string.ascii_letters, length)
            random_digits = "".join(str_list)
        else:
            raise Exception("Unsupported random type ToolUtil.make_rend_sn()")

        if model and await model.exists(**{field: random_digits}):
            return await ToolsUtil.make_rand_sn(model, field, length, scene)
        return random_digits

    @staticmethod
    async def make_order_sn(model, field: str, prefix: str = "", rand_suffix_length: int = 6, pool=None) -> str:
        """
        生成不重复的随机订单号。

        Args:
            model (any): 模型实体。
            field (str): 字段名。
            prefix (str): 前缀名称。
            rand_suffix_length (int): 后缀长度。
            pool (str): 随机池。

        Returns:
            str: 随机生成的不重复订单号。

        Author:
            zero
        """
        if pool is None:
            pool = string.digits

        suffix = "".join(random.choice(pool) for _ in range(rand_suffix_length))
        sn = f"{prefix}{datetime.now().strftime('%Y%m%d%H%M%S')}{suffix}"

        if await model.exists(**{field: sn}):
            return await ToolsUtil.make_order_sn(model, field, prefix, rand_suffix_length, pool)

        return sn

    @staticmethod
    def to_user_agent(ua: str) -> str:
        """
        浏览器UA简写。

        Args:
            ua (str): 字段名。

        Returns:
            str: 简写的UA名。

        Author:
            zero
        """
        ua_dict = {
            "chrome": "Chrome",
            "firefox": "Firefox",
            "safari": "Safari",
            "opera": "Opera",
            "edge": "Edge",
            "wechat": "MicroMessenger"
        }

        ua = ua.lower()
        for key, value in ua_dict.items():
            if value in ua:
                return key

        if "msie" in ua or "trident/" in ua:
            return "ie"

        return "other"
