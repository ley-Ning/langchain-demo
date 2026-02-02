"""
测试取消支付场景
"""
from unittest.mock import patch
from langchain_openai import AzureChatOpenAI
from src.agents.zhangsan_agent import create_zhangsan_agent
from src.agents.lisi_agent import create_lisi_agent
from src.core.agent_group_chat import AgentGroupChat
from src.config.settings import settings


def main():
    """测试取消支付场景"""
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
    
    print("\n" + "="*60)
    print("🧪 测试场景：玩家取消支付")
    print("="*60)
    
    # 模拟用户输入
    user_input = "我想打造一把飞剑"
    print(f"\n👤 玩家: {user_input}")
    chat.add_user_message(user_input)
    
    print("\n" + "="*60)
    print("🏪 开始对话")
    print("="*60 + "\n")
    
    # Mock input 函数，第一次返回 'n' (取消支付)
    with patch('builtins.input', return_value='n'):
        response_count = 0
        for response in chat.run():
            response_count += 1
            agent_name = response.name if hasattr(response, 'name') else "未知"
            print(f"🔨 [{response_count}] {agent_name}: {response.content}\n")
            
            # 如果超过 15 轮对话，停止（防止无限循环）
            if response_count > 15:
                print("\n⚠️  达到测试轮数限制，停止测试")
                break
    
    print("="*60)
    print(f"✅ 测试完成，共 {response_count} 轮对话")
    print("="*60)


if __name__ == "__main__":
    main()
