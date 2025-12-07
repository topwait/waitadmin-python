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
import json
from typing import Union, List, Dict, Tuple, Set, Optional, Mapping, Any
from redis import Redis
from kernels.cache import redis_be
from redis.exceptions import DataError
from config import get_settings

__all__ = ["RedisUtil"]


FieldT = Union[int, float, str]


class RedisUtil:
    """ 缓存工具 """

    redis: Redis = redis_be.redis
    prefix: str = get_settings().REDIS.get("prefix", "wait:")

    @classmethod
    def get_key(cls, key: str) -> str:
        return f"{RedisUtil.prefix}{key}"

    @classmethod
    async def expire(cls, key: str, second: int) -> bool:
        """
        设置Redis中指定键的过期时间。

        Args:
            key: Redis键名。
            second: 过期时间(秒)。

        Returns:
             bool: 如果设置成功, 则返回True; 否则返回False。
        """
        return await cls.redis.expire(cls.get_key(key), second)

    @classmethod
    async def persist(cls, key: str) -> bool:
        """
        移除Redis中指定键的过期时间。

        Args:
            key: Redis键名。

        Returns:
             bool: 如果成功移除过期时间, 则返回True; 否则返回False。
        """
        return await cls.redis.persist(cls.get_key(key))

    @classmethod
    async def ttl(cls, key: str) -> int:
        """
        获取Redis中指定键的剩余生存时间。

        Args:
            key (str): Redis中的键名。

        Returns:
            int: 键的剩余生存时间(TTL), 单位为秒。
            如果键不存在,则返回-2。
            如果键存在但没有设置过期时间, 则返回-1。
        """
        return await cls.redis.ttl(cls.get_key(key))

    @classmethod
    async def exists(cls, key: str) -> bool:
        """
        检查Redis中指定键是否存在。

        Args:
            key (str): Redis中的键名。

        Returns:
            bool: 如果键存在, 则返回True; 否则返回False。
        """
        return await cls.redis.exists(cls.get_key(key))

    @classmethod
    async def rename(cls, old_key: str, new_key: str) -> bool:
        """
        在Redis中重命名一个键。

        Args:
            old_key (str): 需要被重命名的旧键名。
            new_key (str): 新键名。

        Returns:
            bool: 如果重命名成功, 则返回True; 否则返回False。

        """
        _old_key = cls.get_key(old_key)
        _new_key = cls.get_key(new_key)
        return await cls.redis.rename(_old_key, _new_key)

    @classmethod
    async def move(cls, key: str, db: int) -> bool:
        """
        在Redis中将一个键从一个数据库移动到另一个数据库。

        Args:
            key (str): 需要被移动的键名。
            db (int): 目标数据库的编号。

        Returns:
            bool: 如果移动成功, 则返回True; 否则返回False。
        """
        return await cls.redis.move(cls.get_key(key), db)

    @classmethod
    async def keys(cls, pattern: str):
        """
        在Redis中查找所有符合给定模式的键。

        Args:
            pattern (str): 用于匹配键的模式字符串。

        Returns:
            List[str]: 包含所有匹配到的键名的列表。
        """
        return await cls.redis.keys(pattern)

    @classmethod
    async def scan_keys(cls, pattern: str, cursor: int = 0, count: int = None) -> Tuple[int, List[str]]:
        """
        在Redis中迭代所有符合给定模式的键。

        Args:
            pattern (str): 用于匹配键的模式字符串。
            cursor (int): 游标,默认为0。
            count (int): 每次迭代返回的键的最大数量。

        Returns:
            Tuple[int, List[str]]: 包含新的游标和当前迭代返回的键名的列表。

        Example:
            async def print_matching_keys(pattern: str):
                cursor = 0
                while True:
                    cursor, keys = await YourClass.scan_keys(pattern, cursor)
                    for key in keys:
                        print(key.decode())  # 如果键是bytes类型,可能需要解码
                    if cursor == 0:
                        break
        """
        patt = cls.get_key(pattern)
        scan_cursor, keys = await cls.redis.scan(cursor=cursor, match=patt, count=count)
        return scan_cursor, keys

    @classmethod
    async def random_key(cls) -> Optional[str]:
        """
        从Redis数据库中随机返回一个键。

        Returns:
            Optional[str]: 如果数据库中有键存在,则返回随机的一个键的字节串;
                           如果数据库为空,则返回None。
        """
        return await cls.redis.randomkey()

    @classmethod
    async def delete(cls, *keys: str) -> int:
        """
        从Redis数据库中删除一个或多个键。

        Args:
            *keys (str): 一个或多个要删除的键名。

        Returns:
            int: 成功删除的键的数量。
        """
        return await cls.redis.delete(*(cls.get_key(key) for key in keys))

    # =============== 【基础指令】  ===============

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """
        从Redis数据库中获取指定键的值。

        Args:
            key (str): 要获取的键名。

        Returns:
            Optional[str]: 如果键存在,则返回该键对应的值。
                           如果键不存在,则返回None。
        """
        return await cls.redis.get(cls.get_key(key))

    @classmethod
    async def get_int(cls, key: str) -> Optional[int]:
        """
        从Redis数据库中获取指定键的值(并转为int)。

        Args:
            key (str): 要获取的键名。

        Returns:
            Optional[int]: 如果键存在,则返回该键对应的值。
                           如果键不存在,则返回None。
        """
        val = await cls.redis.get(cls.get_key(key))
        return int(val) if val else val

    @classmethod
    async def get_array(cls, key: str) -> Union[Dict, List, Tuple, Set, None]:
        """
        从Redis数据库中获取指定键的值(并转为array)。

        Args:
            key (str): 要获取的键名。

        Returns:
            Union[Dict, List, Tuple, Set, None]: 如果键存在,则返回该键对应的值。
                                                 如果键不存在,则返回None。
        """
        val = await cls.redis.get(cls.get_key(key))
        return json.loads(val) if val else val

    @classmethod
    async def set(cls, key: str, value: Any, ex: int = None, nx: bool = False, xx: bool = False) -> bool:
        """
        将键值对设置到Redis数据库中。

        Args:
            key (str): 要设置的键名。
            value (Any): 要设置的值, 可以是任何类型。
            ex (int): 键的过期时间(秒), 默认为None, 表示不过期。
            nx (bool): 只在键不存在是创建
            xx (bool): 只在键存在是执行

        Returns:
            bool: 如果设置成功则返回True, 否则返回False。
        """
        return await cls.redis.set(cls.get_key(key), value=value, ex=ex, nx=nx, xx=xx)

    @classmethod
    async def incr(cls, key: str, amount: int) -> int:
        """
        增加Redis中指定键的整数值。

        Args:
            key (str): 要增加的键名。
            amount (int): 要增加的数量。

        Returns:
            int: 增加后的整数值, 如果键不存在, 则默认从0开始增加。
        """
        return await cls.redis.incr(cls.get_key(key), amount)

    @classmethod
    async def decr(cls, key: str, amount: int):
        """
        异步减少Redis中指定键的整数值。

        Args:
            key (str): 要减少的键名。
            amount (int): 要减少的数量。

        Returns:
            int: 减少后的整数值, 如果键不存在, Redis将尝试将其解释为0, 然后减少指定的数量。
        """
        return await cls.redis.decr(cls.get_key(key), amount)

    # =============== 【List指令】 ===============
    @classmethod
    async def lPush(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        将一个或多个值插入到列表头部。

        Args:
            key (str): Redis列表的键名。
            *values (Union[int, float, str]): 要插入列表的一个或多个值。

        Returns:
            int: 执行命令后，列表的长度。
        """
        return await cls.redis.lpush(cls.get_key(key), *values)

    @classmethod
    async def rPush(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        将一个或多个值插入到列表尾部。

        Args:
            key (str): Redis列表的键名。
            *values (Union[int, float, str]): 要插入列表的一个或多个值。

        Returns:
            int: 执行命令后，列表的长度。
        """
        return await cls.redis.rpush(cls.get_key(key), *values)

    @classmethod
    async def lPushX(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        将一个值插入到已存在的列表头部。如果列表不存在，则不执行任何操作。

        Args:
            key (str): Redis列表的键名。
            *values (Union[int, float, str]): 要插入列表的一个或多个值。

        Returns:
            int: 执行命令后，列表的长度。如果列表不存在，则返回0。
        """
        return await cls.redis.lpushx(cls.get_key(key), *values)

    @classmethod
    async def rPushX(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        将一个值插入到已存在的列表尾部。如果列表不存在，则不执行任何操作。

        Args:
            key (str): Redis列表的键名。
            *values (Union[int, float, str]): 要插入列表的一个或多个值。

        Returns:
            int: 执行命令后，列表的长度。如果列表不存在，则返回0。
        """
        return await cls.redis.rpushx(cls.get_key(key), *values)

    @classmethod
    async def lPop(cls, key: str, count: int = 1) -> Union[str, List[str], None]:
        """
        移除并返回列表的第一个元素，或者指定数量的元素。

        Args:
            key (str): Redis列表的键名。
            count (int): 要移除的元素数量，默认为1。

        Returns:
            Union[str, List[str], None]: 
                如果count为1，则返回单个元素；
                如果count大于1，则返回包含多个元素的列表；
                如果列表为空，则返回None。
        """
        if count == 1:
            return await cls.redis.lpop(cls.get_key(key))
        else:
            return await cls.redis.lpop(cls.get_key(key), count)

    @classmethod
    async def rPop(cls, key: str, count: int = 1) -> Union[str, List[str], None]:
        """
        移除并返回列表的最后一个元素，或者指定数量的元素。

        Args:
            key (str): Redis列表的键名。
            count (int): 要移除的元素数量，默认为1。

        Returns:
            Union[str, List[str], None]: 
                如果count为1，则返回单个元素；
                如果count大于1，则返回包含多个元素的列表；
                如果列表为空，则返回None。
        """
        if count == 1:
            return await cls.redis.rpop(cls.get_key(key))
        else:
            return await cls.redis.rpop(cls.get_key(key), count)

    @classmethod
    async def blPop(cls, keys: List[str], timeout: int = 0) -> list:
        """
        从第一个非空列表中弹出一个元素，如果列表都为空，则阻塞指定时间。

        Args:
            keys (List[str]): Redis列表的键名列表。
            timeout (int): 阻塞超时时间，单位为秒。默认为0，表示永久阻塞。

        Returns:
            Optional[Tuple[str, str]]: 
                如果成功弹出元素，则返回一个元组，包含键名和弹出的值；
                如果超时，则返回None。
        """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.blpop(ks, timeout)

    @classmethod
    async def brPop(cls, keys: List[str], timeout: int = 0) -> list:
        """
        从第一个非空列表的尾部弹出一个元素，如果列表都为空，则阻塞指定时间。

        Args:
            keys (List[str]): Redis列表的键名列表。
            timeout (int): 阻塞超时时间，单位为秒。默认为0，表示永久阻塞。

        Returns:
            Optional[Tuple[str, str]]: 
                如果成功弹出元素，则返回一个元组，包含键名和弹出的值；
                如果超时，则返回None。
        """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.brpop(ks, timeout)

    @classmethod
    async def brPopLPush(cls, source: str, destination: str, timeout: int = 0) -> Optional[str]:
        """
        从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它；
        如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

        Args:
            source (str): 源列表的键名。
            destination (str): 目标列表的键名。
            timeout (int): 阻塞超时时间，单位为秒。默认为0，表示永久阻塞。

        Returns:
            Optional[str]: 被弹出的元素。如果超时，则返回None。
        """
        src = cls.get_key(source)
        dst = cls.get_key(destination)
        return await cls.redis.brpoplpush(src, dst, timeout)

    @classmethod
    async def lRange(cls, key: str, start: int, end: int) -> List[str]:
        """
        获取列表指定范围内的元素。

        Args:
            key (str): Redis列表的键名。
            start (int): 开始位置，0表示第一个元素，-1表示最后一个元素。
            end (int): 结束位置，0表示第一个元素，-1表示最后一个元素。

        Returns:
            List[str]: 指定范围内的元素列表。
        """
        return await cls.redis.lrange(cls.get_key(key), start, end)

    @classmethod
    async def lIndex(cls, key: str, index: int) -> Optional[str]:
        """
        通过索引获取列表中的元素。

        Args:
            key (str): Redis列表的键名。
            index (int): 索引位置，0表示第一个元素，-1表示最后一个元素。

        Returns:
            Optional[str]: 列表中对应索引的元素。如果索引超出范围，则返回None。
        """
        return await cls.redis.lindex(cls.get_key(key), index)

    @classmethod
    async def lInsert(cls, key: str, where: str, ref_value: str, value: str) -> int:
        """
        在列表的元素前或者后插入元素。

        Args:
            key (str): Redis列表的键名。
            where (str): 插入的位置，可以是 'BEFORE' 或 'AFTER'。
            ref_value (str): 参考值，即在该值前或后插入。
            value (str): 要插入的值。

        Returns:
            int: 执行命令后，列表的长度。如果参考值不存在，则返回-1。
        """
        return await cls.redis.linsert(cls.get_key(key), where, ref_value, value)

    @classmethod
    async def lLen(cls, key: str) -> int:
        """
        获取列表的长度。

        Args:
            key (str): Redis列表的键名。

        Returns:
            int: 列表的长度。如果列表不存在，则返回0。
        """
        return await cls.redis.llen(cls.get_key(key))

    @classmethod
    async def lRem(cls, key: str, count: int, value: str) -> int:
        """
        移除列表中与参数value相等的元素。

        Args:
            key (str): Redis列表的键名。
            count (int): 
                count > 0: 从表头开始向表尾搜索，移除与value相等的元素，数量为count。
                count < 0: 从表尾开始向表头搜索，移除与value相等的元素，数量为count的绝对值。
                count = 0: 移除表中所有与value相等的值。
            value (str): 要移除的值。

        Returns:
            int: 被移除元素的数量。
        """
        return await cls.redis.lrem(cls.get_key(key), count, value)

    @classmethod
    async def lSet(cls, key: str, index: int, value: str) -> str:
        """
        通过索引设置列表元素的值。

        Args:
            key (str): Redis列表的键名。
            index (int): 索引位置，0表示第一个元素，-1表示最后一个元素。
            value (str): 要设置的值。

        Returns:
            str
        """
        return await cls.redis.lset(cls.get_key(key), index, value)

    @classmethod
    async def lTrim(cls, key: str, start: int, end: int) -> str:
        """
        对一个列表进行修剪，只保留指定区间内的元素，不在指定区间之内的元素都将被删除。

        Args:
            key (str): Redis列表的键名。
            start (int): 开始位置，0表示第一个元素，-1表示最后一个元素。
            end (int): 结束位置，0表示第一个元素，-1表示最后一个元素。

        Returns:
            str
        """
        return await cls.redis.ltrim(cls.get_key(key), start, end)

    @classmethod
    async def rPopLPush(cls, source: str, destination: str) -> Optional[str]:
        """
        移除列表的最后一个元素，并将该元素添加到另一个列表并返回。

        Args:
            source (str): 源列表的键名。
            destination (str): 目标列表的键名。

        Returns:
            Optional[str]: 被移除的元素。如果源列表为空，则返回None。
        """
        src = cls.get_key(source)
        dst = cls.get_key(destination)
        return await cls.redis.rpoplpush(src, dst)

    # =============== 【Hash指令】 ===============
    @classmethod
    async def hExists(cls, key: str, field: str) -> bool:
        """
        判断指定哈希表的指定字段是否存在。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要检查的字段名。

        Returns:
            bool: 如果指定字段存在于哈希表中, 则返回True; 否则返回False。
        """
        return await cls.redis.hexists(cls.get_key(key), field)

    @classmethod
    async def hKeys(cls, key: str) -> List[str]:
        """
        获取哈希表中所有的字段键(field)。

        Args:
            key (str): Redis哈希表的键名。

        Returns:
            List[str]: 包含哈希表所有字段键的列表。
        """
        return await cls.redis.hkeys(cls.get_key(key))

    @classmethod
    async def hValS(cls, key: str) -> List[str]:
        """
        获取哈希表中所有字段的值。

        Args:
            key (str): Redis哈希表的键名。

        Returns:
            List[str]: 包含哈希表所有字段值的列表。
        """
        return await cls.redis.hvals(cls.get_key(key))

    @classmethod
    async def hGet(cls, key: str, field: str) -> Optional[str]:
        """
        获取哈希表中指定字段的值。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要获取的字段名。

        Returns:
            Optional[str]: 指定字段的值, 成功返回字符串值, 否则返回None。
        """
        return await cls.redis.hget(cls.get_key(key), field)

    @classmethod
    async def hmGet(cls, key: str, keys: List[str], *args: List[str]) -> List[str]:
        """
        批量获取哈希表中多个字段的值。

        Args:
            key (str): Redis哈希表的键名。
            keys (List[str]): 包含要获取的字段名的列表。
            *args (List[str]): 额外的字段名列表,用于兼容不同形式的参数传入。

        Returns:
            List[str]: 包含指定字段值的列表,顺序与keys中字段的顺序一致。
        """
        return await cls.redis.hmget(cls.get_key(key), keys, *args)

    @classmethod
    async def hGetAll(cls, key: str) -> Dict[str, str]:
        """
        获取哈希表中所有的字段和对应的值。

        Args:
            key (str): Redis哈希表的键名。

        Returns:
            Dict[str, str]: 包含哈希表所有字段和对应值的字典。
        """
        return await cls.redis.hgetall(cls.get_key(key))

    @classmethod
    async def hLen(cls, key: str) -> int:
        """
        获取哈希表中字段的数量。

        Args:
            key (str): Redis哈希表的键名。

        Returns:
            int: 哈希表中字段的数量。
        """
        return await cls.redis.hlen(cls.get_key(key))

    @classmethod
    async def hStrLen(cls, key: str, field: str) -> int:
        """
        获取哈希表中指定字段值的长度(字节)。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要获取长度的字段名。

        Returns:
            int: 字段值的长度(字节)。
        """
        return await cls.redis.hstrlen(cls.get_key(key), field)

    @classmethod
    async def hmSet(cls, key: str, mapping: Dict[str, Union[int, str]], time: int = None) -> int:
        """
        批量设置哈希表中的多个字段和值,并可选择设置过期时间。

        Args:
            key (str): Redis哈希表的键名。
            mapping (Dict[str, Union[int, str]]): 包含字段名和对应值的字典。
            time (int): 过期时间, 单位为秒, 如果提供且大于0, 则设置键的过期时间, 默认为None。

        Returns:
            int: 成功设置的字段数量。
        """
        cnt = await cls.redis.hset(cls.get_key(key), mapping=mapping)
        if time and time > 0:
            await cls.expire(key, time)
        return cnt

    @classmethod
    async def hSet(cls, key: str, field: str, value: FieldT, time: int = None) -> int:
        """
        设置哈希表中指定字段的值,并可选择设置过期时间。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要设置的字段名。
            value (Any): 字段的值。
            time (int): 过期时间, 单位为秒, 如果提供且大于0, 则设置键的过期时间, 默认为None。

        Returns:
            int: 成功设置的字段数量(对于Redis的hSet命令, 通常这个值为1, 除非发生错误）。
        """
        return await cls.hmSet(key, mapping={field: value}, time=time)

    @classmethod
    async def hDel(cls, key: str, *field: str) -> int:
        """
        从Redis哈希表中删除一个或多个字段。

        Args:
            key (str): Redis哈希表的键名。
            *field (str): 要删除的字段名列表。

        Returns:
            int: 成功删除的字段数量。
        """
        return await cls.redis.hdel(cls.get_key(key), *field)

    @classmethod
    async def hSetNx(cls, key: str, field: str, value: str) -> bool:
        """
        如果哈希表中不存在指定字段,则设置该字段的值。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要设置的字段名。
            value (str): 字段的值。

        Returns:
            bool: 如果字段被设置则返回True, 如果字段已存在则返回False。
        """
        return await cls.redis.hsetnx(cls.get_key(key), field, value)

    @classmethod
    async def hInrBy(cls, key: str, field: str, amount: int = 1) -> int:
        """
        对哈希表中指定字段的值进行自增操作。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要自增的字段名。
            amount (int, optional): 自增的数值, 默认为1。

        Returns:
            int: 自增后的字段值。
        """
        return await cls.redis.hincrby(cls.get_key(key), field, amount)

    @classmethod
    async def hIncrByFloat(cls, key: str, field: str, amount: float = 1.0) -> float:
        """
        对哈希表中指定字段的值进行浮点数自增操作。

        Args:
            key (str): Redis哈希表的键名。
            field (str): 要自增的字段名。
            amount (float, optional): 自增的浮点数值, 默认为1.0。

        Returns:
            float: 自增后的字段值。
        """
        return await cls.redis.hincrbyfloat(cls.get_key(key), field, amount)

    # =============== 【Set指令: 无序集合】 ===============
    @classmethod
    async def sAdd(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        向集合中添加一个或多个成员。

        Args:
            key (str): Redis集合的键名。
            *values (Field): 要添加到集合中的成员列表。

        Returns:
            int: 成功添加到集合的新成员数量。
        """
        return await cls.redis.sadd(cls.get_key(key), *values)

    @classmethod
    async def sCard(cls, key: str) -> int:
        """
        获取集合的成员数量。

        Args:
            key (str): Redis集合的键名。

        Returns:
            int: 集合中的成员数量。
        """
        return await cls.redis.scard(cls.get_key(key))

    @classmethod
    async def sDiff(cls, keys: List[str]) -> Set[str]:
        """
        返回给定集合的差集。

        Args:
            keys (List[str): 第一个集合的键名列表。

        Returns:
            Set[str]: 存在于第一个集合, 但不存在于其他任何集合的成员列表。
        """
        ks = [cls.get_key(k) for k in keys]
        return set(await cls.redis.sdiff(ks))

    @classmethod
    async def sDiffStore(cls, dest: str, keys: List[str]) -> int:
        """
       将给定集合的差集存储到另一个集合中。

       Args:
           dest (str): 目标集合的键名。
           keys (List[str]): 第一个集合的键名列表。

       Returns:
           int: 存储到目标集合的新成员数量。
       """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.sdiffstore(dest, ks)

    @classmethod
    async def sInter(cls, keys: List[str]) -> Set[str]:
        """
        返回给定集合的交集。

        Args:
            keys (List[str]): 第一个集合的键名列表。

        Returns:
            Set[str]: 同时存在于所有给定集合的成员列表。
        """
        ks = [cls.get_key(k) for k in keys]
        return set(await cls.redis.sinter(ks))

    @classmethod
    async def sInterCard(cls, numKeys: int, keys: List[str], limit: int = 0) -> int:
        """
        返回给定集合的交集成员数量,同时支持限制返回结果数量。

        Args:
            numKeys (int): 集合键名的数量(用于优化性能)。
            keys (List[str]): 集合的键名列表。
            limit (int): 限制返回结果的数量, 默认为0, 表示不限制。

        Returns:
            int: 交集成员的数量。
        """
        ks = [cls.get_key(k) for k in keys]
        args = [numKeys, *ks, "LIMIT", limit]
        return await cls.redis.execute_command("SINTER_CARD".replace("_", ""), *args)

    @classmethod
    async def sInterStore(cls, dest: str, keys: List[str]) -> int:
        """
        将给定集合的交集存储到另一个集合中。

        Args:
            dest (str): 目标集合的键名。
            keys (List[str]): 第一个集合的键名列表。

        Returns:
            int: 存储到目标集合的新成员数量。
        """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.sinterstore(dest, ks)

    @classmethod
    async def sIsMember(cls, key: str, value: str) -> bool:
        """
        判断给定值是否是Redis集合的成员。

        Args:
            key (str): Redis集合的键名。
            value (str): 要检查的值。

        Returns:
            bool: 如果值是集合的成员, 返回True; 否则返回False。
        """
        return bool(await cls.redis.sismember(cls.get_key(key), value))

    @classmethod
    async def sMembers(cls, key: str) -> Set[str]:
        """
        获取Redis集合的所有成员。

        Args:
            key (str): Redis集合的键名。

        Returns:
            Set[str]: 包含集合所有成员的集合。
        """
        return await cls.redis.smembers(cls.get_key(key))

    @classmethod
    async def sMove(cls, src: str, dst: str, value: str) -> bool:
        """
        将集合的一个成员从源集合移动到目标集合。

        Args:
            src (str): 源集合的键名。
            dst (str): 目标集合的键名。
            value (str): 要移动的成员值。

        Returns:
            bool: 如果移动成功返回True, 否则返回False。
        """
        _src = cls.get_key(src)
        _dst = cls.get_key(dst)
        return await cls.redis.smove(_src, _dst, value)

    @classmethod
    async def sPop(cls, key: str, count: int = None) -> Union[str, List[str], None]:
        """
        从集合中移除并获取一个或多个随机成员。

        Args:
            key (str): Redis集合的键名。
            count (int): 要移除的成员数量。默认为None，表示只移除一个成员。

        Returns:
            Union[str, List[str], None]: 如果提供了count参数且大于0，返回包含移除成员的列表; 否则返回单个移除的成员, 如果没有成员可移除, 返回None。
        """
        args = (count is not None) and [count] or []
        return await cls.redis.execute_command("S_POP".replace("_", ""), cls.get_key(key), *args)

    @classmethod
    async def sRandMember(cls, key: str, number: int = None) -> Union[str, List[str], None]:
        """
        从集合中获取一个或多个随机成员。

        Args:
            key (str): Redis集合的键名。
            number (int): 要获取的随机成员数量, 默认为None, 表示只获取一个成员。

        Returns:
            Union[str, List[str], None]: 如果提供了number参数且大于0，返回包含随机成员的列表；否则返回单个随机成员。如果集合为空，返回None。
        """
        args = (number is not None) and [number] or []
        return await cls.redis.execute_command("SR_AND_MEMBER".replace("_", ""), cls.get_key(key), *args)

    @classmethod
    async def sRem(cls, key: str, *values: Union[int, float, str]) -> int:
        """
        从集合中移除一个或多个成员。

        Args:
           key (str): Redis集合的键名。
           *values (Union[int, float, str]): 要从集合中移除的一个或多个成员。

        Returns:
           int: 被成功移除的成员数量。
        """
        return await cls.redis.srem(cls.get_key(key), *values)

    @classmethod
    async def sUnion(cls, keys: List[str], *args: List[str]) -> Set[str]:
        """
        返回多个集合的并集。

        Args:
            keys (List[str]): 要获取并集的Redis集合的键名列表。
            *args (List[str]): 其他集合的键名列表（可选，用于兼容不同Redis客户端库的额外参数）。

        Returns:
            Set[str]: 包含所有集合并集的列表。
        """
        ks = [cls.get_key(k) for k in keys]
        return set(await cls.redis.sunion(ks, *args))

    @classmethod
    async def sUnionStore(cls, dest: str, keys: List[str], *args: List[str]) -> int:
        """
        返回多个集合的并集,并将结果存储到新的集合中。

        Args:
            dest (str): 用于存储结果的新集合的键名。
            keys (List[str]): 要获取并集的Redis集合的键名列表。
            *args (List[str]): 其他集合的键名列表（可选，用于兼容不同Redis客户端库的额外参数）。

        Returns:
            int: 新集合中元素的数量。
        """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.sunionstore(dest, ks, *args)

    # =============== 【Set指令: 有序集合】 ===============
    @classmethod
    async def zAdd(cls,
                   key: str,
                   mapping: Mapping[Union[int, float, str, list], Union[int, float]],
                   nx: bool = False,
                   xx: bool = False,
                   ch: bool = False,
                   incr: bool = False) -> int:
        """
        将一个或多个成员及其分数添加到有序集合中,或者如果它们已经存在则更新其分数。

        Args:
            key (str): 要操作的有序集合的键名。
            mapping (dict): 其中键是成员,值是对应的分数。
            nx (bool): 如果设置为True, 则仅当集合中不存在该成员时才添加, 默认为False。
            xx (bool): 如果设置为True, 则仅当集合中存在该成员时才更新其分数, 默认为False。
            ch (bool): 如果设置为True, 则返回操作后集合中元素数量的变化量, 默认为False。
            incr (bool):
                如果设置为True, 并且成员已经存在, 则将分数增加到该成员上, 而不是替换它。
                注意: 这个参数与nx和xx参数是互斥的, 通常不会一起使用, 默认为False。

        Returns:
            int: 返回发生改变的成员数量。
        """
        return await cls.redis.zadd(cls.get_key(key), mapping=mapping, nx=nx, xx=xx, ch=ch, incr=incr)

    @classmethod
    async def zCard(cls, key: str) -> int:
        """
        返回有序集合中成员的数量。

        Args:
            key (str): 要操作的有序集合的键名。

        Returns:
            int: 有序集合中成员的数量。
        """
        return await cls.redis.zcard(cls.get_key(key))

    @classmethod
    async def zCount(cls, key: str, min_: int, max_: int) -> int:
        """
        返回有序集合中分数在给定最小值和最大值之间的成员数量。

        Args:
            key (str): 要操作的有序集合的键名。
            min_ (int): 分数范围的最小值（包含）。
            max_ (int): 分数范围的最大值（包含）。

        Returns:
            int: 分数在给定范围内的成员数量。
        """
        return await cls.redis.zcount(cls.get_key(key), min_, max_)

    @classmethod
    async def zDiff(cls, keys: List[str], withScores: bool = False) -> List[str]:
        """
        返回给定有序集合的差集。

        Args:
            keys (List[str]): 包含多个有序集合键名的列表。
            withScores (bool): 如果为True, 则返回每个成员及其分数, 默认为False。

        Returns:
            List[str]: 差集成员列表。如果withScores为True, 则每个成员是一个包含成员名和分数的列表。
        """
        ks = [cls.get_key(k) for k in keys]
        pieces = [len(ks), *ks]
        if withScores:
            pieces.append("WITH_SCORES".replace("_", ""))
        return await cls.redis.execute_command("Z_DIFF".replace("_", ""), *pieces)

    @classmethod
    async def zDiffStore(cls, dest: str, keys: List[str]) -> int:
        """
        计算给定键集合之间的有序集合差集, 并将结果存储在指定的目标键中。

        Args:
            dest (str): 目标键的名称, 用于存储差集的结果。
            keys (List[str]): 一个包含键的列表, 这些键是有序集合, 用于计算差集。

        Returns:
            int: 存储在目标键中的元素数量。
        """
        ks = [cls.get_key(k) for k in keys]
        pieces = [len(ks), *ks]
        return await cls.redis.execute_command("Z_DIFF_STORE".replace("_", ""), dest, *pieces)

    @classmethod
    async def zIncrBy(cls, key: str, amount: float, value: Union[int, float, str]) -> float:
        """
        对有序集合中指定成员的分数进行增量操作。

        Args:
            key (str): 有序集合的键名。
            amount (float): 要增加或减少的分数值。
            value (Union[int, float, str]): 成员的值, 如果成员不是字符串表示的数字, 那么它将被解释为分数并转换为浮点数。

        Returns:
            float: 成员更新后的分数值。
        """
        return await cls.redis.zincrby(cls.get_key(key), amount, value)

    @classmethod
    async def zInterStore(cls, dest: str, keys: List[str], aggregate: str = None) -> int:
        """
        计算给定集合的交集并将结果存储在新的有序集合中。

        Args:
            dest (str): 目标有序集合的键名。
            keys (list): 一个包含多个有序集合键名的列表。
            aggregate (str, None):
                聚合方式: 可以为["SUM", "MIN", "MAX"]。
                默认为 None, 表示取交集元素的分数之和。

        Returns:
            int: 交集后存储在目标有序集合中的元素数量。
        """
        ks = [cls.get_key(k) for k in keys]
        return await cls.redis.zinterstore(cls.get_key(dest), ks, aggregate)

    @classmethod
    async def zInterCard(cls, numKeys: int, keys: List[str], limit: int = 0) -> int:
        """
        返回给定有序集合的交集元素的数量,但不存储结果。

        Args:
            numKeys (int): 参与交集计算的有序集合的数量,应与keys列表的长度一致。
            keys (List[str]): 包含多个有序集合键名的列表。
            limit (int):
                表示只计算前limit个有序集合的交集元素数量。
                默认为0, 表示计算所有集合的交集元素数量。

        Returns:
            int: 交集元素的数量。
        """
        ks = [cls.get_key(k) for k in keys]
        args = [numKeys, *ks, "LIMIT", limit]
        return await cls.redis.execute_command("Z_INTER_CARD".replace("_", ""), *args)

    @classmethod
    async def zLexCount(cls, key: str, min_: str, max_: str) -> int:
        """
        返回有序集合中指定字典区间内成员的数量。

        Args:
            key (str): 有序集合的键名。
            min_ (str): 字典序最小成员(包含)。
            max_ (str): 字典序最大成员(包含)。

        Returns:
            int: 指定区间内成员的数量。
        """
        return await cls.redis.zlexcount(cls.get_key(key), min_, max_)

    @classmethod
    async def zPopMax(cls, key: str, count: int = None) -> Union[List[Tuple[str, float]], Tuple[str, float]]:
        """
        移除并返回有序集合中分数最高的成员。

        Args:
            key (str): 有序集合的键名。
            count (int): 表示要移除并返回的成员数量, 默认为 None, 表示只移除并返回一个成员。

        Returns:
            Union[List[Tuple[str, float]], Tuple[str, float]]:
                如果count参数被指定且大于1, 则返回一个包含成员和分数的元组列表；
                否则, 只返回一个包含成员和分数的元组。
        """
        return await cls.redis.zpopmax(cls.get_key(key), count)

    @classmethod
    async def zPopMin(cls, key: str, count: int = None) -> Union[List[Tuple[str, float]], Tuple[str, float]]:
        """
        移除并返回有序集合中分数最低的成员。

        Args:
            key (str): 有序集合的键名。
            count (int): 表示要移除并返回的成员数量, 默认为 1, 表示只移除并返回一个成员。

        Returns:
            Union[List[Tuple[str, float]], Tuple[str, float]]:
                如果count参数大于1, 则返回一个包含成员和分数的元组列表；
                否则, 只返回一个包含成员和分数的元组。
        """
        return await cls.redis.zpopmin(cls.get_key(key), count)

    @classmethod
    async def zRandMember(cls,
                          key: str,
                          count: int = None,
                          withCores: bool = False) -> Union[str, List[Union[str, Tuple[str, float]]]]:
        """
        从有序集合中随机返回指定数量的成员。

        Args:
            key (str): 有序集合的键名。
            count (int): 表示要返回的随机成员数量, 默认为 None, 表示只返回一个随机成员。
            withCores (bool): 表示是否同时返回成员的分数, 默认为 False。

        Returns:
            Union[str, List[Union[str, Tuple[str, float]]]]:
                如果count参数未指定或小于等于 1, 并且withCores为 False, 则返回一个随机成员;
                如果count参数未指定或小于等于 1, 但withCores为 True, 则返回一个包含成员和分数的元组;
                如果count参数大于 1, 并且withCores为 False, 则返回一个随机成员列表;
                如果count参数大于 1, 并且withCores为 True, 则返回一个包含成员和分数的元组列表。
        """
        params = []
        if count is not None:
            params.append(str(count))
        if withCores:
            params.append("WITH_SCORES".replace("_", ""))

        return await cls.redis.execute_command("Z_RAND_MEMBER".replace("_", ""), cls.get_key(key), *params)

    @classmethod
    async def bZPopMax(cls, keys: List[str], timeout: int = 0) -> Optional[Tuple[str, str, float]]:
        """
        从给定的一个或多个阻塞有序集合中弹出具有最高分数的成员。

        Args:
            keys (List[str]): 包含多个阻塞有序集合键名的列表。
            timeout (int): 等待阻塞有序集合中有可用元素的最大秒数。默认为 0, 表示永远阻塞。

        Returns:
            Optional[Tuple[str, str, float]]:
                如果在超时时间内有元素可用, 返回一个三元组, 包含：
                - 弹出元素的键名（str）
                - 弹出元素的成员（str）
                - 弹出元素的分数（float）
                如果超时时间内没有元素可用, 则返回 None。
        """
        ks = [cls.get_key(k) for k in keys if await cls.exists(k)]
        if not ks:
            return None
        return await cls.redis.bzpopmax(ks, timeout)

    @classmethod
    async def bZPopMin(cls, keys: List[str], timeout: int = 0) -> Optional[Tuple[str, str, float]]:
        """
        从给定的一个或多个阻塞有序集合中弹出具有最低分数的成员。

        Args:
            keys (List[str]): 包含多个阻塞有序集合键名的列表。
            timeout (int, optional): 等待阻塞有序集合中有可用元素的最大秒数, 默认为 0, 表示永远阻塞。

        Returns:
            Optional[Tuple[str, str, float]]:
                如果在超时时间内有元素可用，返回一个三元组，包含：
                - 弹出元素的键名（str）
                - 弹出元素的成员（str）
                - 弹出元素的分数（float）
                如果超时时间内没有元素可用, 则返回 None。
        """
        ks = [cls.get_key(k) for k in keys if await cls.exists(k)]
        if not ks:
            return None
        return await cls.redis.bzpopmin(ks, timeout)

    @classmethod
    async def zmPop(cls,
                    numKeys: int,
                    keys: List[str],
                    min_: bool = False,
                    max_: bool = False,
                    count: int = 1) -> List[Tuple[str, str, float]]:
        """
        从多个有序集合中按分数弹出成员。

        Args:
            numKeys (int): 需要从中弹出成员的有序集合的键数量。
            keys (List[str]): 包含多个有序集合键名的列表。
            min_ (bool): 如果为 True, 则从每个键的最小分数成员中弹出, 默认为 False。
            max_ (bool): 如果为 True, 则从每个键的最大分数成员中弹出, 默认为 False。
            count (int): 从每个键中弹出的成员数量。默认为 1。

        Returns:
            List[Tuple[str, str, float]]:
            返回一个列表, 其中每个元素都是一个三元组, 包含：
            - 弹出成员的键名（str）
            - 弹出成员的值（str）
            - 弹出成员的分数（float）

        Raises:
            DataError: 如果同时指定了 min_ 和 max_ 参数，或者两者都未指定。
        """
        ks = [cls.get_key(k) for k in keys]
        args = [str(numKeys)] + ks
        if (min_ and max_) or (not min_ and not max_):
            raise DataError
        elif min_:
            args.append("MIN")
        else:
            args.append("MAX")
        if count != 1:
            args.extend(["COUNT", count])

        return await cls.redis.execute_command("ZM_POP".replace("_", ""), *args)

    @classmethod
    async def bzmPop(cls,
                     timeout: float,
                     numKeys: int,
                     keys: List[str],
                     min_: bool = False,
                     max_: bool = False,
                     count: int = 1) -> Optional[List[any]]:
        """
        从多个有序集合中按分数阻塞地弹出成员。

        Args:
            timeout (float): 阻塞等待的最大秒数。
            numKeys (int): 需要从中弹出成员的有序集合的键数量。
            keys (List[str]): 包含多个有序集合键名的列表。
            min_ (bool): 如果为 True, 则从每个键的最小分数成员中弹出, 默认为 False。
            max_ (bool): 如果为 True, 则从每个键的最大分数成员中弹出, 默认为 False。
            count (int): 从每个键中弹出的成员数量。默认为 1。

        Returns:
            Optional[List[any]]: 包含键名成员和分数的列表。

        Raises:
            DataError: 如果同时指定了 min_ 和 max_ 参数, 或者两者都未指定。
        """
        ks = [cls.get_key(k) for k in keys]
        args = [timeout, numKeys, *ks]
        if (min_ and max_) or (not min_ and not max_):
            raise DataError("Either min or max, but not both must be set")
        elif min_:
            args.append("MIN")
        else:
            args.append("MAX")
        args.extend(["COUNT", count])

        return await cls.redis.execute_command("BZM_POP".replace("_", ""), *args)

    # =============== 【发布订阅】 ===============
    @classmethod
    async def publish(cls, channel: str, scene: str, data: Any = None, **kwargs):
        """
        向指定频道发布消息

        Args:
            channel (str): 要发布的频道名称
            scene (str): 场景类型
            data (Any): 发布数据
            **kwargs: 额外的参数

        Returns:
            返回消息被投递到的订阅者数量
        """
        key = cls.get_key(channel)
        message = json.dumps({"scene": scene, "data": data})
        return await cls.redis.publish(key, message, **kwargs)

    @classmethod
    async def subscribe(cls, channel: str):
        """
        订阅指定频道并返回 PubSub 对象用于监听消息。

        Args:
            channel (str): 要订阅的频道名称

        Returns:
            redis.client.PubSub:
                返回 PubSub 对象，调用方需维护其生命周期。
            Demo：
                 pubsub = await subscribe("my_channel")
                 async for message in pubsub.listen():
                     print(message)

        PubSub对象：
            1. 调用 pubsub.listen() 接收消息
            2. 调用 pubsub.unsubscribe() 取消订阅
            3. 调用 pubsub.close() 释放资源
        """
        key = cls.get_key(channel)
        pubsub = cls.redis.pubsub()
        await pubsub.subscribe(key)
        return pubsub
