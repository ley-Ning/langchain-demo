"""
李四（学徒）的工具插件

这个模块定义了李四（学徒）可以使用的工具函数。
李四是张三的学徒，负责协助打造装备、查询价格和收款。
"""
from typing import Dict


class LiSiPlugin:
    """
    李四的工具集
    
    这个类包含了李四（学徒）在协助打造装备过程中需要使用的工具。
    包含两个工具：
    1. 查询装备价格
    2. 向玩家发起支付请求
    """
    
    # 装备价格数据库
    # 存储了各种装备的价格（单位：灵石）
    PRICE_DB: Dict[str, int] = {
        "飞剑": 500,
        "护甲": 300,
        "法杖": 450,
        "灵靴": 200,
    }
    
    @staticmethod
    def get_equipment_price(equipment_name: str) -> str:
        """
        查询装备价格
        
        这是李四的第一个工具，用于查询指定装备的价格。
        当张三完成装备打造后，李四会调用这个工具来查询价格并报价。
        
        Args:
            equipment_name: 装备名称（例如：飞剑、护甲、法杖、灵靴）
            
        Returns:
            装备价格字符串，格式为 "【装备名】的价格是 X 灵石"
            如果装备不在数据库中，返回默认价格 100 灵石
        """
        # 从数据库中查询价格
        price = LiSiPlugin.PRICE_DB.get(equipment_name, 100)  # 默认价格 100 灵石
        
        # 格式化并返回价格信息
        return f"【{equipment_name}】的价格是 {price} 灵石"
    
    @staticmethod
    def request_payment(equipment_name: str, amount: int) -> str:
        """
        向玩家发起支付请求
        
        这是李四的第二个工具，用于向玩家发起支付请求。
        当张三确认报价后，李四会调用这个工具向玩家收款。
        
        Args:
            equipment_name: 装备名称（例如：飞剑、护甲、法杖、灵靴）
            amount: 金额（单位：灵石）
            
        Returns:
            支付结果字符串
            - 如果支付成功：返回确认信息
            - 如果取消支付：返回取消信息
        """
        print(f"\n" + "="*60)
        print(f"💰 [支付系统]")
        print("="*60)
        print(f"装备名称: 【{equipment_name}】")
        print(f"支付金额: {amount} 灵石")
        print("="*60)
        
        try:
            while True:
                user_input = input("\n👤 是否确认支付？(y/n): ").strip().lower()
                
                if user_input in ['y', 'yes', '是']:
                    print("\n✅ 支付成功！")
                    return f"✅ 玩家已支付 {amount} 灵石，交易完成！"
                elif user_input in ['n', 'no', '否']:
                    print("\n❌ 已取消支付")
                    return f"❌ 玩家取消了支付"
                else:
                    print("⚠️  请输入 y (确认) 或 n (取消)")
        except (EOFError, KeyboardInterrupt):
            # 如果无法读取输入或用户中断，视为取消
            print("\n❌ 支付已取消")
            return f"❌ 玩家取消了支付"

