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
    """
    生成一个随机的RGB颜色值。
    """
    return tuple((random.randint(0, 255) for _ in range(3)))


def get_xy(width, height):
    """
    生成四个随机的x, y坐标值，用于验证码字符的定位。

    Args:
        width (int): 图片的宽度。
        height (int): 图片的高度。

    Returns:
        List[int]: 包含四个整数的列表，分别代表两个字符的随机x, y坐标。
                   列表格式为 [x1, y1, x2, y2]，其中(x1, y1)和(x2, y2)是两个字符的坐标。
    """
    return [
        random.randint(int(width / 2), int(width)),
        random.randint(int(height / 2), int(height)),
        random.randint(0, int(width)),
        random.randint(0, int(height))
    ]


def captcha(num: int = 4) -> str:
    """
    生成随机验证码
    
    Args:
        num (int): 验证码位数。
    
    Returns: 
        (str): 文本验证码
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
    生成图形验证码, 返回Image对象, 验证码文本

    Args:
        width (int): 验证码长度（x轴） 默认 150。
        height (int): 图片宽度（y轴） 默认 40。
        font_size (int): 字体大小 默认 18。
        code_num (int): 验证码位数 默认 4。
        byte_stream (int): byte io 流的形式返回。

    Returns: 
        (Image, str)
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
        width: int = 150,
        height: int = 60,
        font_size: int = 39,
        code_num: int = 4
) -> Tuple[str, str]:
    """
    生成一个指定宽度、高度、字体大小和字符数量的验证码图片，
    并将图片转换为base64编码的字符串格式, 同时返回验证码文本。

    Args:
        width (int): 图片的宽度, 默认为150像素。
        height (int): 图片的高度, 默认为60像素。
        font_size (int): 验证码中字符的字体大小, 默认为39像素。
        code_num (int): 验证码中字符的数量, 默认为4个字符。

    Returns:
        Tuple[str, str]: 一个元组, 第一个元素是base64编码的图片字符串,
                       第二个元素是验证码文本字符串。
    """
    img, code = img_captcha(width, height, font_size, code_num, byte_stream=True)
    b64_img = "data:image/jpeg;base64," + b64encode(img.getvalue()).decode(
        encoding="utf-8"
    )
    return b64_img, code


__all__ = ["captcha", "img_captcha", "b64_captcha"]
