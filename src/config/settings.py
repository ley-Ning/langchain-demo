"""
配置管理模块

这个模块负责管理应用的所有配置项，包括：
1. OpenAI API 配置
2. Azure OpenAI 配置
3. 模型参数配置
4. 对话限制配置

配置通过环境变量（.env 文件）加载。
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings:
    """
    应用配置类
    
    这个类集中管理所有配置项，从环境变量中读取配置。
    支持标准 OpenAI API 和 Azure OpenAI 两种配置方式。
    """
    
    # ========== OpenAI 配置 ==========
    # 标准 OpenAI API 的配置项
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    # ========== Azure OpenAI 配置 ==========
    # Azure OpenAI 的配置项（如果使用 Azure）
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    # ========== 模型参数 ==========
    # 控制模型生成的随机性，0-1 之间，越高越随机
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # ========== 对话限制 ==========
    # 最大对话轮数，防止无限循环
    MAX_CONVERSATION_ROUNDS: int = int(os.getenv("MAX_CONVERSATION_ROUNDS", "20"))
    # 历史记录截断大小，用于 SelectionStrategy 和 TerminationStrategy
    HISTORY_TRUNCATION_SIZE: int = int(os.getenv("HISTORY_TRUNCATION_SIZE", "3"))
    
    @property
    def is_azure(self) -> bool:
        """
        判断是否使用 Azure OpenAI
        
        通过检查配置项来判断是否使用 Azure OpenAI：
        1. 如果设置了 AZURE_OPENAI_ENDPOINT，则使用 Azure
        2. 如果 OPENAI_API_BASE 包含 "azure"，则使用 Azure
        
        Returns:
            True 表示使用 Azure OpenAI，False 表示使用标准 OpenAI
        """
        return bool(self.AZURE_OPENAI_ENDPOINT or "azure" in self.OPENAI_API_BASE.lower())


# 创建全局配置实例
settings = Settings()

