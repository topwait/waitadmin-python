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
import random
import string
from io import BytesIO
from pathlib import Path
from base64 import b64encode
from typing import Tuple, Union
from PIL import Image, ImageDraw, ImageFont

path = Path(__file__).parent.joinpath("font")
font_arr = [str(f) for f in path.glob("*.ttf")]

background_color = [(255, 255, 255), (211, 211, 211), (245, 245, 245)]


def color():
    return tuple((random.randint(0, 255) for _ in range(3)))


def get_xy(width, height):
    return [
        random.randint(width / 2, width),
        random.randint(height / 2, height),
        random.randint(0, width),
        random.randint(0, height),
    ]


def captcha(num: int = 4) -> str:
    """
    生成随机验证码
    :param num: 验证码位数
    :return: 文本验证码
    """
    return "".join(
        [random.choice(string.digits + string.ascii_letters) for _ in range(num)]
    )


def img_captcha(
    width: int = 150,
    height: int = 60,
    font_size: int = 39,
    code_num: int = 4,
    byte_stream: bool = False,
) -> Tuple[Union[Image.Image, BytesIO], str]:
    """
    生成图形验证码，返回Image对象 , 验证码文本
    :param width: 验证码长度（x轴） 默认 150
    :param height: 图片宽度（y轴） 默认 40
    :param font_size: 字体大小 默认 18
    :param code_num: 验证码位数 默认 4
    :param byte_stream: byte io 流的形式返回
    :return: (Image, str)
    """
    # 创建图形
    img = Image.new("RGB", (width, height), random.choice(background_color))
    # 画笔
    draw = ImageDraw.Draw(img)
    text = captcha(code_num)
    # 写字
    for i, t in enumerate(text):
        # 字体
        font = ImageFont.truetype(font=random.choice(font_arr), size=font_size)
        draw.text(
            xy=(
                i * width / code_num + random.randint(0, code_num),
                random.randint(i * 2, height // code_num),
            ),
            text=t,
            fill=color(),
            font=font,
        )
        # 干扰
        draw.line(xy=get_xy(width, height), fill=color())
        draw.point(xy=get_xy(width, height), fill=color())
    if byte_stream:
        byte_io = BytesIO()
        img.save(byte_io, "JPEG")
        byte_io.seek(0)
        result = byte_io
    else:
        result = img
    return result, text


def b64_captcha(
    width: int = 150, height: int = 60, font_size: int = 39, code_num: int = 4
) -> Tuple[str, str]:
    img, code = img_captcha(width, height, font_size, code_num, byte_stream=True)
    b64_img = "data:image/jpeg;base64," + b64encode(img.getvalue()).decode(
        encoding="utf-8"
    )
    return b64_img, code


__all__ = ["captcha", "img_captcha", "b64_captcha"]
