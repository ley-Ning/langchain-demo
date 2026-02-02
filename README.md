# 多智能体交互 Demo - 修仙游戏铁匠铺

这是一个使用 Python + LangChain 实现的多智能体协作系统，模拟修仙游戏中的铁匠铺场景。

**核心特性：** 完全对应 C# Semantic Kernel 的 AgentGroupChat 实现方式，支持流式输出和 Token 统计。

## ✨ 主要功能

- 🤖 多智能体自动协作（类似 C# Semantic Kernel 的 AgentGroupChat）
- 🎯 自动选择发言者（SelectionStrategy）
- 🛑 自动判断终止（TerminationStrategy）
- 🔧 工具调用（查询材料、价格、收款）
- 💬 流式输出（逐字显示，打字机效果）
- 📊 Token 统计（每次对话 + 总计）
- 🎮 取消支付后继续对话（张三会发飙）

## 场景说明

这是一个修仙游戏中的铁匠铺场景，包含两个 NPC 智能体：

- **张三（铁匠）**: 
  - 性格鲁莽，说话粗鲁
  - 负责查询材料清单
  - 分 3-5 个工序打造装备
  - 通知李四完成并收款
  
- **李四（学徒）**: 
  - 性格顽皮，活泼可爱
  - 协助张三打造装备
  - 查询装备价格
  - 向玩家发起支付请求

## 技术实现

### 对应 C# Semantic Kernel 的实现

本项目完全对应 C# Semantic Kernel 的 AgentGroupChat 实现方式：

| C# Semantic Kernel | Python LangChain | 说明 |
|-------------------|------------------|------|
| `AgentGroupChat` | `AgentGroupChat` | 智能体群聊管理 |
| `SelectionStrategy` | `select_next_speaker()` | 自动选择下一个发言者 |
| `TerminationStrategy` | `should_terminate()` | 自动判断对话终止 |
| `KernelPlugin` | `@tool` 装饰器 | 工具定义 |
| `AgentDefinition` | 系统提示词 | 智能体角色定义 |

### 核心组件

1. **AgentGroupChat** (`src/core/agent_group_chat.py`)
   - 管理多个智能体的群聊
   - 自动选择发言者（SelectionStrategy）
   - 自动判断终止条件（TerminationStrategy）
   - 处理工具调用和结果

2. **智能体定义** (`src/agents/`)
   - 张三智能体：查询材料、打造装备
   - 李四智能体：查询价格、发起支付

3. **工具插件** (`src/plugins/`)
   - 张三工具：查询装备材料清单
   - 李四工具：查询价格、发起支付

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ley-Ning/langchain-demo.git
cd langchain-demo
```

### 2. 安装依赖

```bash
# 推荐使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
```

**Azure OpenAI 配置示例：**

```env
# Azure OpenAI 配置
OPENAI_API_KEY=your_azure_api_key_here
OPENAI_API_BASE=https://your-resource.openai.azure.com/
MODEL_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
TEMPERATURE=0.7
```

**标准 OpenAI 配置示例：**

```env
# 标准 OpenAI 配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4
TEMPERATURE=0.7
```

### 4. 运行项目

#### 🎯 方式 1：AgentGroupChat 方式（推荐）

```bash
python3 main_groupchat.py
```

**特点：**
- ✅ 完全对应 C# Semantic Kernel 的 AgentGroupChat
- ✅ 智能体自动轮流对话
- ✅ 流式输出（逐字显示）
- ✅ Token 统计（每次 + 总计）
- ✅ 支持取消支付后继续对话

**运行效果：**

```
============================================================
🎮 修仙游戏 - 铁匠铺
============================================================
欢迎来到铁匠铺，你想打造什么装备？
============================================================

请选择要打造的装备：
1. 飞剑 - 锋利无比的飞行法宝
2. 护甲 - 坚不可摧的防御装备
3. 法杖 - 增强法力的神秘法器
4. 灵靴 - 轻盈如风的移动装备

👤 请输入选项 (1-4): 1

👤 玩家: 我想打造一把飞剑

============================================================
🏪 铁匠铺开始营业！
============================================================

🔨 张三: [流式输出] 材料清单搞定了！制作飞剑需要...
   💰 Token: 输入=150, 输出=80, 总计=230

