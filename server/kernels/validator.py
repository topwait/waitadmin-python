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
from typing import Dict, List

__all__ = ["CustomValidate"]


class CustomValidate:
    def __init__(self, messages: Dict[str, str], model_fields: Dict[str, object]):
        self.messages: dict = messages
        self.model_fields: dict = model_fields

    def format_error(self, errors: Dict[str, any]) -> List[Dict[str, any]]:
        """
        将错误字典格式化为带有自定义错误描述信息的列表。

        Args:
            errors (Dict[str, any]): 包含错误信息的字典。
                type: str:  示例: string_too_short
                loc: tuple: 示例: ("body", "username")
                msg: str:   示例: "String should have at least 2 characters"
                input: str: 示例: "admin"
                ctx: dict:  示例: {"min_length": 2}

        Returns:
            List[Dict[str, any]]: 包含格式化后错误信息的字典列表。

        Author zero
        """
        loc: tuple = errors.get("loc")
        rules: dict = errors.get("ctx")
        types: str = errors.get("type")
        field: str = loc[1] if len(loc) >= 2 else loc[0]

        # 返回指定错误描述
        key = list(rules.keys())[0] if rules else types
        if self.messages.get(f"{field}.{key}"):
            errors["err"] = self.messages.get(f"{field}.{key}")
            return [errors]

        # 使用描述覆盖字段
        remark = field
        nature = self.model_fields.get(field)
        if nature and nature.json_schema_extra and nature.json_schema_extra.get("label"):
            label = nature.json_schema_extra.get("label")
            if isinstance(label, bool):
                description = self.model_fields.get(field).description
                remark = description if description else field
            else:
                remark = label

        # 使用多语言转换
        error_rule_msg = self.languages().get(key)
        if error_rule_msg:
            error_rule_msg = error_rule_msg.replace(":attribute", remark)
            if rules and rules.get(key) is not None:
                error_rule_msg = error_rule_msg.replace(":rule", str(rules.get(key)))
            errors["err"] = error_rule_msg

        return [errors]

    @staticmethod
    def languages():
        _lang = {
            "en-us": {
                "missing": ":attribute require",
                "pattern": ":attribute should match pattern `:rule`",
                "float_parsing": ":attribute must be a valid number",
                "int_from_float": ":attribute must be a valid integer",
                "int_parsing": ":attribute must be a valid integer",
                "string_type": ":attribute must be a valid string",
                "max_length": ":attribute should have at least :rule characters",
                "min_length": ":attribute should have at most :rule characters",
                "gt": ":attribute must greater than :rule",
                "lt": ":attribute must less than :rule",
                "ge": ":attribute must be greater than or equal to :rule",
                "le": ":attribute must be less than or equal to :rule",
                "multiple_of": ":attribute must be a multiple of :rule",
                "max_digits": ":attribute decimal input should have no more than :rule digits in total",
                "decimal_places": ":attribute decimal input should have no more than :rule decimal places",
                "whole_digits": ":attribute Decimal input should have no more than :rule digit before the decimal point"
            },
            "zh-cn": {
                "missing": ":attribute 字段必填",
                "pattern": ":attribute 不匹配模式规则 `:rule`",
                "float_parsing": ":attribute 必须是有效的数字",
                "int_from_float": ":attribute 必须是有效的整数",
                "int_parsing": ":attribute 必须是有效的整数",
                "string_type": ":attribute 必须是有效的字符串",
                "max_length": ":attribute 不能超过 :rule 个字符",
                "min_length": ":attribute 不能小于 :rule 个字符",
                "gt": ":attribute 必须大于 :rule",
                "lt": ":attribute 必须小于 :rule",
                "ge": ":attribute 必须大于或等于 :rule",
                "le": ":attribute 必须小于或等于 :rule",
                "multiple_of": ":attribute 必须是的 :rule 倍数",
                "max_digits": ":attribute 十进制输入的总位数不能超过 :rule 位",
                "decimal_places": ":attribute 十进制输入的小数位数不能超过 :rule 位",
                "whole_digits": ":attribute 输入的小数点前面的位数不能超过 :rule 位"
            },
            "ja-jp": {

            }
        }
        return _lang.get("zh-cn", _lang.get("en-us"))
