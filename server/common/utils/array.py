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
from typing import TypeVar, Union, List, Dict, Any

T = TypeVar("T")


class ArrayUtil:
    """ 数组工具 """

    @staticmethod
    def list_to_tree(arr: List[Dict[str, Any]], id_: str, pid: str, child: str) -> Union[T, List[Dict[str, Any]]]:
        """
        将包含字典的列表转换为树形结构。

        Args:
            arr (List[Dict[str, Any]]): 包含字典的列表,每个字典表示树中的一个节点。
            id_ (str): 字典中作为主键的字段名。
            pid (str): 字典中表示父节点ID的字段名。
            child (str): 在树形结构中,用于存储子节点的字段名。

        Returns:
            Union[List[Dict[str, Any]], Dict[str, Any]]: 转换后的树形结构,可以是列表(根节点列表)或单个字典(单根树)。

        Author:
            zero
        """
        # 使用id_字段的值作为键，将arr中的字典映射为字典。
        id_dict_map = {item[id_]: item for item in arr}
        # 用于存放顶级节点（即没有父节点的节点）的列表。
        top_level_nodes = []

        # 遍历arr中的每个字典
        for item in arr:
            # 获取父节点ID
            parent_id = item.get(pid)
            # 尝试从映射中获取父节点
            p_node = id_dict_map.get(parent_id)

            # 如果找到父节点,则将当前节点添加到父节点的子节点列表中
            if p_node:
                # 确保child字段在p_node中存在
                if child in p_node:
                    p_node[child].append(item)
                else:
                    p_node[child] = [item]
                    # 如果没有父节点(即顶级节点),则将其添加到top_level_nodes列表中
            else:
                top_level_nodes.append(item)

        # 如果只有一个顶级节点,并且该节点有child字段,则返回这个节点(表示单根树)
        if len(top_level_nodes) == 1 and child in top_level_nodes[0]:
            if not top_level_nodes[0]:
                return []
            return top_level_nodes[0] if isinstance(top_level_nodes[0], list) else [top_level_nodes[0]]
        # 否则返回顶级节点列表(表示多根树)
        else:
            return top_level_nodes
