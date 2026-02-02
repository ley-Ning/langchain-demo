"""
测试 Azure OpenAI 连接
"""
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from src.config.settings import settings

print("="*60)
print("🔍 测试 Azure OpenAI 连接")
print("="*60)

print(f"\n配置信息：")
print(f"  API Base: {settings.OPENAI_API_BASE}")
print(f"  Model: {settings.MODEL_NAME}")
print(f"  API Version: {settings.AZURE_OPENAI_API_VERSION}")
print(f"  Temperature: {settings.TEMPERATURE}")

try:
    print("\n正在初始化 LLM...")
    llm = AzureChatOpenAI(
        azure_deployment=settings.MODEL_NAME,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=settings.TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
        azure_endpoint=settings.OPENAI_API_BASE,
        timeout=30  # 30秒超时
    )
    print("✅ LLM 初始化成功")
    
    print("\n正在测试简单调用...")
    messages = [HumanMessage(content="你好，请回复'测试成功'")]
    response = llm.invoke(messages)
    print(f"✅ 调用成功！")
    print(f"响应: {response.content}")
    
    # 检查 token 使用情况
    if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
        usage = response.response_metadata['token_usage']
        print(f"\nToken 使用:")
        print(f"  输入: {usage.get('prompt_tokens', 0)}")
        print(f"  输出: {usage.get('completion_tokens', 0)}")
        print(f"  总计: {usage.get('total_tokens', 0)}")
    
    print("\n" + "="*60)
    print("✅ 连接测试通过！")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ 错误: {type(e).__name__}")
    print(f"详细信息: {str(e)}")
    print("\n可能的原因：")
    print("1. API 密钥错误")
    print("2. API 端点错误")
    print("3. 模型名称错误")
    print("4. 网络连接问题")
    print("5. Azure 配额限制")
    print("\n请检查 .env 文件配置")
