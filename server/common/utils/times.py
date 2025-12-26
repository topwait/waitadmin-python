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
import time
import datetime
import calendar
from typing import List
from zoneinfo import ZoneInfo


class TimeUtil:
    """ 时间工具 """

    TIMEZONE = ZoneInfo("Asia/Shanghai")

    @classmethod
    def day_range(cls, date: datetime.date) -> List[int]:
        """
        获取指定日期的开始和结束时间戳

        Args:
            date (datetime.date)

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为今日开始时间戳,第二个元素为今日结束时间戳。

        Author:
            zero
        """
        start = datetime.datetime.combine(date, datetime.time.min, tzinfo=cls.TIMEZONE)
        end = datetime.datetime.combine(date, datetime.time.max, tzinfo=cls.TIMEZONE)
        return [int(start.timestamp()), int(end.timestamp())]

    @classmethod
    def today(cls) -> List[int]:
        """
        返回今日开始和结束的时间戳列表。
        开始时间戳为今日凌晨0点的时间戳,结束时间戳为今日23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为今日开始时间戳,第二个元素为今日结束时间戳。

        Author:
            zero
        """
        return cls.day_range(datetime.date.today())

    @classmethod
    def yesterday(cls) -> List[int]:
        """
        返回昨日开始和结束的时间戳列表。
        开始时间戳为昨日凌晨0点的时间戳,结束时间戳为昨日23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为昨日开始时间戳,第二个元素为昨日结束时间戳。

        Author:
            zero
        """
        return cls.day_range(datetime.date.today() - datetime.timedelta(days=1))

    @classmethod
    def tomorrow(cls) -> List[int]:
        """
        返回明天开始和结束的时间戳列表。
        开始时间戳为明天凌晨0点的时间戳,结束时间戳为明天23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为明天开始时间戳,第二个元素为明天结束时间戳。

        Author:
            zero
        """
        return cls.day_range(datetime.date.today() + datetime.timedelta(days=1))

    @classmethod
    def week(cls) -> List[int]:
        """
        返回本周开始和结束的时间戳列表。
        开始时间戳为本周周一开始的时间戳,结束时间戳为本周周日的23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为本周开始时间戳，第二个元素为本周结束时间戳。

        Author:
            zero
        """
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = monday + datetime.timedelta(days=6)
        monday_start, _ = cls.day_range(monday)
        _, sunday_end = cls.day_range(sunday)
        return [monday_start, sunday_end]

    @classmethod
    def last_week(cls) -> List[int]:
        """
        返回上周开始和结束的时间戳列表。
        开始时间戳为上周周一开始的时间戳，结束时间戳为上周周日的23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为上周开始时间戳,第二个元素为上周结束时间戳。

        Author:
            zero
        """
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday() + 7)
        last_sunday = last_monday + datetime.timedelta(days=6)
        monday_start, _ = cls.day_range(last_monday)
        _, sunday_end = cls.day_range(last_sunday)
        return [monday_start, sunday_end]

    @classmethod
    def month(cls) -> List[int]:
        """
        返回本月开始和结束的Unix时间戳列表。

        Returns:
            List[int]: 包含两个整数的列表,第一个整数表示本月第一天的Unix时间戳,
                        第二个整数表示本月最后一天的Unix时间戳。

        Author:
            zero
        """
        now = datetime.datetime.now(cls.TIMEZONE)
        first_day = datetime.datetime(now.year, now.month, 1, tzinfo=cls.TIMEZONE)
        last_day = datetime.datetime(now.year,
                                     now.month,
                                     calendar.monthrange(now.year, now.month)[1],
                                     tzinfo=cls.TIMEZONE).replace(hour=23, minute=59, second=59)
        return [int(first_day.timestamp()), int(last_day.timestamp())]

    @classmethod
    def last_month(cls) -> List[int]:
        """
        返回上个月第一天和最后一天的时间戳(均为午夜00:00和23:59:59的时间戳)。

        Returns:
            list: 包含两个元素的列表,分别表示上个月第一天和最后一天的时间戳。

        Author:
            zero
        """
        today = datetime.date.today()
        first_day = today.replace(day=1) - datetime.timedelta(days=1)
        first_day = first_day.replace(day=1)
        last_day = first_day.replace(day=calendar.monthrange(first_day.year, first_day.month)[1])
        start, _ = cls.day_range(first_day)
        _, end = cls.day_range(last_day)
        return [start, end]

    @classmethod
    def year(cls) -> List[int]:
        """
        返回今年开始和结束的时间戳。

        Returns:
            List[int]: 包含今年开始和结束时间戳的列表。

        Author:
            zero
        """
        now = datetime.datetime.now(cls.TIMEZONE)
        first_day = datetime.datetime(now.year, 1, 1, tzinfo=cls.TIMEZONE)
        last_day = datetime.datetime(now.year, 12, 31, 23, 59, 59, tzinfo=cls.TIMEZONE)
        return [int(first_day.timestamp()), int(last_day.timestamp())]

    @classmethod
    def last_year(cls) -> List[int]:
        """
        返回去年开始和结束的时间戳。

        Returns:
            List[int]: 包含去年开始和结束时间戳的列表。

        Author:
            zero
        """
        now = datetime.datetime.now(cls.TIMEZONE)
        first_day = datetime.datetime(now.year - 1, 1, 1, tzinfo=cls.TIMEZONE)
        last_day = datetime.datetime(now.year - 1, 12, 31, 23, 59, 59, tzinfo=cls.TIMEZONE)
        return [int(first_day.timestamp()), int(last_day.timestamp())]

    @classmethod
    def day_to_now(cls, day: int = 1, now: bool = True) -> List[int]:
        """
        获取几天前零点到现在/昨日结束的时间戳列表。

        Args:
            day (int, optional): 天数,默认为1。
            now (bool, optional): 是否返回现在的时间戳,默认为True。

        Returns:
            List[int]: 包含几天前零点和现在/昨日结束的时间戳的列表。

        Author:
            zero
        """
        end_time = time.time() if now else cls.yesterday()[1]
        start_time = datetime.datetime.now(cls.TIMEZONE).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - datetime.timedelta(days=day)
        return [int(start_time.timestamp()), int(end_time)]

    @classmethod
    def current_minute_range(cls) -> List[int]:
        """
        获取当前时间分钟的范围时间戳列表

        Returns:
            List[int]: 当前分钟开始时间戳/分钟结束时间戳。
                       如: 2025-12-23 10:20:00 - 2025-12-23 10:20:59

        Author:
            zero
        """
        now = datetime.datetime.now(cls.TIMEZONE)
        start = now.replace(second=0, microsecond=0)
        end = start + datetime.timedelta(minutes=1) - datetime.timedelta(seconds=1)
        return [int(start.timestamp()), int(end.timestamp())]

    @classmethod
    def days_ago(cls, day=1) -> int:
        """
        返回指定天数前的时间戳(以秒为单位)。

        Args:
            day (int, optional): 天数,默认为1。

        Returns:
            int: 指定天数前的时间戳(以秒为单位)。
                 假设当前时间是: 2025-12-22 10:20:00
                 那么就返回: 2025-12-21 10:20:00 的时间戳
                 返回结果为: 1766283600

        Author:
            zero
        """
        return int(time.time()) - cls.days_to_second(day)

    @classmethod
    def days_after(cls, day=1) -> int:
        """
        返回指定天数后的时间戳(以秒为单位)。

        Args:
            day (int, optional): 天数,默认为1。

        Returns:
            int: 指定天数后的时间戳（以秒为单位）。
                 假设当前时间是: 2025-12-22 10:20:00
                 那么就返回: 2025-12-23 10:20:00 的时间戳
                 返回结果为: 1766456400

        Author:
            zero
        """
        return int(time.time()) + cls.days_to_second(day)

    @classmethod
    def days_to_second(cls, day=1) -> int:
        """
        将天数转换为秒数。

        Args:
            day (int, optional): 天数,默认为1。

        Returns:
            int: 转换后的秒数。

        Author:
            zero
        """
        return int(day) * 86400

    @classmethod
    def week_to_second(cls, week=1) -> int:
        """
        将周数转换为秒数。

        Args:
            week (int, optional): 周数,默认为1。

        Returns:
            int: 转换后的秒数。

        Author:
            zero
        """
        return cls.days_to_second() * 7 * int(week)

    @classmethod
    def timestamp_to_date(cls, t: int, formats: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        将时间戳转换为指定格式的日期时间字符串。

        Args:
            t (int): 时间戳,单位为秒。
            formats (str, optional): 日期时间格式字符串,默认为"%Y-%m-%d %H:%M:%S"。

        Returns:
            str: 转换后的日期时间字符串。

        Author:
            zero
        """
        if t is None:
            return None

        dt_utc = datetime.datetime.fromtimestamp(t, tz=ZoneInfo("UTC"))
        dt_shanghai = dt_utc.astimezone(cls.TIMEZONE)
        return dt_shanghai.strftime(formats)

    @classmethod
    def date_to_timestamp(cls, d: str, formats: str = "%Y-%m-%d %H:%M:%S") -> int:
        """
        将日期时间字符串转换为时间戳(整数形式)。

        Args:
            d (str): 日期时间字符串,需符合formats指定的格式。
            formats (str, optional): 日期时间格式字符串,默认为"%Y-%m-%d %H:%M:%S"。

        Returns:
            int: 转换后的时间戳,单位为秒。

        Author:
            zero
        """
        dt_shanghai = datetime.datetime.strptime(d, formats).replace(tzinfo=cls.TIMEZONE)
        return int(dt_shanghai.timestamp())

    @classmethod
    def near_to_date(cls, day: int = 7, formats: str = "%Y-%m-%d"):
        """
        最近N天的日期列表。

        Args:
            day (int): N天前。
            formats (str, optional): 日期时间格式字符串,默认为 "%Y-%m-%d"。

        Returns:
            List[str]: 最近N天的日期列表。

        Author:
            zero
        """
        now = datetime.datetime.now(cls.TIMEZONE)
        return [
            (now - datetime.timedelta(days=i)).strftime(formats)
            for i in range(day, 0, -1)
        ]

    @classmethod
    def compute_remain_time(cls, expire_time: int) -> int:
        """
        计算(当前时间-过期时间)剩余秒数
        这个计算主要考虑到有的月份是31天
        有的是30天的情况,所有不能直接用时间戳去减

        Args:
            expire_time (int): 失效时间(1739340000)

        Returns:
            int

        Author:
            zero
        """
        expire_dt = datetime.datetime.fromtimestamp(expire_time, tz=cls.TIMEZONE)
        now = datetime.datetime.now(cls.TIMEZONE)
        return int((expire_dt - now).total_seconds())

    @classmethod
    def calculate_age(cls, birth_date_str: str, formats: str = "%Y-%m-%d") -> int:
        """
        根据出生日期计算年龄

        Args:
            birth_date_str (str): 出生日期字符串，格式为 'YYYY-MM-DD'
            formats (str）: 日期格式

        Returns:
            当前年龄（整数）

        Author:
            zero
        """
        if not birth_date_str:
            return 0

        birth_date_str = birth_date_str.split(" ")[0]
        try:
            birth_date = datetime.datetime.strptime(birth_date_str, formats).date()
            today = datetime.date.today()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            return max(0, age)
        except ValueError:
            return 0
