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
class AttachEnum:
    IMAGE = 10  # 图片
    VIDEO = 20  # 视频
    AUDIO = 30  # 音频
    PACKS = 40  # 包装
    DOCS = 50   # 文档

    @classmethod
    def get_code_by_msg(cls, msg: str) -> int:
        _desc = {
            "image": cls.IMAGE,
            "video": cls.VIDEO,
            "audio": cls.AUDIO,
            "packs": cls.PACKS,
            "docs": cls.DOCS
        }
        return _desc.get(msg, 0)

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        _desc = {
            cls.IMAGE: "image",
            cls.VIDEO: "video",
            cls.AUDIO: "audio",
            cls.PACKS: "packs",
            cls.DOCS: "docs"
        }
        return _desc.get(code, "")
