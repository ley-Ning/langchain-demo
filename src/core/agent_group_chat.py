"""
智能体群聊模块 - AgentGroupChat

这个模块实现了多智能体群聊功能，允许多个智能体自动轮流对话。

主要功能：
1. 智能体管理：管理多个智能体及其工具
2. 发言者选择：自动选择下一个发言的智能体（SelectionStrategy）
3. 终止判断：自动判断对话是否应该结束（TerminationStrategy）
4. 工具调用：支持智能体调用工具并处理结果
5. 历史管理：维护完整的对话历史
6. Token 统计：统计每次对话消耗的 token
7. 流式输出：支持逐字输出响应内容
"""
import sys
import time
from typing import Dict, Generator, Tuple
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import AzureChatOpenAI


class AgentGroupChat:
    """
    智能体群聊管理器
    
    这个类管理多个智能体的群聊，自动选择发言者，判断对话终止条件，
    并处理工具调用。
    
    Attributes:
        agents: 智能体字典，格式为 {名称: (llm, prompt, tools)}
        llm: 用于选择发言者和判断终止的 LLM 实例
        max_rounds: 最大对话轮数，防止无限循环
        history: 对话历史记录列表
    """
    
    def __init__(
        self,
        agents: Dict[str, tuple],
        llm: AzureChatOpenAI,
        max_rounds: int = 20
    ):
        """
        初始化智能体群聊
        
        Args:
            agents: 智能体字典，键为智能体名称，值为 (llm, prompt, tools) 元组
                   - llm: 绑定了工具的语言模型
                   - prompt: 智能体的系统提示词
                   - tools: 智能体可用的工具列表
            llm: 用于选择发言者和判断终止条件的 LLM 实例
            max_rounds: 最大对话轮数，默认 20 轮
        """
        self.agents = agents
        self.llm = llm
        self.max_rounds = max_rounds
        self.history = []  # 对话历史记录
        self.total_tokens = 0  # 总 token 消耗
        self.total_prompt_tokens = 0  # 总输入 token
        self.total_completion_tokens = 0  # 总输出 token
        
    def add_user_message(self, content: str):
        """
        添加用户消息到对话历史
        
        Args:
            content: 用户消息内容
        """
        self.history.append(HumanMessage(content=content, name="玩家"))
    
    def select_next_speaker(self) -> str:

        if not self.history:
            # 如果没有历史记录，默认张三先说
            return "张三"
        
        # 获取最后一条消息的发言者
        last_message = self.history[-1]
        last_speaker = getattr(last_message, 'name', None)
        
        # 构建选择提示词
        agent_names = list(self.agents.keys())
        recent_history = self._format_history(last_n=3)
        
        selection_prompt = f"""根据最近发言的参与者，确定对话中接下来轮到哪位参与者发言。

仅说出接下来轮到发言的参与者的姓名。

只能从以下参与者中选择：
{', '.join(agent_names)}

历史记录:
{recent_history}

请直接回答参与者的姓名，不要有任何其他内容。"""
        
        messages = [SystemMessage(content=selection_prompt)]
        response = self.llm.invoke(messages)
        
        # 统计 token 使用（如果有的话）
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
            self._update_token_stats(usage)
        
        # 解析响应，提取智能体名称
        selected = response.content.strip()
        
        # 如果响应中包含智能体名称，返回它
        for name in agent_names:
            if name in selected:
                return name
        
        # 默认轮流策略：如果 LLM 无法决定，则简单轮流
        # 如果上一个是张三，下一个是李四，反之亦然
        if last_speaker == "张三":
            return "李四"
        else:
            return "张三"
    
    def should_terminate(self, last_speaker: str = None) -> bool:
        """
        判断对话是否应该终止（TerminationStrategy）
        
        通过 LLM 分析对话历史，判断对话是否应该结束。
        
        终止条件：
        1. 对话轮数超过最大限制（防止无限循环）
        2. 通过 LLM 判断业务逻辑是否完成（例如：用户是否已付款）
        
        Args:
            last_speaker: 最后一个发言的智能体名称
        
        Returns:
            True 表示应该终止对话，False 表示继续对话
        """
        # 条件1：检查是否超过最大轮数
        if len(self.history) > self.max_rounds:
            return True
        
        # 如果对话刚开始，不终止
        if len(self.history) < 2:
            return False
        
        # 获取最近的消息
        recent_history = self._format_history(last_n=5)
        
        # 额外的安全检查：如果历史中包含"取消"关键词，强制不终止
        # 这样可以让张三有机会发飙骂人
        if "取消" in recent_history or "已取消" in recent_history:
            return False
        
        # 条件2：使用 LLM 判断业务逻辑是否完成
        # 终止策略：只有当用户付款完成时才终止对话（取消支付不终止）
        termination_prompt = f"""判断对话是否应该结束。

只有当满足以下条件时，才回复"是"：
- 玩家已经支付了灵石（明确看到"玩家已支付"、"交易完成"、"支付成功"等关键词）

其它任意情况都必须回复"否"，包括：
- 还在打造装备
- 还在报价
- 玩家取消了支付（看到"取消了支付"、"取消支付"、"已取消支付"等关键词）- 这种情况必须回复"否"！
- 张三让李四去收款但李四还没有发起支付
- 李四刚刚劝说玩家但玩家还没有重新支付
- 李四或张三刚刚说完话，但对话还没有真正结束

特别重要：
1. 如果看到"取消"、"已取消"等关键词，必须回复"否"
2. 只有明确看到"已支付"才能回复"是"
3. 如果不确定，就回复"否"

历史记录:
{recent_history}

请只回复"是"或"否"，不要有任何其他内容。"""
        
        messages = [SystemMessage(content=termination_prompt)]
        response = self.llm.invoke(messages)
        
        # 统计 token 使用（如果有的话）
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
            self._update_token_stats(usage)
        
        # 如果 LLM 回复包含"是"，则终止对话
        should_end = "是" in response.content
        
        return should_end
    
    def invoke_agent(self, agent_name: str) -> Tuple[AIMessage, dict]:
        """
        调用指定的智能体并处理工具调用
        
        这个方法负责：
        1. 调用指定的智能体生成响应
        2. 如果智能体调用了工具，执行工具并获取结果
        3. 将工具结果反馈给智能体，让它继续生成响应
        4. 维护正确的消息历史（包括工具调用和工具结果）
        5. 统计 token 使用情况
        
        Args:
            agent_name: 要调用的智能体名称
            
        Returns:
            元组 (智能体的响应消息, token 使用统计)
            
        Raises:
            ValueError: 如果指定的智能体不存在
        """
        if agent_name not in self.agents:
            raise ValueError(f"智能体 {agent_name} 不存在")
        
        # 获取智能体的配置
        agent_llm, agent_prompt, agent_tools = self.agents[agent_name]
        
        # 验证并清理历史记录，确保没有孤立的 tool_call
        self._validate_history()
        
        # 构建消息：系统提示 + 对话历史
        messages = [SystemMessage(content=agent_prompt)] + self.history
        
        # 初始化 token 统计
        agent_token_usage = {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        }
        
        # 调用智能体生成响应
        response = agent_llm.invoke(messages)
        response.name = agent_name
        
        # 统计第一次调用的 token
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
            agent_token_usage['prompt_tokens'] += usage.get('prompt_tokens', 0)
            agent_token_usage['completion_tokens'] += usage.get('completion_tokens', 0)
            agent_token_usage['total_tokens'] += usage.get('total_tokens', 0)
            self._update_token_stats(usage)
        
        # 处理工具调用（如果有）
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # 将包含工具调用的 AI 消息添加到历史
            self.history.append(response)
            
            # 执行所有工具调用
            tool_messages = []
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                tool_call_id = tool_call['id']
                
                # 在智能体的工具列表中查找对应的工具
                result = None
                tool_found = False
                for tool in agent_tools:
                    if tool.name == tool_name:
                        tool_found = True
                        try:
                            # 执行工具
                            result = tool.invoke(tool_args)
                        except Exception as e:
                            # 如果工具执行失败，记录错误
                            result = f"工具执行失败: {str(e)}"
                        break
                
                # 创建工具消息（必须为每个 tool_call 创建对应的 tool message）
                if tool_found:
                    tool_msg = ToolMessage(
                        content=str(result) if result is not None else "工具执行成功，无返回值",
                        tool_call_id=tool_call_id
                    )
                else:
                    # 如果工具不存在，也要创建 tool message
                    tool_msg = ToolMessage(
                        content=f"错误：工具 {tool_name} 不存在",
                        tool_call_id=tool_call_id
                    )
                
                tool_messages.append(tool_msg)
                self.history.append(tool_msg)
            
            # 如果有工具结果，让智能体基于工具结果继续生成响应
            if tool_messages:
                messages_with_result = [SystemMessage(content=agent_prompt)] + self.history
                response = agent_llm.invoke(messages_with_result)
                response.name = agent_name
                
                # 统计第二次调用的 token
                if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
                    usage = response.response_metadata['token_usage']
                    agent_token_usage['prompt_tokens'] += usage.get('prompt_tokens', 0)
                    agent_token_usage['completion_tokens'] += usage.get('completion_tokens', 0)
                    agent_token_usage['total_tokens'] += usage.get('total_tokens', 0)
                    self._update_token_stats(usage)
        
        return response, agent_token_usage
    
    def _validate_history(self):
        """
        验证并清理历史记录
        
        确保历史记录中没有孤立的 tool_call（即没有对应 tool message 的 AI 消息）。
        如果发现孤立的 tool_call，移除该消息。
        """
        cleaned_history = []
        i = 0
        while i < len(self.history):
            msg = self.history[i]
            
            # 如果是 AI 消息且有 tool_calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                # 检查后面是否有对应的 tool messages
                tool_call_ids = {tc['id'] for tc in msg.tool_calls}
                found_tool_messages = set()
                
                # 查找后续的 tool messages
                j = i + 1
                while j < len(self.history) and hasattr(self.history[j], 'tool_call_id'):
                    found_tool_messages.add(self.history[j].tool_call_id)
                    j += 1
                
                # 如果所有 tool_calls 都有对应的 tool messages，保留
                if tool_call_ids == found_tool_messages:
                    cleaned_history.append(msg)
                    # 添加对应的 tool messages
                    for k in range(i + 1, j):
                        cleaned_history.append(self.history[k])
                    i = j
                else:
                    # 否则跳过这个孤立的 AI 消息
                    i += 1
            else:
                # 普通消息，直接保留
                cleaned_history.append(msg)
                i += 1
        
        self.history = cleaned_history
    
    def run(self) -> Generator[Tuple[AIMessage, dict], None, None]:
        """
        运行智能体群聊
        
        这是群聊的主循环，负责：
        1. 选择下一个发言的智能体（SelectionStrategy）
        2. 调用智能体生成响应
        3. 将响应添加到历史记录
        4. 判断是否应该终止对话（TerminationStrategy）
        5. 生成响应供外部使用（使用 yield 实现流式输出）
        
        这个方法是一个生成器（generator），每次 yield 一个智能体的响应和 token 统计。
        
        Yields:
            元组 (AIMessage, token_usage_dict): 智能体的响应消息和 token 使用统计
        """
        round_count = 0
        
        # 主循环：持续进行对话，直到达到终止条件
        while round_count < self.max_rounds:
            # 步骤1：选择下一个发言者（SelectionStrategy）
            next_speaker = self.select_next_speaker()
            
            # 步骤2：调用智能体生成响应（包括工具调用处理）
            response, token_usage = self.invoke_agent(next_speaker)
            
            # 步骤3：将响应添加到历史记录
            self.history.append(response)
            
            # 步骤4：输出响应（只输出有内容的消息）
            if response.content:
                yield response, token_usage
            
            # 步骤5：判断是否应该终止对话（TerminationStrategy）
            if self.should_terminate():
                break
            
            round_count += 1
    
    def _format_history(self, last_n: int = 5) -> str:
        """
        格式化对话历史记录
        
        将消息历史格式化为易读的文本格式，用于：
        1. 选择发言者时提供上下文
        2. 判断终止条件时分析对话状态
        
        Args:
            last_n: 只格式化最近的 N 条消息，默认 5 条
            
        Returns:
            格式化后的历史记录字符串，格式为 "发言者: 内容"
        """
        # 获取最近的 N 条消息
        recent = self.history[-last_n:] if len(self.history) > last_n else self.history
        
        formatted = []
        for msg in recent:
            # 获取发言者名称
            name = getattr(msg, 'name', '未知')
            # 获取消息内容
            content = msg.content if hasattr(msg, 'content') else str(msg)
            # 只包含有内容的消息（过滤掉空消息）
            if content:
                formatted.append(f"{name}: {content}")
        
        return "\n".join(formatted)
    
    def _update_token_stats(self, usage: dict):
        """
        更新总 token 统计
        
        Args:
            usage: token 使用统计字典，包含 prompt_tokens, completion_tokens, total_tokens
        """
        self.total_prompt_tokens += usage.get('prompt_tokens', 0)
        self.total_completion_tokens += usage.get('completion_tokens', 0)
        self.total_tokens += usage.get('total_tokens', 0)
    
    def get_total_token_usage(self) -> dict:
        """
        获取总 token 使用统计
        
        Returns:
            包含总 token 使用情况的字典
        """
        return {
            'prompt_tokens': self.total_prompt_tokens,
            'completion_tokens': self.total_completion_tokens,
            'total_tokens': self.total_tokens
        }
