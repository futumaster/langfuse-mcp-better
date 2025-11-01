# Quick Start Guide - langfuse-mcp-better

Get started with `langfuse-mcp-better` in 5 minutes!

## Installation

```bash
pip install langfuse-mcp-better
```

## Basic Usage

### 1. Run the Server

```bash
langfuse-mcp-better \
  --public-key YOUR_LANGFUSE_PUBLIC_KEY \
  --secret-key YOUR_LANGFUSE_SECRET_KEY \
  --host https://cloud.langfuse.com
```

Or using environment variables:

```bash
export LANGFUSE_PUBLIC_KEY=your_key
export LANGFUSE_SECRET_KEY=your_secret
export LANGFUSE_HOST=https://cloud.langfuse.com

langfuse-mcp-better
```

### 2. Configure in Cursor IDE

Create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "langfuse-better": {
      "command": "uvx",
      "args": [
        "langfuse-mcp-better",
        "--public-key", "YOUR_KEY",
        "--secret-key", "YOUR_SECRET",
        "--host", "https://cloud.langfuse.com"
      ]
    }
  }
}
```

### 3. Try the Training Data Tool

In your AI agent or Cursor chat:

```
Extract LLM training data from the last 24 hours in OpenAI format from the agent_llm node
```

The AI will use:

```python
fetch_llm_training_data(
    age=1440,
    node_name="agent_llm",
    output_format="openai"
)
```

## Common Use Cases

### Extract Training Data by Node

```python
# Get all interactions from a specific node
fetch_llm_training_data(
    age=1440,  # last 24 hours
    node_name="agent_reasoning",
    output_format="openai"
)
```

### Filter by Model

```python
# Get only GPT-4 calls
fetch_llm_training_data(
    age=10080,  # last 7 days
    model="gpt-4",
    output_format="generic"
)
```

### Extract by Node Hierarchy

```python
# Get all nodes under agent.tools.*
fetch_llm_training_data(
    age=10080,
    node_path="agent.tools",
    output_format="anthropic"
)
```

### Save to File

```python
# Extract and save to file
fetch_llm_training_data(
    age=10080,
    node_name="agent_llm",
    output_format="openai",
    output_mode="full_json_file"
)
```

## Output Formats

### OpenAI Format
Perfect for OpenAI fine-tuning API:
```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "metadata": {...}
}
```

### Anthropic Format
For Claude fine-tuning:
```json
{
  "system": "...",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

### Generic Format
Simple prompt/completion:
```json
{
  "prompt": "...",
  "completion": "...",
  "metadata": {...}
}
```

### DPO Format
For reinforcement learning:
```json
{
  "prompt": "...",
  "chosen": "...",
  "rejected": null
}
```

## LangGraph Integration

Add metadata to your LangGraph nodes:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# In your node
generation = langfuse.generation(
    name="my_llm_call",
    input=messages,
    output=response,
    metadata={
        "langgraph_node": "reasoning",
        "langgraph_path": "agent.reasoning.step1"
    }
)
```

## Next Steps

- Read [ENHANCED_FEATURES.md](ENHANCED_FEATURES.md) for detailed feature comparison
- Check [README.md](README.md) for complete documentation
- See [examples/demo_training_data_extraction.py](examples/demo_training_data_extraction.py) for more examples

## Need Help?

- **Issues**: https://github.com/futumaster/langfuse-mcp-better/issues
- **Original Project**: https://github.com/avivsinai/langfuse-mcp
- **Documentation**: See README.md

