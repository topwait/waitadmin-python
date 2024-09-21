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
import re


class ValidUtils:
    """ 验证工具 """

    @classmethod
    def is_mobile(cls, value):
        """ 是否为手机号 """
        pattern = r"^1[3-9]\d{9}$"
        return re.match(pattern, value)

    @classmethod
    def is_email(cls, value):
        """ 是否为邮箱号 """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, value)

    @classmethod
    def is_alpha(cls, value):
        """ 是否为纯字母 """
        pattern = r"^[A-Za-z]+$"
        return re.match(pattern, value)

    @classmethod
    def is_alpha_num(cls, value):
        """ 是否为字母和数字 """
        pattern = r"^[A-Za-z0-9]+$"
        return re.match(pattern, value)

    @classmethod
    def is_alpha_dash(cls, value):
        """ 是否为字母和数字,下划线_及破折号- """
        pattern = r"^[A-Za-z0-9\-\_]+$"
        return re.match(pattern, value)

    @classmethod
    def is_chs(cls, value):
        """ 是否为汉字 """
        pattern = r"^[\x{4e00}-\x{9fa5}\x{9fa6}-\x{9fef}\x{3400}-\x{4db5}\x{20000}-\x{2ebe0}]+$/u"
        return re.match(pattern, value)

    @classmethod
    def is_chs_alpha(cls, value):
        """ 是否为汉字、字母 """
        pattern = r"^[\x{4e00}-\x{9fa5}\x{9fa6}-\x{9fef}\x{3400}-\x{4db5}\x{20000}-\x{2ebe0}a-zA-Z]+$/u"
        return re.match(pattern, value)

    @classmethod
    def is_chs_alpha_num(cls, value):
        """ 是否为汉字、字母和数字 """
        pattern = r"^[\x{4e00}-\x{9fa5}\x{9fa6}-\x{9fef}\x{3400}-\x{4db5}\x{20000}-\x{2ebe0}a-zA-Z0-9]+$/u"
        return re.match(pattern, value)

    @classmethod
    def is_chs_dash(cls, value):
        """ 是否为汉字、字母、数字和下划线_及破折号- """
        pattern = r"^[\x{4e00}-\x{9fa5}\x{9fa6}-\x{9fef}\x{3400}-\x{4db5}\x{20000}-\x{2ebe0}a-zA-Z0-9\_\-]+$/u"
        return re.match(pattern, value)

    @classmethod
    def is_id_card(cls, value):
        """ 是否为有效的身份证格式 """
        pattern = r"(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)" \
                  r"|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}$)/"
        return re.match(pattern, value)

    @staticmethod
    def is_json(obj: any) -> bool:
        """
        判断给定的字符串是否是有效的JSON对象。

        Args:
            obj (any): 需要被判断的字符串。

        Returns:
            bool: 如果字符串是有效的JSON对象，返回True；否则返回False。

        Author:
            zero
        """
        import json
        try:
            json.loads(obj)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_number(s: any) -> bool:
        """
        判断给定的字符串是否可以转换为数字（整数或浮点数）。

        Args:
            s (any): 需要被判断的字符串。

        Returns:
            bool: 如果字符串可以转换为数字，则返回True；否则返回False。

        Author:
            zero
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_integer(s: any) -> bool:
        try:
            import re
            return bool(re.match(r"^[1-9]\d*$", s))
        except ValueError:
            return False

    @staticmethod
    def is_datetime(date_str: any) -> bool:
        try:
            from datetime import datetime
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
