"""
肖斩天（打手）的工具插件

这个模块定义了肖斩天（打手）可以使用的工具函数。
肖斩天是铁匠铺的打手，负责催债和威胁不付钱的客人。
"""


class XiaoZhanPlugin:
    """
    肖斩天的工具集
    
    这个类包含了肖斩天（打手）在催债时需要使用的工具。
    """
    
    @staticmethod
    def threaten_customer() -> str:
        """
        威胁客人
        
        Returns:
            威胁语句
        """
        threats = [
            "💢 老子的拳头可不认人！",
            "💢 不想挨揍就赶紧掏钱！",
            "💢 别逼老子动手，后果自负！",
            "💢 这条街上还没人敢欠我们的钱！"
        ]
        import random
        return random.choice(threats)
    
    @staticmethod
    def beat_customer() -> str:
        """
        打人（催债）
        
        Returns:
            打人动作描述
        """
        actions = [
            "👊 肖斩天一拳打在桌子上，桌子应声而裂！",
            "👊 肖斩天抓起铁锤，狠狠砸在地上，地面都震了三震！",
            "👊 肖斩天撸起袖子，露出满臂的刀疤，眼神凶狠！",
            "👊 肖斩天一脚踢翻椅子，整个铁匠铺都安静了！"
        ]
        import random
        return random.choice(actions)
    
    @staticmethod
    def force_payment(equipment_name: str, amount: int) -> str:
        """
        强制收款（威胁式）
        
        Args:
            equipment_name: 装备名称
            amount: 金额
            
        Returns:
            收款结果
        """
        print(f"\n" + "="*60)
        print(f"💀 [肖斩天催债]")
        print("="*60)
        print(f"装备：【{equipment_name}】")
        print(f"金额：{amount} 灵石")
        print("="*60)
        print("💀 肖斩天：老子最后问一次，给不给钱？！")
        print("="*60)
        
        try:
            while True:
                user_input = input("\n👤 给钱吗？(y/n): ").strip().lower()
                
                if user_input in ['y', 'yes', '是']:
                    print("\n✅ 你乖乖交钱了")
                    return f"✅ 玩家被打怕了，乖乖支付了 {amount} 灵石！"
                elif user_input in ['n', 'no', '否']:
                    print("\n💢 你还敢说不？！")
                    return f"💢 玩家还在嘴硬，继续不给钱！"
                else:
                    print("⚠️  请输入 y (给钱) 或 n (不给)")
        except (EOFError, KeyboardInterrupt):
            print("\n💢 想跑？没门！")
            return f"💢 玩家想跑，被肖斩天拦住了！"
