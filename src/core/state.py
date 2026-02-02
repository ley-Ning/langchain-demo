"""智能体状态定义"""
from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    智能体状态
    
    Attributes:
        messages: 消息历史
        next_agent: 下一个发言的智能体
        equipment_name: 装备名称
        is_completed: 是否完成对话
    """
    messages: Sequence[BaseMessage]
    next_agent: str
    equipment_name: str
    is_completed: bool
