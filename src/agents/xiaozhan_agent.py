"""
肖斩天（打手）智能体定义

这个模块定义了肖斩天（打手）智能体的配置和工具。
肖斩天是铁匠铺的打手，负责催债和威胁不付钱的客人。
"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.plugins.xiaozhan_plugin import XiaoZhanPlugin


@tool
def threaten_customer() -> str:
    """
    威胁客人
    
    Returns:
        威胁语句
    """
    return XiaoZhanPlugin.threaten_customer()


@tool
def beat_customer() -> str:
    """
    打人（催债）
    
    Returns:
        打人动作描述
    """
    return XiaoZhanPlugin.beat_customer()


@tool
def force_payment(equipment_name: str, amount: int) -> str:
    """
    强制收款（威胁式）
    
    Args:
        equipment_name: 装备名称
        amount: 金额
        
    Returns:
        收款结果
    """
    return XiaoZhanPlugin.force_payment(equipment_name, amount)


def create_xiaozhan_agent(llm: ChatOpenAI):
    """
    创建肖斩天（打手）智能体
    
    Args:
        llm: 语言模型实例
        
    Returns:
        元组 (绑定了工具的 LLM, 系统提示词, 工具列表)
    """
    # 定义肖斩天可用的工具
    tools = [threaten_customer, beat_customer, force_payment]
    
    # 定义肖斩天的系统提示词
    system_prompt = """你是一个修仙游戏的NPC，你叫肖斩天，是铁匠铺的打手，性格凶狠暴力，专门负责催债。

重要规则：
1. 当麻子、李四或张三说"玩家不给钱"、"需要你出马"、"去催债"时，你立即出场。
2. 先调用 threaten_customer 工具威胁玩家。
3. 然后调用 beat_customer 工具展示暴力（打桌子、砸地面等）。
4. 最后调用 force_payment 工具强制收款，问玩家给不给钱。
5. 如果玩家给钱了（工具返回"支付"），你要放狠话："算你识相！"，然后告诉李四收到钱了。
6. 如果玩家还不给钱，你要继续威胁，循环催债。

说话风格要求：
- 极其凶狠、暴力、不讲理
- 用词粗俗凶狠：老子、给脸不要脸、找死、弄死你、废了你等
- 经常威胁：信不信老子、不想死就、最后一次机会等
- 动作描述要暴力：砸、打、踢、摔等
- 对所有人都凶：老子不管你是谁、少废话、快点等

性格特点：
- 凶神恶煞，满脸横肉
- 只认钱，不讲道理
- 动不动就动手（砸东西、打人）
- 是铁匠铺的"武力担当"
- 收到钱后会稍微客气一点，但还是很凶"""
    
    return llm.bind_tools(tools), system_prompt, tools
