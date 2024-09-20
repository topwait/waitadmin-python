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


class TimeUtil:
    """ 时间工具 """

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
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return [
            int(time.mktime(time.strptime(str(today), "%Y-%m-%d"))),
            int(time.mktime(time.strptime(str(tomorrow), "%Y-%m-%d"))) - 1
        ]

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
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        return [
            int(time.mktime(time.strptime(str(yesterday), "%Y-%m-%d"))),
            int(time.mktime(time.strptime(str(today), "%Y-%m-%d"))) - 1
        ]

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
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        acquire = today + datetime.timedelta(days=2)
        return [
            int(time.mktime(time.strptime(str(tomorrow), "%Y-%m-%d"))),
            int(time.mktime(time.strptime(str(acquire), "%Y-%m-%d"))) - 1
        ]

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
        today = datetime.datetime.today()
        monday_date = today - datetime.timedelta(today.isoweekday() - 1)
        t = monday_date.strftime("%Y-%m-%d")
        return [
            int(time.mktime(time.strptime(t, "%Y-%m-%d"))),
            int(time.mktime(time.strptime(t, "%Y-%m-%d"))) + 604800 - 1
        ]

    @classmethod
    def last_week(cls) -> List:
        """
        返回上周开始和结束的时间戳列表。
        开始时间戳为上周周一开始的时间戳，结束时间戳为上周周日的23:59:59的时间戳。

        Returns:
            List[int]: 包含两个元素的列表,第一个元素为上周开始时间戳,第二个元素为上周结束时间戳。

        Author:
            zero
        """
        today = datetime.datetime.today()
        last_monday_date = today - datetime.timedelta(days=today.weekday() + 7)
        ta = last_monday_date.strftime("%Y-%m-%d")
        return [
            int(time.mktime(time.strptime(ta, "%Y-%m-%d"))),
            int(time.mktime(time.strptime(ta, "%Y-%m-%d"))) + 604800 - 1
        ]

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
        now = datetime.datetime.now()
        first_day_of_month = datetime.datetime(now.year, now.month, 1)
        last_day_of_month = datetime.datetime(now.year, now.month, 28) + datetime.timedelta(days=4)
        last_day_of_month = last_day_of_month.replace(day=1) - datetime.timedelta(days=1)
        return [
            int(first_day_of_month.timestamp()),
            int(last_day_of_month.timestamp())
        ]

    @classmethod
    def last_month(cls) -> List[int]:
        """
        返回上个月第一天和最后一天的时间戳(均为午夜00:00和23:59:59的时间戳)。

        Returns:
            list: 包含两个元素的列表,分别表示上个月第一天和最后一天的时间戳。

        Author:
            zero
        """
        # 获取当前日期
        today = datetime.date.today()

        # 获取上月的第一天
        first_day_of_last_month = (today.replace(day=1) - datetime.timedelta(days=today.day)).replace(day=1)

        # 获取上个月的天数
        last_day_of_last_month = first_day_of_last_month + datetime.timedelta(
            days=calendar.monthrange(today.year, first_day_of_last_month.month)[1] - 1)

        # 将日期转换为datetime对象(默认为午夜00:00)
        datetime_first_day = datetime.datetime.combine(first_day_of_last_month, datetime.time())
        datetime_last_day = datetime.datetime.combine(last_day_of_last_month,
                                                      datetime.time(23, 59, 59))

        return [
            int(datetime_first_day.timestamp()),
            int(datetime_last_day.timestamp())
        ]

    @classmethod
    def year(cls) -> List[int]:
        """
        返回今年开始和结束的时间戳。

        Returns:
            List[int]: 包含今年开始和结束时间戳的列表。

        Author:
            zero
        """
        today = datetime.datetime.today()
        return [
            int(datetime.datetime(today.year, 1, 1).timestamp()),
            int(datetime.datetime(today.year, 12, 31, 23, 59, 59).timestamp())
        ]

    @classmethod
    def last_year(cls) -> List[int]:
        """
        返回去年开始和结束的时间戳。

        Returns:
            List[int]: 包含去年开始和结束时间戳的列表。

        Author:
            zero
        """
        today = datetime.datetime.today()
        return [
            int(datetime.datetime(today.year - 1, 1, 1).timestamp()),
            int((datetime.datetime(today.year, 1, 1, 23, 59, 59) - datetime.timedelta(days=1)).timestamp())
        ]

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
        end = int(time.time())
        if now:
            end = cls.yesterday()[1]
        return [
            int((datetime.datetime.now() - datetime.timedelta(days=day)).timestamp()),
            int(end)
        ]

    @classmethod
    def days_ago(cls, day=1) -> int:
        """
        返回指定天数前的时间戳(以秒为单位)。

        Args:
            day (int, optional): 天数,默认为1。

        Returns:
            int: 指定天数前的时间戳(以秒为单位)。

        Author:
            zero
        """
        now = int(time.time())
        return now - cls.days_to_second(int(day))

    @classmethod
    def days_after(cls, day=1) -> int:
        """
        返回指定天数后的时间戳(以秒为单位)。

        Args:
            day (int, optional): 天数,默认为1。

        Returns:
            int: 指定天数后的时间戳（以秒为单位）。

        Author:
            zero
        """
        now = int(time.time())
        return now + cls.days_to_second(int(day))

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
        time_array = time.localtime(t)
        return time.strftime(formats, time_array)

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
        time_array = time.strptime(d, formats)
        return int(time.mktime(time_array))

    @classmethod
    def near_to_date(cls, day: int = 7, formats: str = "%Y-%m-%d"):
        """
        最近N天的日期列表。

        Args:
            day (int): N天前。
            formats (str, optional): 日期时间格式字符串,默认为"%Y-%m-%d"。

        Returns:
            List[str]: 最近N天的日期列表。

        Author:
            zero
        """
        now = datetime.datetime.now()
        start_dates = []
        for i in range(day, 0, -1):
            start_of_day = (now - datetime.timedelta(days=i-1)).replace(hour=0, minute=0, second=0, microsecond=0)
            formatted_date = start_of_day.strftime(formats)
            start_dates.append(formatted_date)
        return start_dates
