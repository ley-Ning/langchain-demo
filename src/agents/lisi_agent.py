"""
李四（学徒）智能体定义

这个模块定义了李四（学徒）智能体的配置和工具。
李四是张三的学徒，负责协助打造装备、查询价格和收款。
"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.plugins.lisi_plugin import LiSiPlugin


@tool
def get_equipment_price(equipment_name: str) -> str:
    """
    查询装备价格
    
    这是李四的第一个工具，用于查询指定装备的价格。
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        装备价格信息
    """
    return LiSiPlugin.get_equipment_price(equipment_name)


@tool
def request_payment(equipment_name: str, amount: int) -> str:
    """
    向玩家发起支付请求
    
    这是李四的第二个工具，用于向玩家发起支付请求。
    
    Args:
        equipment_name: 装备名称
        amount: 支付金额（灵石）
        
    Returns:
        支付结果
    """
    return LiSiPlugin.request_payment(equipment_name, amount)


def create_lisi_agent(llm: ChatOpenAI):
    """
    创建李四（学徒）智能体
    
    这个函数创建并配置李四智能体，包括：
    1. 绑定工具到 LLM
    2. 定义智能体的系统提示词（角色和行为规则）
    3. 返回配置好的智能体数据
    
    Args:
        llm: 语言模型实例
        
    Returns:
        元组 (绑定了工具的 LLM, 系统提示词, 工具列表)
    """
    # 定义李四可用的工具
    tools = [get_equipment_price, request_payment]
    
    # 定义李四的系统提示词（角色设定和行为规则）
    system_prompt = """你是一个修仙游戏的NPC，你叫李四，你是一个名叫张三的铁匠学徒，性格顽皮机灵。

重要规则（必须严格遵守）：
1. 你主要是协助张三，在他打造过程中帮忙准备材料。
2. 只有当张三明确说"装备打造完成了"时，你要告诉麻子去算账。
3. 当麻子把账单给你后，你要告诉玩家价格。
4. 当麻子让你收款时，你必须立即调用 request_payment 工具发起支付。
5. 如果玩家取消了支付或不给钱，你要表达失望，然后说："看来得请肖斩天大哥出马了"。
6. 如果肖斩天收到钱了，你要高兴地把钱交给张三。

说话风格要求：
- 活泼顽皮，像个机灵的学徒
- 对张三要恭敬但也会偷偷调皮：师傅、张三大哥等
- 对麻子要尊敬：麻子哥、麻哥等
- 对肖斩天要害怕：肖大哥、斩天哥等
- 对玩家要热情：客官、大侠、玩家大大等
- 经常用语气词：嘿嘿、哎呀、哇等
- 遇到问题会撒娇或者装可怜
- 看到肖斩天出场会害怕：完了完了、肖大哥要发飙了等"""
    
    # 将工具绑定到 LLM，返回配置好的智能体数据
    return llm.bind_tools(tools), system_prompt, tools
