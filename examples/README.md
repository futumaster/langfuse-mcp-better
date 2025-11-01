# Langfuse MCP Examples

This directory contains example scripts and demo clients that demonstrate how to use the Langfuse MCP integration.

## Available Examples

### langfuse_client_demo.py

A demonstration client that connects to the Langfuse MCP server and shows key functionality by executing various tool calls. It demonstrates:

- Connecting to the Langfuse MCP server
- Listing available tools
- Getting error counts
- Retrieving traces
- Finding exceptions

To run the demo client:

```bash
uv run examples/langfuse_client_demo.py --public-key YOUR_PUBLIC_KEY --secret-key YOUR_SECRET_KEY
```

### demo_training_data_extraction.py

**[NEW]** A comprehensive demo of the `fetch_llm_training_data` tool that shows how to extract training data from LangGraph applications. It demonstrates:

- Extracting LLM calls in different formats (OpenAI, Anthropic, generic, DPO)
- Filtering by LangGraph node name and hierarchy
- Filtering by LLM model (e.g., GPT-4 only)
- Including metadata (token usage, model parameters, timestamps)
- Saving training data to files

To run the training data extraction demo:

```bash
export LANGFUSE_PUBLIC_KEY=your_key
export LANGFUSE_SECRET_KEY=your_secret
export LANGFUSE_HOST=https://cloud.langfuse.com
uv run examples/demo_training_data_extraction.py
```

This demo is particularly useful if you're:
- Building fine-tuning datasets from production LLM interactions
- Creating training data for reinforcement learning
- Analyzing and filtering LLM calls by node or model
- Preparing data for Direct Preference Optimization (DPO)

The wrapper will use environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST`) if available. 
