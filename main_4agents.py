"""
主程序 - 4个智能体版本（黑社会铁匠铺）

角色：
1. 张三（铁匠）- 暴躁粗鲁
2. 李四（学徒）- 活泼机灵
3. 麻子（财务）- 细腻严谨
4. 肖斩天（打手）- 凶狠暴力
"""
import sys
import time
from langchain_openai import AzureChatOpenAI
from src.agents.zhangsan_agent import create_zhangsan_agent
from src.agents.lisi_agent import create_lisi_agent
from src.agents.mazi_agent import create_mazi_agent
from src.agents.xiaozhan_agent import create_xiaozhan_agent
from src.core.agent_group_chat import AgentGroupChat
from src.config.settings import settings


def print_stream(text: str, delay: float = 0.02):
    """
    流式输出文本（逐字输出）
    
    Args:
        text: 要输出的文本
        delay: 每个字符之间的延迟（秒），默认 0.02 秒
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # 换行


def main():
    """
    主函数 - 4个智能体协作
    """
    # 初始化 LLM
    llm = AzureChatOpenAI(
        azure_deployment=settings.MODEL_NAME,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=settings.TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
        azure_endpoint=settings.OPENAI_API_BASE
    )
    
    # 创建4个智能体
    zhangsan_data = create_zhangsan_agent(llm)
    lisi_data = create_lisi_agent(llm)
    mazi_data = create_mazi_agent(llm)
    xiaozhan_data = create_xiaozhan_agent(llm)
    
    # 创建智能体群聊
    agents = {
        "张三": zhangsan_data,
        "李四": lisi_data,
        "麻子": mazi_data,
        "肖斩天": xiaozhan_data
    }
    
    chat = AgentGroupChat(agents=agents, llm=llm, max_rounds=30)
    
    # 欢迎信息
    print("\n" + "="*60)
    print("🎮 修仙游戏 - 黑社会铁匠铺")
    print("="*60)
    print("欢迎来到铁匠铺，你想打造什么装备？")
    print("⚠️  警告：这里有打手肖斩天，不给钱后果自负！")
    print("="*60)
    
    # 装备选择菜单
    equipment_options = {
        "1": "飞剑",
        "2": "护甲",
        "3": "法杖",
        "4": "灵靴"
    }
    
    print("\n请选择要打造的装备：")
    print("1. 飞剑 - 锋利无比的飞行法宝")
    print("2. 护甲 - 坚不可摧的防御装备")
    print("3. 法杖 - 增强法力的神秘法器")
    print("4. 灵靴 - 轻盈如风的移动装备")
    
    choice = input("\n👤 请输入选项 (1-4): ").strip()
    
    if choice not in equipment_options:
        print("❌ 无效的选择，请输入 1-4")
        return
    
    equipment_name = equipment_options[choice]
    user_input = f"我想打造一把{equipment_name}" if equipment_name == "飞剑" else f"我想打造一个{equipment_name}"
    
    print(f"\n👤 玩家: {user_input}")
    
    # 将用户消息添加到群聊
    chat.add_user_message(user_input)
    
    print("\n" + "="*60)
    print("🏪 铁匠铺开始营业！")
    print("="*60 + "\n")
    
    # 运行群聊
    for response, token_usage in chat.run():
        agent_name = response.name if hasattr(response, 'name') else "未知"
        
        # 根据角色显示不同的图标
        icon = {
            "张三": "🔨",
            "李四": "👦",
            "麻子": "💰",
            "肖斩天": "💀"
        }.get(agent_name, "🤖")
        
        # 流式输出响应内容
        sys.stdout.write(f"{icon} {agent_name}: ")
        sys.stdout.flush()
        print_stream(response.content, delay=0.015)
        
        # 显示 token 使用情况
        print(f"   📊 Token: 输入={token_usage['prompt_tokens']}, "
              f"输出={token_usage['completion_tokens']}, "
              f"总计={token_usage['total_tokens']}\n")
    
    # 显示总 token 使用情况
    total_usage = chat.get_total_token_usage()
    print("="*60)
    print("✅ 对话结束")
    print("="*60)
    print(f"📊 总 Token 消耗统计：")
    print(f"   输入 Token: {total_usage['prompt_tokens']}")
    print(f"   输出 Token: {total_usage['completion_tokens']}")
    print(f"   总计 Token: {total_usage['total_tokens']}")
    print("="*60)


if __name__ == "__main__":
    main()
