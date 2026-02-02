"""主程序入口"""
from src.core.chat_manager import MultiAgentChatManager


def main():
    """主函数"""
    chat_manager = MultiAgentChatManager()
    
    print("\n" + "="*60)
    print("🎮 修仙游戏 - 铁匠铺")
    print("="*60)
    print("欢迎来到铁匠铺，你想打造什么装备？")
    print("(可选装备: 飞剑、护甲、法杖、灵靴)")
    print("="*60)
    
    user_input = input("\n👤 玩家 - 你: ").strip()
    
    if not user_input:
        print("❌ 输入不能为空")
        return
    
    # 运行多智能体对话
    chat_manager.run(user_input)


if __name__ == "__main__":
    main()
