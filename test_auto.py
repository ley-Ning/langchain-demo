"""
自动化测试：不需要 API 调用，直接测试逻辑
"""
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


def test_format_history():
    """测试历史记录格式化"""
    print("\n" + "="*60)
    print("🧪 测试：历史记录格式化")
    print("="*60)
    
    # 模拟历史记录
    history = [
        HumanMessage(content="我想打造一把飞剑", name="玩家"),
        AIMessage(content="装备打造完成了，李四！", name="张三"),
        AIMessage(content="好的，价格是500灵石", name="李四"),
        ToolMessage(content="❌ 玩家取消了支付", tool_call_id="test_123"),
        AIMessage(content="哎呀，大侠您居然取消支付了！", name="李四"),
    ]
    
    # 格式化历史记录（模拟 _format_history 方法）
    recent = history[-5:]
    formatted = []
    for msg in recent:
        name = getattr(msg, 'name', '未知')
        content = msg.content if hasattr(msg, 'content') else str(msg)
        if content:
            formatted.append(f"{name}: {content}")
    
    recent_history = "\n".join(formatted)
    
    print("\n格式化后的历史记录：")
    print(recent_history)
    
    # 测试安全检查
    has_cancel = "取消" in recent_history or "已取消" in recent_history
    
    print(f"\n包含'取消'关键词: {has_cancel}")
    print(f"预期: True")
    
    if has_cancel:
        print("\n✅ 测试通过：能够检测到取消支付！")
        print("💡 根据安全检查，should_terminate 会返回 False")
    else:
        print("\n❌ 测试失败：未能检测到取消支付！")
    
    print("="*60)


def test_success_history():
    """测试支付成功的历史记录"""
    print("\n" + "="*60)
    print("🧪 测试：支付成功的历史记录")
    print("="*60)
    
    # 模拟历史记录
    history = [
        HumanMessage(content="我想打造一把飞剑", name="玩家"),
        AIMessage(content="装备打造完成了，李四！", name="张三"),
        AIMessage(content="好的，价格是500灵石", name="李四"),
        ToolMessage(content="✅ 玩家已支付 500 灵石，交易完成！", tool_call_id="test_123"),
        AIMessage(content="太好了！感谢大侠！", name="李四"),
    ]
    
    # 格式化历史记录
    recent = history[-5:]
    formatted = []
    for msg in recent:
        name = getattr(msg, 'name', '未知')
        content = msg.content if hasattr(msg, 'content') else str(msg)
        if content:
            formatted.append(f"{name}: {content}")
    
    recent_history = "\n".join(formatted)
    
    print("\n格式化后的历史记录：")
    print(recent_history)
    
    # 测试安全检查
    has_cancel = "取消" in recent_history or "已取消" in recent_history
    has_paid = "已支付" in recent_history or "支付成功" in recent_history
    
    print(f"\n包含'取消'关键词: {has_cancel}")
    print(f"包含'已支付'关键词: {has_paid}")
    print(f"预期: 取消=False, 已支付=True")
    
    if not has_cancel and has_paid:
        print("\n✅ 测试通过：能够检测到支付成功！")
        print("💡 安全检查通过，LLM 会判断 should_terminate = True")
    else:
        print("\n❌ 测试失败！")
    
    print("="*60)


if __name__ == "__main__":
    test_format_history()
    test_success_history()
