"""
麻子（财务）的工具插件

这个模块定义了麻子（财务）可以使用的工具函数。
麻子是铁匠铺的财务，负责精确计算账单。
"""
from typing import Dict


class MaZiPlugin:
    """
    麻子的工具集
    
    这个类包含了麻子（财务）在计算账单时需要使用的工具。
    """
    
    # 装备基础价格
    BASE_PRICE: Dict[str, int] = {
        "飞剑": 500,
        "护甲": 300,
        "法杖": 450,
        "灵靴": 200,
    }
    
    # 材料成本
    MATERIAL_COST: Dict[str, int] = {
        "飞剑": 200,
        "护甲": 150,
        "法杖": 180,
        "灵靴": 80,
    }
    
    @staticmethod
    def calculate_total_price(equipment_name: str) -> str:
        """
        计算装备总价
        
        Args:
            equipment_name: 装备名称
            
        Returns:
            总价信息
        """
        base = MaZiPlugin.BASE_PRICE.get(equipment_name, 100)
        return f"【{equipment_name}】总价：{base} 灵石"
    
    @staticmethod
    def calculate_cost(equipment_name: str) -> str:
        """
        计算材料成本
        
        Args:
            equipment_name: 装备名称
            
        Returns:
            成本信息
        """
        cost = MaZiPlugin.MATERIAL_COST.get(equipment_name, 50)
        return f"【{equipment_name}】材料成本：{cost} 灵石"
    
    @staticmethod
    def calculate_profit(equipment_name: str) -> str:
        """
        计算利润
        
        Args:
            equipment_name: 装备名称
            
        Returns:
            利润信息
        """
        base = MaZiPlugin.BASE_PRICE.get(equipment_name, 100)
        cost = MaZiPlugin.MATERIAL_COST.get(equipment_name, 50)
        profit = base - cost
        return f"【{equipment_name}】利润：{profit} 灵石（售价 {base} - 成本 {cost}）"
    
    @staticmethod
    def generate_bill(equipment_name: str) -> str:
        """
        生成详细账单
        
        Args:
            equipment_name: 装备名称
            
        Returns:
            详细账单
        """
        base = MaZiPlugin.BASE_PRICE.get(equipment_name, 100)
        cost = MaZiPlugin.MATERIAL_COST.get(equipment_name, 50)
        profit = base - cost
        
        bill = f"""
╔════════════════════════════════╗
║        铁匠铺账单明细          ║
╠════════════════════════════════╣
║ 装备名称：【{equipment_name}】
║ 材料成本：{cost} 灵石
║ 人工费用：{profit // 2} 灵石
║ 店铺利润：{profit - profit // 2} 灵石
║ ────────────────────────────
║ 应收总额：{base} 灵石
╚════════════════════════════════╝
"""
        return bill
