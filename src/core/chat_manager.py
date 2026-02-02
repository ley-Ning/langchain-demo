"""聊天管理器"""
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, AzureChatOpenAI

from src.agents.zhangsan_agent import create_zhangsan_agent
from src.agents.lisi_agent import create_lisi_agent
from src.core.workflow import AgentWorkflow
from src.config.settings import settings


class MultiAgentChatManager:
    """多智能体聊天管理器"""
    
    def __init__(self):
        """初始化聊天管理器"""
        # 初始化 LLM
        self.llm = AzureChatOpenAI(
            azure_deployment=settings.MODEL_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
            azure_endpoint=settings.OPENAI_API_BASE
        )

        # 创建智能体
        zhangsan_data = create_zhangsan_agent(self.llm)
        lisi_data = create_lisi_agent(self.llm)
        
        # 创建工作流
        self.workflow = AgentWorkflow(zhangsan_data, lisi_data)
    
    def run(self, user_input: str):
        """
        运行多智能体对话
        
        Args:
            user_input: 用户输入
        """
        initial_state = {
            "messages": [HumanMessage(content=user_input, name="玩家")],
            "next_agent": "zhangsan",
            "equipment_name": "",
            "is_completed": False
        }
        
        self._print_header(user_input)
        
        for state in self.workflow.stream(initial_state):
            for node_name, node_state in state.items():
                if node_name in ["zhangsan", "lisi"]:
                    self._print_agent_message(node_state)
        
        self._print_footer()
    
    @staticmethod
    def _print_header(user_input: str):
        """打印对话头部"""
        print("\n" + "="*60)
        print("🏪 欢迎来到铁匠铺！")
        print("="*60)
        print(f"👤 玩家: {user_input}\n")
    
    @staticmethod
    def _print_agent_message(node_state):
        """打印智能体消息"""
        last_message = node_state["messages"][-1]
        agent_name = last_message.name if hasattr(last_message, 'name') else "未知"
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # 只打印非工具调用的消息
        if content and not (hasattr(last_message, 'tool_calls') and last_message.tool_calls):
            print(f"🔨 {agent_name}: {content}\n")
    
    @staticmethod
    def _print_footer():
        """打印对话尾部"""
        print("="*60)
        print("✅ 对话结束")
        print("="*60)