🔨 李四: [流式输出] 收到啦，张三大哥！我这就去准备材料...
   💰 Token: 输入=200, 输出=60, 总计=260

... (继续对话)

============================================================
✅ 对话结束
============================================================
📊 总 Token 消耗统计：
   输入 Token: 1500
   输出 Token: 800
   总计 Token: 2300
============================================================
```

#### 🧪 方式 2：演示版本（自动支付）

```bash
python3 demo_final.py
```

**特点：**
- 自动模拟支付流程
- 适合快速演示和测试

#### 📝 方式 3：测试脚本

```bash
# 测试取消支付场景
python3 test_cancel.py

# 测试支付逻辑
python3 test_payment.py

# 测试自动化逻辑（不需要 API）
python3 test_auto.py
```

## 📁 项目结构

```
langchain-demo/
├── main_groupchat.py                # 主程序（AgentGroupChat 方式）⭐
├── demo_final.py                    # 演示程序（自动支付）
├── test_auto.py                     # 自动化测试（不需要 API）
├── test_cancel.py                   # 取消支付测试
├── test_payment.py                  # 支付逻辑测试
├── requirements.txt                 # 依赖包列表
├── .env.example                     # 环境变量示例
├── .gitignore                       # Git 忽略文件
├── README.md                        # 项目说明文档
├── 配置说明.md                       # 详细配置和逻辑说明
└── src/                             # 源代码目录
    ├── __init__.py
    ├── config/                      # 配置层
    │   ├── __init__.py
    │   └── settings.py              # 应用配置（读取 .env）
    ├── plugins/                     # 插件层（工具集）
    │   ├── __init__.py
    │   ├── zhangsan_plugin.py       # 张三的工具（查询材料）
    │   └── lisi_plugin.py           # 李四的工具（查询价格、收款）
    ├── agents/                      # 智能体层
    │   ├── __init__.py
    │   ├── zhangsan_agent.py        # 张三智能体定义
    │   └── lisi_agent.py            # 李四智能体定义
    └── core/                        # 核心业务层
        ├── __init__.py
        ├── agent_group_chat.py      # AgentGroupChat 实现 ⭐
        ├── state.py                 # 状态定义（旧版）
        ├── workflow.py              # 工作流管理（旧版）
        └── chat_manager.py          # 聊天管理器（旧版）
```

## 🏗️ 架构说明

### 分层架构

- **config/**: 配置层，管理所有配置项（从 .env 读取）
- **plugins/**: 插件层，提供各种工具函数（查询材料、价格、收款）
- **agents/**: 智能体层，定义各个智能体的行为和工具
- **core/**: 核心业务层，实现 AgentGroupChat 和多智能体协作逻辑

### 核心文件说明

| 文件 | 说明 | 重要性 |
|------|------|--------|
| `main_groupchat.py` | 主程序入口，AgentGroupChat 方式 | ⭐⭐⭐ |
| `src/core/agent_group_chat.py` | AgentGroupChat 核心实现 | ⭐⭐⭐ |
| `src/agents/zhangsan_agent.py` | 张三智能体定义 | ⭐⭐ |
| `src/agents/lisi_agent.py` | 李四智能体定义 | ⭐⭐ |
| `src/plugins/zhangsan_plugin.py` | 张三的工具集 | ⭐⭐ |
| `src/plugins/lisi_plugin.py` | 李四的工具集 | ⭐⭐ |
| `src/config/settings.py` | 配置管理 | ⭐ |
| `配置说明.md` | 详细的逻辑说明文档 | ⭐ |

## 工作流程

### 完整的多智能体协作流程

1. **玩家输入** - 玩家说明想要打造的装备（例如："我想打造一把飞剑"）

2. **张三工作** - 铁匠张三开始工作：
   - 调用 `get_equipment_materials` 工具查询材料清单
   - 分 3-5 个工序打造装备：
     - 第1步：准备材料和工具
     - 第2步：熔炼材料
     - 第3步：锻打成型
     - 第4步：淬火处理
     - 第5步：打磨抛光
   - 完成后明确告诉李四："装备打造完成了"

3. **李四工作** - 学徒李四接手：
   - 听到张三说"装备打造完成了"
   - 调用 `get_equipment_price` 工具查询价格
   - 告诉张三和玩家价格

4. **收款流程** - 张三确认后：
   - 张三告诉李四："去找玩家收款"
   - 李四调用 `request_payment` 工具发起支付
   - 玩家确认支付，交易完成

5. **自动终止** - 系统通过 TerminationStrategy 判断：
   - 检测到"已支付"或"交易完成"关键词
   - 自动终止对话

### 智能体协作机制

- **SelectionStrategy**: 根据对话上下文，自动选择下一个发言的智能体
- **TerminationStrategy**: 根据业务逻辑（是否完成支付），自动判断对话是否结束
- **工具调用**: 智能体可以调用工具完成具体任务
- **自然对话**: 智能体之间通过自然语言协作，无需硬编码流程

## 技术特点

### 1. AgentGroupChat 实现

完全对应 C# Semantic Kernel 的实现方式：

```python
# 创建智能体群聊
chat = AgentGroupChat(
    agents={"张三": zhangsan_data, "李四": lisi_data},
    llm=llm,
    max_rounds=20
)

