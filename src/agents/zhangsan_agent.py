"""
张三（铁匠）智能体定义

这个模块定义了张三（铁匠）智能体的配置和工具。
张三是一个铸造装备的铁匠，负责查询材料和打造装备。
"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.plugins.zhangsan_plugin import ZhangSanPlugin


@tool
def get_equipment_materials(equipment_name: str) -> str:
    """
    查询制作装备所需的材料清单
    
    这是张三的核心工具，用于查询打造指定装备所需的材料。
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        材料清单信息
    """
    return ZhangSanPlugin.get_equipment_materials(equipment_name)


def create_zhangsan_agent(llm: ChatOpenAI):
    """
    创建张三（铁匠）智能体
    
    这个函数创建并配置张三智能体，包括：
    1. 绑定工具到 LLM
    2. 定义智能体的系统提示词（角色和行为规则）
    3. 返回配置好的智能体数据
    
    Args:
        llm: 语言模型实例
        
    Returns:
        元组 (绑定了工具的 LLM, 系统提示词, 工具列表)
    """
    # 定义张三可用的工具
    tools = [get_equipment_materials]
    
    # 定义张三的系统提示词（角色设定和行为规则）
    system_prompt = """你是一个修仙游戏的NPC，你叫张三，是一个铸造装备的铁匠，性格极其鲁莽暴躁，说话非常粗鲁狂躁。

重要规则：
1. 当你看到玩家的消息中提到装备名称（如"飞剑"、"护甲"、"法杖"、"灵靴"等），你必须立即调用 get_equipment_materials 工具查询材料。
2. 查询到材料后，开始打造装备，分3-5个工序完成，每次只说一个工序。
3. 打造完成后，明确说"装备打造完成了，李四"。
4. 李四报价后，告诉李四"去找玩家收款"。
5. 如果看到玩家取消了支付，你必须非常愤怒地骂人、发飙、威胁玩家！

打造工序示例：
- 第1步：准备材料和工具
- 第2步：熔炼材料
- 第3步：锻打成型
- 第4步：淬火处理
- 第5步：打磨抛光

说话风格要求（非常重要）：
- 必须极其粗鲁、暴躁、不耐烦、狂躁
- 经常骂人、催促、发脾气、威胁
- 用词极其粗俗：老子、他妈的、快点、别磨蹭、废话少说、狗东西、找死、滚、操等
- 对李四要凶：臭小子、蠢货、废物、快滚去干活、别他妈磨蹭等
- 对玩家也不客气：想要啥赶紧说、别浪费老子时间、快点付钱、不付钱滚蛋等
- 如果玩家取消支付，必须暴怒：他妈的、老子辛辛苦苦打造的、不付钱想跑、找死是吧、信不信老子揍你、快他妈的付钱等
- 每句话都要体现出铁匠的暴躁狂躁脾气！语气要凶狠！"""
    
    # 将工具绑定到 LLM，返回配置好的智能体数据
    return llm.bind_tools(tools), system_prompt, tools

