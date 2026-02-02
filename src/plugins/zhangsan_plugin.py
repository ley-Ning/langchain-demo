"""
张三（铁匠）的工具插件

这个模块定义了张三（铁匠）可以使用的工具函数。
张三是一个铸造装备的铁匠，他的主要工具是查询装备材料清单。
"""
from typing import Dict, List


class ZhangSanPlugin:
    """
    张三的工具集
    
    这个类包含了张三（铁匠）在打造装备过程中需要使用的工具。
    目前包含一个工具：查询装备材料清单。
    """
    
    # 装备材料数据库
    # 存储了各种装备所需的材料清单
    MATERIALS_DB: Dict[str, List[str]] = {
        "飞剑": ["玄铁 x3", "寒冰石 x2", "灵木 x1"],
        "护甲": ["精钢 x5", "兽皮 x3", "符文布 x2"],
        "法杖": ["紫檀木 x2", "灵晶 x3", "凤凰羽 x1"],
        "灵靴": ["软皮 x2", "云纹石 x1", "轻羽 x3"],
    }
    
    @staticmethod
    def get_equipment_materials(equipment_name: str) -> str:
        """
        查询制作装备所需的材料清单
        
        这是张三的核心工具，用于查询打造指定装备所需的材料。
        当玩家提出打造装备的需求时，张三会调用这个工具来获取材料清单。
        
        Args:
            equipment_name: 装备名称（例如：飞剑、护甲、法杖、灵靴）
            
        Returns:
            材料清单字符串，格式为 "制作【装备名】需要材料：材料1, 材料2, ..."
            如果装备不在数据库中，返回默认的神秘材料提示
        """
        # 从数据库中查询材料清单
        materials = ZhangSanPlugin.MATERIALS_DB.get(
            equipment_name, 
            ["未知装备，需要：神秘材料 x1"]  # 默认材料（当装备不在数据库中时）
        )
        
        # 格式化并返回材料清单
        return f"制作【{equipment_name}】需要材料：{', '.join(materials)}"
