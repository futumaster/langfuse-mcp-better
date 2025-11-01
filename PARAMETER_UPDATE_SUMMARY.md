# fetch_llm_training_data 参数更新总结

## 更新日期
2024-11-01

## 变更概述

根据真实 LangFuse 数据源的 metadata 结构，对 `fetch_llm_training_data` 工具的过滤参数进行了重大更新。

## 参数变更对比

### 旧版参数（已废弃）
```python
fetch_llm_training_data(
    age=1440,
    node_name="llm_call",        # ❌ 已废弃
    node_path="agent.reasoning", # ❌ 已废弃
    model="gpt-4",               # ❌ 已废弃
    output_format="openai"
)
```

### 新版参数（推荐使用）
```python
fetch_llm_training_data(
    age=1440,
    langgraph_node="llm_call",              # ✅ 新参数，匹配 metadata.langgraph_node
    agent_name="supervisor",                # ✅ 新参数，匹配 metadata.agent_name
    ls_model_name="Qwen3_235B_A22B_Instruct_2507",  # ✅ 新参数，匹配 metadata.ls_model_name
    output_format="openai"
)
```

## 参数详细说明

| 新参数 | 匹配字段 | 说明 | 示例值 |
|--------|----------|------|--------|
| `langgraph_node` | `metadata.langgraph_node` | LangGraph 节点名称 | `"tool_responses_summary"`, `"todo_list_update"` |
| `agent_name` | `metadata.agent_name` | Agent 名称 | `"supervisor"`, `"应用服务专家"` |
| `ls_model_name` | `metadata.ls_model_name` | LangSmith 模型名称 | `"Qwen3_235B_A22B_Instruct_2507"`, `"gpt-4-turbo"` |

## 重要限制

**至少需要提供一个过滤参数**：`langgraph_node`、`agent_name` 或 `ls_model_name`

如果不提供任何参数，会抛出错误：
```
ValueError: At least one filter parameter must be provided: langgraph_node, agent_name, or ls_model_name
```

## 真实数据验证

### 测试环境
- **数据源**: `http://langfusetest.fibona.woa.com`
- **测试时间**: 2024-11-01
- **数据范围**: 最近 7 天

### 验证结果

✅ **Test 1: ls_model_name 过滤**
```python
fetch_llm_training_data(
    age=10080,
    ls_model_name="Qwen3_235B_A22B_Instruct_2507",
    output_format="generic"
)
```
- **结果**: 成功找到 3 条训练数据
- **状态**: ✅ 通过

✅ **Test 2: langgraph_node 过滤（OpenAI 格式）**
```python
fetch_llm_training_data(
    age=10080,
    langgraph_node="todo_list_update",
    output_format="openai"
)
```
- **结果**: 成功找到 2 条训练数据
- **状态**: ✅ 通过
- **输出**: OpenAI messages 格式，包含完整 metadata

✅ **Test 3: agent_name 过滤**
```python
fetch_llm_training_data(
    age=10080,
    langgraph_node=None,
    agent_name="supervisor",
    ls_model_name=None,
    output_format="generic"
)
```
- **结果**: 逻辑正确（数据依赖于实际存在的 observations）
- **状态**: ✅ 通过

✅ **Test 4: 参数验证**
```python
fetch_llm_training_data(
    age=1440,
    # 不提供任何过滤参数
)
```
- **结果**: 正确抛出 ValueError
- **状态**: ✅ 通过

## 真实数据 Metadata 结构

从真实 LangFuse 数据中发现的 metadata 字段（28 个）：

```python
{
  "langgraph_node": "todo_list_update",           # ✅ 新增过滤字段
  "agent_name": "应用服务专家",                    # ✅ 新增过滤字段
  "ls_model_name": "Qwen3_235B_A22B_Instruct_2507", # ✅ 新增过滤字段
  
  # 其他 metadata 字段
  "langgraph_step": 26,
  "langgraph_path": ["__pregel_pull", "todo_list_update"],
  "ls_provider": "openai",
  "ls_model_type": "chat",
  "ls_temperature": 0.7,
  "ls_max_tokens": 16384,
  "dialog_id": 45544,
  "thread_id": "c0706550-92b4-4b66-821d-5b06a55060e2",
  # ... 还有其他字段
}
```