# 添加用户消息
chat.add_user_message("我想打造一把飞剑")

# 运行群聊（自动选择发言者、自动终止）
for response in chat.run():
    print(f"{response.name}: {response.content}")
```

### 2. SelectionStrategy（发言者选择策略）

通过 LLM 分析对话历史，智能选择下一个发言者：

```python
def select_next_speaker(self) -> str:
    """根据对话上下文，选择下一个发言的智能体"""
    # 使用 LLM 分析最近的对话历史
    # 返回最合适的下一个发言者
```

### 3. TerminationStrategy（终止策略）

通过 LLM 判断业务逻辑是否完成：

```python
def should_terminate(self) -> bool:
    """判断对话是否应该终止"""
    # 使用 LLM 分析对话历史
    # 判断是否完成支付（业务逻辑）
```

### 4. 工具调用

智能体可以调用工具完成具体任务：

```python
@tool
def get_equipment_materials(equipment_name: str) -> str:
    """查询装备材料清单"""
    return ZhangSanPlugin.get_equipment_materials(equipment_name)
```

### 5. 流式输出和 Token 统计

每次对话都会：
- 逐字显示响应内容（打字机效果）
- 显示本次消耗的 Token（输入、输出、总计）
- 最后显示总 Token 统计

```python
for response, token_usage in chat.run():
    # 流式输出
    print_stream(response.content, delay=0.015)
    
    # 显示 Token
    print(f"💰 Token: 输入={token_usage['prompt_tokens']}, "
          f"输出={token_usage['completion_tokens']}, "
          f"总计={token_usage['total_tokens']}")
```

### 6. 支持 Azure OpenAI

自动检测并支持 Azure OpenAI 配置：

```python
llm = AzureChatOpenAI(
    azure_deployment=settings.MODEL_NAME,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    api_key=settings.OPENAI_API_KEY,
    azure_endpoint=settings.OPENAI_API_BASE
)
```

## ❓ 常见问题

### Q1: 如何调整流式输出速度？

修改 `main_groupchat.py` 中的 `delay` 参数：

```python
print_stream(response.content, delay=0.01)  # 更快
print_stream(response.content, delay=0.03)  # 更慢
```

### Q2: 取消支付后会怎样？

- 李四会劝说玩家
- 张三会发飙骂人（性格粗鲁暴躁）
- 对话继续，不会结束
- 直到玩家支付或达到最大轮数

### Q3: 如何查看详细的逻辑说明？

查看 `配置说明.md` 文件，里面有详细的：
- 程序流程图
- 核心逻辑解释
- `self` 的含义
- LangChain 使用说明

### Q4: 为什么不用 LangGraph？

LangGraph 需要手动编排流程（硬编码），而我们的实现是让 AI 动态决策（灵活）：

- ❌ LangGraph: 固定流程（张三 → 李四 → 张三 → 李四）
- ✅ 我们的方式: AI 根据上下文动态选择（张三 → 张三 → 李四 → 张三 → 李四 → 李四）

详见 `配置说明.md` 中的对比说明。

## 📚 相关文档

- [配置说明.md](./配置说明.md) - 详细的程序逻辑和配置说明
- [.env.example](./.env.example) - 环境变量配置示例

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

ley-Ning

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
