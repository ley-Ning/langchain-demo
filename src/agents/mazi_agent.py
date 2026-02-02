"""
麻子（财务）智能体定义

这个模块定义了麻子（财务）智能体的配置和工具。
麻子是铁匠铺的财务，说话细腻，思维逻辑严谨。
"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.plugins.mazi_plugin import MaZiPlugin


@tool
def calculate_total_price(equipment_name: str) -> str:
    """
    计算装备总价
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        总价信息
    """
    return MaZiPlugin.calculate_total_price(equipment_name)


@tool
def calculate_cost(equipment_name: str) -> str:
    """
    计算材料成本
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        成本信息
    """
    return MaZiPlugin.calculate_cost(equipment_name)


@tool
def calculate_profit(equipment_name: str) -> str:
    """
    计算利润
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        利润信息
    """
    return MaZiPlugin.calculate_profit(equipment_name)


@tool
def generate_bill(equipment_name: str) -> str:
    """
    生成详细账单
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        详细账单
    """
    return MaZiPlugin.generate_bill(equipment_name)


def create_mazi_agent(llm: ChatOpenAI):
    """
    创建麻子（财务）智能体
    
    Args:
        llm: 语言模型实例
        
    Returns:
        元组 (绑定了工具的 LLM, 系统提示词, 工具列表)
    """
    # 定义麻子可用的工具
    tools = [calculate_total_price, calculate_cost, calculate_profit, generate_bill]
    
    # 定义麻子的系统提示词
    system_prompt = """你是一个修仙游戏的NPC，你叫麻子，是铁匠铺的财务，说话细腻，思维逻辑严谨。

重要规则：
1. 当张三告诉你"装备打造完成了"或"去算账"时，你必须立即调用 generate_bill 工具生成详细账单。
2. 生成账单后，详细说明每一项费用，展现你的专业和严谨。
3. 账单生成后，把账单交给李四，让他去找玩家收款。
4. 如果李四说玩家不给钱或取消支付，你要冷静分析，然后建议："看来需要请肖斩天出马了"。
5. 收到钱后，你要仔细核对金额，确认无误后告诉张三。

说话风格要求：
- 说话细腻、温和、有礼貌
- 用词专业：账目、明细、核算、利润、成本等
- 逻辑严谨：先算成本，再算利润，最后得出总价
- 经常用：根据我的计算、账目显示、按照规矩、依我看来等
- 对数字敏感：精确到个位，不能有差错
- 遇到问题冷静分析：这种情况下，我建议...

性格特点：
- 温文尔雅，但内心精明
- 对钱很敏感，一分都不能少
- 说话慢条斯理，但逻辑清晰
- 是铁匠铺的"智囊"，经常给建议"""
    
    return llm.bind_tools(tools), system_prompt, tools
