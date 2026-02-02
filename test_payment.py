"""
简单测试：验证取消支付后的终止逻辑
"""
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import AzureChatOpenAI
from src.agents.zhangsan_agent import create_zhangsan_agent
from src.agents.lisi_agent import create_lisi_agent
from src.core.agent_group_chat import AgentGroupChat
from src.config.settings import settings


def test_termination_with_cancel():
    """测试取消支付时的终止判断"""
    print("\n" + "="*60)
    print("🧪 测试：取消支付时的终止判断")
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
    
    # 模拟对话历史：装备打造完成，李四发起支付，玩家取消
    chat.history = [
        HumanMessage(content="我想打造一把飞剑", name="玩家"),
        AIMessage(content="装备打造完成了，李四！", name="张三"),
        AIMessage(content="好的，价格是500灵石", name="李四"),
        ToolMessage(content="❌ 玩家取消了支付", tool_call_id="test_123"),
        AIMessage(content="哎呀，大侠您居然取消支付了，真是让小李四伤心呀！", name="李四"),
    ]
    
    # 测试终止判断
    should_end = chat.should_terminate(last_speaker="李四")
    
    print(f"\n结果：should_terminate = {should_end}")
    print(f"预期：should_terminate = False (因为玩家取消了支付)")
    
    if should_end:
        print("\n❌ 测试失败：对话不应该终止！")
    else:
        print("\n✅ 测试通过：对话继续，张三可以发飙骂人！")
    
    print("="*60)


def test_termination_with_success():
    """测试支付成功时的终止判断"""
    print("\n" + "="*60)
    print("🧪 测试：支付成功时的终止判断")
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
    
    # 模拟对话历史：装备打造完成，李四发起支付，玩家支付成功
    chat.history = [
        HumanMessage(content="我想打造一把飞剑", name="玩家"),
        AIMessage(content="装备打造完成了，李四！", name="张三"),
        AIMessage(content="好的，价格是500灵石", name="李四"),
        ToolMessage(content="✅ 玩家已支付 500 灵石，交易完成！", tool_call_id="test_123"),
        AIMessage(content="太好了！感谢大侠！", name="李四"),
    ]
    
    # 测试终止判断
    should_end = chat.should_terminate(last_speaker="李四")
    
    print(f"\n结果：should_terminate = {should_end}")
    print(f"预期：should_terminate = True (因为玩家已支付)")
    
    if should_end:
        print("\n✅ 测试通过：对话应该终止！")
    else:
        print("\n❌ 测试失败：对话应该终止！")
    
    print("="*60)


if __name__ == "__main__":
    # 测试1：取消支付
    test_termination_with_cancel()
    
    # 测试2：支付成功
    test_termination_with_success()
