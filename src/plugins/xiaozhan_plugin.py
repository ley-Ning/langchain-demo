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
        警告客人
        
        Returns:
            警告语句
        """
        threats = [
            "⚠️ 我劝你最好想清楚后果！",
            "⚠️ 别不识抬举，这是最后机会！",
            "⚠️ 欠债还钱，天经地义！",
            "⚠️ 这条街上还没人敢欠我们的钱！"
        ]
        import random
        return random.choice(threats)
    
    @staticmethod
    def beat_customer() -> str:
        """
        展示威慑力
        
        Returns:
            威慑动作描述
        """
        actions = [
            "👊 肖斩天重重一拍桌子，桌子发出巨响！",
            "👊 肖斩天用力跺脚，整个铁匠铺都震了一下！",
            "👊 肖斩天撸起袖子，露出结实的肌肉，眼神严肃！",
            "👊 肖斩天站起身来，气势逼人！"
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
        print(f"⚠️ [肖斩天催债]")
        print("="*60)
        print(f"装备：【{equipment_name}】")
        print(f"金额：{amount} 灵石")
        print("="*60)
        print("⚠️ 肖斩天：我最后问一次，给不给钱？")
        print("="*60)
        
        try:
            while True:
                user_input = input("\n👤 给钱吗？(y/n): ").strip().lower()
                
                if user_input in ['y', 'yes', '是']:
                    print("\n✅ 你乖乖交钱了")
                    return f"✅ 玩家被震慑住了，乖乖支付了 {amount} 灵石！"
                elif user_input in ['n', 'no', '否']:
                    print("\n⚠️ 你还敢说不？")
                    return f"⚠️ 玩家还在犹豫，继续不给钱！"
                else:
                    print("⚠️  请输入 y (给钱) 或 n (不给)")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ 想跑？没门！")
            return f"⚠️ 玩家想跑，被肖斩天拦住了！"