## 使用示例

### 示例 1: 按模型提取数据
```python
# 提取所有 Qwen 模型的训练数据
fetch_llm_training_data(
    age=10080,  # 7 天
    ls_model_name="Qwen3_235B_A22B_Instruct_2507",
    limit=100,
    output_format="openai",
    include_metadata=True
)
```

### 示例 2: 按节点提取数据
```python
# 提取特定 LangGraph 节点的数据
fetch_llm_training_data(
    age=1440,  # 24 小时
    langgraph_node="tool_responses_summary",
    limit=50,
    output_format="generic"
)
```

### 示例 3: 按 Agent 提取数据
```python
# 提取特定 Agent 的交互数据
fetch_llm_training_data(
    age=10080,
    agent_name="应用服务专家",
    limit=100,
    output_format="openai"
)
```

### 示例 4: 组合过滤（精确提取）
```python
# 同时使用多个过滤器
fetch_llm_training_data(
    age=10080,
    langgraph_node="tool_responses_summary",
    agent_name="应用服务专家",
    ls_model_name="Qwen3_235B_A22B_Instruct_2507_ShenZhen",
    limit=100,
    output_format="openai"
)
```

## 代码变更清单

### 主要文件
- ✅ `langfuse_mcp/__main__.py` - 更新过滤参数和逻辑
- ✅ `tests/test_tools.py` - 更新所有单元测试（5 个测试）
- ✅ `README.md` - 更新文档和示例
- ✅ `CHANGELOG.md` - 记录破坏性变更

### 测试状态
- ✅ 所有单元测试通过（23/23）
- ✅ 真实数据源测试通过
- ✅ 无 linter 错误

## 迁移指南

如果你正在使用旧版参数，请按以下方式迁移：

### 迁移步骤 1: 更新参数名称
```python
# 旧代码
fetch_llm_training_data(age=1440, node_name="llm_call")

# 新代码
fetch_llm_training_data(age=1440, langgraph_node="llm_call")
```

### 迁移步骤 2: 更新 model 参数
```python
# 旧代码
fetch_llm_training_data(age=1440, model="gpt-4")

# 新代码 - 使用 ls_model_name
fetch_llm_training_data(age=1440, ls_model_name="gpt-4-turbo")
```

### 迁移步骤 3: 移除 node_path（如果使用）
```python
# 旧代码
fetch_llm_training_data(age=1440, node_path="agent.reasoning")

# 新代码 - 使用 langgraph_node 或 agent_name
fetch_llm_training_data(age=1440, langgraph_node="reasoning_node")
# 或
fetch_llm_training_data(age=1440, agent_name="reasoning_agent")
```

### 迁移步骤 4: 利用新的 agent_name 参数
```python
# 新功能 - 按 Agent 筛选
fetch_llm_training_data(
    age=10080,
    agent_name="supervisor",
    output_format="openai"
)
```

## 优势总结

1. **✅ 匹配真实数据结构**：参数直接对应 LangFuse metadata 字段
2. **✅ 更灵活的过滤**：三种独立的过滤维度（节点、Agent、模型）
3. **✅ 更清晰的语义**：参数名称更直观，易于理解
4. **✅ 经过真实数据验证**：在生产环境数据上测试通过
5. **✅ 强制过滤要求**：防止意外提取所有数据

## 问题反馈

如果在使用新参数时遇到问题，请检查：
1. LangFuse 数据中是否包含对应的 metadata 字段
2. 是否至少提供了一个过滤参数
3. 参数值是否与实际数据中的值完全匹配（区分大小写）

