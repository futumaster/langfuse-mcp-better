# Enhanced Features in langfuse-mcp-better

This document highlights the enhancements made in `langfuse-mcp-better` compared to the original `langfuse-mcp`.

## 🆕 New Tool: fetch_llm_training_data

The main enhancement is the new `fetch_llm_training_data` tool, designed specifically for extracting training data from LangGraph applications.

### Why This Tool?

The original `langfuse-mcp` is excellent for debugging and observability, but it lacks specialized features for:

1. **Extracting training data** from production LLM interactions
2. **Filtering by LangGraph node hierarchy** without needing trace IDs
3. **Formatting data** for different fine-tuning platforms
4. **Preparing datasets** for reinforcement learning

### Key Capabilities

#### 1. Node Hierarchy Filtering

Unlike the original tools that require trace IDs, this tool filters by node metadata:

```python
# Filter by specific node name
fetch_llm_training_data(
    age=1440,
    node_name="agent_llm",  # Match exact node name
    output_format="openai"
)

# Filter by node path hierarchy
fetch_llm_training_data(
    age=10080,
    node_path="agent.reasoning",  # Matches agent.reasoning.*
    output_format="generic"
)
```

#### 2. Multiple Output Formats

Supports 4 specialized formats for different use cases:

| Format | Use Case | Output Structure |
|--------|----------|------------------|
| `openai` | OpenAI fine-tuning | `{"messages": [...], "metadata": {...}}` |
| `anthropic` | Claude fine-tuning | `{"system": "...", "messages": [...]}` |
| `generic` | General purpose | `{"prompt": "...", "completion": "..."}` |
| `dpo` | Direct Preference Optimization | `{"prompt": "...", "chosen": "...", "rejected": null}` |

#### 3. Smart Filtering

Combine multiple filters:

```python
# Get only GPT-4 calls from reasoning nodes in the last week
fetch_llm_training_data(
    age=10080,
    node_path="agent.reasoning",
    model="gpt-4",
    output_format="openai",
    limit=1000
)
```

#### 4. Rich Metadata

Each training sample includes valuable metadata:

- `observation_id`: For tracking back to the original observation
- `trace_id`: For full context
- `timestamp`: When the LLM call was made
- `model`: Which model was used
- `model_parameters`: Temperature, max_tokens, etc.
- `usage`: Token statistics (prompt_tokens, completion_tokens, total_tokens)
- `node_name`: LangGraph node name
- `node_path`: Full hierarchical path

This metadata is invaluable for:
- **Cost analysis**: Calculate training data costs
- **Quality filtering**: Select high-quality samples
- **Performance tracking**: Analyze model behavior by node
- **Reproducibility**: Track exact configurations used

## Comparison with Original Tools

### Original: fetch_observations

```python
# Original tool - requires trace_id, returns raw observations
fetch_observations(
    type="GENERATION",
    age=1440,
    trace_id="specific-trace-123"  # Must know trace ID
)
```

**Limitations:**
- Requires trace_id to be known
- No filtering by node hierarchy
- Raw output format (not training-ready)
- No specialized formatting for ML platforms

### Enhanced: fetch_llm_training_data

```python
# Enhanced tool - filters by node, formats for training
fetch_llm_training_data(
    age=1440,
    node_name="agent_llm",  # Filter by node name
    output_format="openai"   # Training-ready format
)
```

**Advantages:**
- ✅ No trace_id needed
- ✅ Filter by node hierarchy
- ✅ Training-ready output formats
- ✅ Rich metadata included
- ✅ Model-based filtering
- ✅ Time-range queries

## Use Cases

### 1. Building Fine-Tuning Datasets

Extract successful interactions from production:

```python
fetch_llm_training_data(
    age=10080,  # Last week
    node_name="successful_responses",
    model="gpt-4",
    output_format="openai",
    limit=10000
)
```

### 2. Reinforcement Learning Data

Prepare data for RLHF or DPO:

```python
fetch_llm_training_data(
    age=10080,
    node_path="agent.actions",
    output_format="dpo",
    include_metadata=True
)
```

### 3. Model Performance Analysis

Compare different nodes:

```python
# Get data from reasoning nodes
reasoning_data = fetch_llm_training_data(
    age=1440,
    node_path="agent.reasoning",
    output_format="generic"
)

# Get data from action nodes
action_data = fetch_llm_training_data(
    age=1440,
    node_path="agent.actions",
    output_format="generic"
)
```

### 4. Cost Optimization

Analyze token usage by node:

```python
data = fetch_llm_training_data(
    age=10080,
    node_name="expensive_node",
    include_metadata=True,
    output_format="generic"
)

# Metadata includes usage: {prompt_tokens, completion_tokens, total_tokens}
total_tokens = sum(sample['metadata']['usage']['total_tokens'] for sample in data)
```

## Integration with LangGraph

To use this tool effectively, your LangGraph application should include node metadata:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# In your LangGraph nodes, add metadata
generation = langfuse.generation(
    name="agent_reasoning",
    input=input_messages,
    output=response,
    model="gpt-4",
    metadata={
        "langgraph_node": "reasoning_node",      # Node name
        "langgraph_path": "agent.reasoning.step1" # Hierarchical path
    }
)
```

## Backward Compatibility

All original tools remain available and unchanged:
- `fetch_traces`
- `fetch_trace`
- `fetch_observations`
- `fetch_observation`
- `fetch_sessions`
- `get_session_details`
- `get_user_sessions`
- `find_exceptions`
- `find_exceptions_in_file`
- `get_exception_details`
- `get_error_count`
- `get_data_schema`

## Future Enhancements

Potential future additions:
- Automatic dataset balancing
- Quality scoring integration
- Multi-turn conversation extraction
- Automatic preference pair generation for DPO
- Integration with popular fine-tuning platforms

## Credits

Built on top of the excellent [langfuse-mcp](https://github.com/avivsinai/langfuse-mcp) by Aviv Sinai.

Enhanced by Wenxin Huang with focus on ML training workflows.

