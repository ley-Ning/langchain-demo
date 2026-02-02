"""
演示最终版本：流式输出 + Token 统计
"""
import sys
import time
from unittest.mock import patch
from langchain_openai import AzureChatOpenAI
from src.agents.zhangsan_agent import create_zhangsan_agent
from src.agents.lisi_agent import create_lisi_agent
from src.core.agent_group_chat import AgentGroupChat
from src.config.settings import settings


def print_stream(text: str, delay: float = 0.015):
    """流式输出文本"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def main():
    """演示流式输出和 Token 统计"""
    print("\n" + "="*60)
    print("🎮 修仙游戏 - 铁匠铺（流式输出 + Token 统计）")
    print("="*60)
    
    # 初始化 LLM
    llm = AzureChatOpenAI(
        azure_deployment=settings.MODEL_NAME,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=settings.TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
        azure_endpoint=settings.OPENAI_API_BASE
    )
    
    # 创建智能体
    zhangsan_data = create_zhangsan_agent(llm)
    lisi_data = create_lisi_agent(llm)
    
    agents = {
        "张三": zhangsan_data,
        "李四": lisi_data
    }
    
    chat = AgentGroupChat(agents=agents, llm=llm, max_rounds=20)
    
    # 模拟用户输入
    user_input = "我想打造一把飞剑"
    print(f"\n👤 玩家: {user_input}")
    chat.add_user_message(user_input)
    
    print("\n" + "="*60)
    print("🏪 开始对话")
    print("="*60 + "\n")
    
    # Mock input 函数，自动支付
    with patch('builtins.input', return_value='y'):
        response_count = 0
        for response, token_usage in chat.run():
            response_count += 1
            agent_name = response.name if hasattr(response, 'name') else "未知"
            
            # 流式输出
            sys.stdout.write(f"🔨 [{response_count}] {agent_name}: ")
            sys.stdout.flush()
            print_stream(response.content, delay=0.015)
            
            # 显示 token 使用情况
            print(f"   💰 Token: 输入={token_usage['prompt_tokens']}, "
                  f"输出={token_usage['completion_tokens']}, "
                  f"总计={token_usage['total_tokens']}\n")
            
            # 限制测试轮数
            if response_count > 15:
                print("\n⚠️  达到测试轮数限制")
                break
    
    # 显示总统计
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
