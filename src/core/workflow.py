"""工作流管理"""
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.core.state import AgentState
from src.config.settings import settings


class AgentWorkflow:
    """智能体工作流"""
    
    def __init__(self, zhangsan_data, lisi_data):
        """
        初始化工作流
        
        Args:
            zhangsan_data: 张三智能体数据 (llm, system_prompt, tools)
            lisi_data: 李四智能体数据 (llm, system_prompt, tools)
        """
        self.zhangsan_llm, self.zhangsan_prompt, self.zhangsan_tools = zhangsan_data
        self.lisi_llm, self.lisi_prompt, self.lisi_tools = lisi_data
        
        # 创建工具节点
        self.zhangsan_tool_node = ToolNode(self.zhangsan_tools)
        self.lisi_tool_node = ToolNode(self.lisi_tools)
        
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """创建智能体工作流"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("zhangsan", self._zhangsan_node)
        workflow.add_node("zhangsan_tools", self.zhangsan_tool_node)
        workflow.add_node("lisi", self._lisi_node)
        workflow.add_node("lisi_tools", self.lisi_tool_node)
        workflow.add_node("terminator", self._terminator_node)
        
        # 设置入口
        workflow.set_entry_point("zhangsan")
        
        # 添加条件边
        workflow.add_conditional_edges(
            "zhangsan",
            self._should_use_zhangsan_tools,
            {
                "tools": "zhangsan_tools",
                "continue": "terminator"
            }
        )
        
        workflow.add_conditional_edges(
            "lisi",
            self._should_use_lisi_tools,
            {
                "tools": "lisi_tools",
                "continue": "terminator"
            }
        )
        
        # 工具执行后返回对应的智能体
        workflow.add_edge("zhangsan_tools", "zhangsan")
        workflow.add_edge("lisi_tools", "lisi")
        
        # 终止器的条件边
        workflow.add_conditional_edges(
            "terminator",
            self._should_continue,
            {
                "zhangsan": "zhangsan",
                "lisi": "lisi",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _zhangsan_node(self, state: AgentState) -> AgentState:
        """张三节点"""
        messages = state["messages"]
        
        # 智能过滤消息：保留完整的工具调用对（AI消息+工具消息）
        filtered_messages = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            msg_type = getattr(msg, 'type', None)
            
            # 如果是 AI 消息且有 tool_calls
            if msg_type == 'ai' and hasattr(msg, 'tool_calls') and msg.tool_calls:
                # 保留这条 AI 消息
                filtered_messages.append(msg)
                # 查找并保留紧跟的工具消息
                if i + 1 < len(messages) and getattr(messages[i + 1], 'type', None) == 'tool':
                    filtered_messages.append(messages[i + 1])
                    i += 2
                    continue
            # 如果是普通消息（human, ai without tool_calls）
            elif msg_type in ['human', 'ai', 'system']:
                # 如果是 AI 消息但没有 tool_calls，只保留内容不为空的
                if msg_type == 'ai':
                    if msg.content:
                        filtered_messages.append(msg)
                else:
                    filtered_messages.append(msg)
            # 跳过孤立的工具消息
            
            i += 1
        
        # 添加系统提示
        messages_with_system = [SystemMessage(content=self.zhangsan_prompt)] + filtered_messages
        
        # 调用 LLM
        response = self.zhangsan_llm.invoke(messages_with_system)
        response.name = "张三"
        
        return {
            "messages": messages + [response],
            "next_agent": "lisi",
            "equipment_name": state.get("equipment_name", ""),
            "is_completed": state.get("is_completed", False)
        }
    
    def _lisi_node(self, state: AgentState) -> AgentState:
        """李四节点"""
        messages = state["messages"]
        
        # 智能过滤消息：保留完整的工具调用对（AI消息+工具消息）
        filtered_messages = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            msg_type = getattr(msg, 'type', None)
            
            # 如果是 AI 消息且有 tool_calls
            if msg_type == 'ai' and hasattr(msg, 'tool_calls') and msg.tool_calls:
                # 保留这条 AI 消息
                filtered_messages.append(msg)
                # 查找并保留紧跟的工具消息
                if i + 1 < len(messages) and getattr(messages[i + 1], 'type', None) == 'tool':
                    filtered_messages.append(messages[i + 1])
                    i += 2
                    continue
            # 如果是普通消息（human, ai without tool_calls）
            elif msg_type in ['human', 'ai', 'system']:
                # 如果是 AI 消息但没有 tool_calls，只保留内容不为空的
                if msg_type == 'ai':
                    if msg.content:
                        filtered_messages.append(msg)
                else:
                    filtered_messages.append(msg)
            # 跳过孤立的工具消息
            
            i += 1
        
        # 添加系统提示
        messages_with_system = [SystemMessage(content=self.lisi_prompt)] + filtered_messages
        
        # 调用 LLM
        response = self.lisi_llm.invoke(messages_with_system)
        response.name = "李四"
        
        return {
            "messages": messages + [response],
            "next_agent": "zhangsan",
            "equipment_name": state.get("equipment_name", ""),
            "is_completed": state.get("is_completed", False)
        }
    
    def _should_use_zhangsan_tools(self, state: AgentState) -> str:
        """判断张三是否需要使用工具"""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return "continue"
    
    def _should_use_lisi_tools(self, state: AgentState) -> str:
        """判断李四是否需要使用工具"""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return "continue"
    
    def _terminator_node(self, state: AgentState) -> AgentState:
        """终止器节点：判断对话是否应该结束"""
        messages = state["messages"]
        
        # 检查最近的消息中是否包含支付完成的标志
        recent_messages = messages[-5:] if len(messages) >= 5 else messages
        
        for msg in recent_messages:
            content = msg.content if hasattr(msg, 'content') else str(msg)
            if "已支付" in content or "交易完成" in content:
                state["is_completed"] = True
                return state
            elif "取消了支付" in content:
                state["is_completed"] = True
                return state
        
        # 限制最大轮次（降低到15轮，避免无限循环）
        if len(messages) > 15:
            state["is_completed"] = True
        
        return state
    
    def _should_continue(self, state: AgentState) -> str:
        """判断是否继续对话"""
        if state.get("is_completed", False):
            return "end"
        
        # 根据最后一条消息的发送者决定下一个发言者
        messages = state["messages"]
        if len(messages) > 0:
            last_message = messages[-1]
            if hasattr(last_message, 'name'):
                if last_message.name == "张三":
                    return "lisi"
                elif last_message.name == "李四":
                    return "zhangsan"
        
        return state.get("next_agent", "zhangsan")
    
    def stream(self, initial_state: AgentState):
        """
        流式执行工作流
        
        Args:
            initial_state: 初始状态
            
        Yields:
            工作流状态
        """
        return self.workflow.stream(initial_state)
