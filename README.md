# Langfuse MCP Better (Model Context Protocol)

[![PyPI version](https://badge.fury.io/py/langfuse-mcp-better.svg)](https://badge.fury.io/py/langfuse-mcp-better)
[![Python 3.10-3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Based on langfuse-mcp](https://img.shields.io/badge/based%20on-langfuse--mcp-blue)](https://github.com/avivsinai/langfuse-mcp)

An enhanced Model Context Protocol (MCP) server for Langfuse with powerful **training data extraction** capabilities. This fork adds specialized tools for extracting LLM training data from LangGraph applications, supporting fine-tuning and reinforcement learning workflows.

### What's New in Better?

- 🎯 **Training Data Extraction**: Extract LLM interactions filtered by LangGraph node hierarchy
- 🔄 **Multiple Output Formats**: OpenAI, Anthropic, generic prompt/completion, and DPO formats
- 🎨 **Smart Filtering**: Filter by node name, node path, model, and time range
- 📊 **Rich Metadata**: Token usage, model parameters, timestamps, and node information
- 🚀 **Production Ready**: Full test coverage and comprehensive documentation

Based on the excellent [langfuse-mcp](https://github.com/avivsinai/langfuse-mcp) by Aviv Sinai.

## Quick Start

### Installation

Install via pip or uvx:

```bash
# Using pip
pip install langfuse-mcp-better

# Using uvx (recommended)
uvx langfuse-mcp-better --public-key YOUR_KEY --secret-key YOUR_SECRET --host https://cloud.langfuse.com
```

### Cursor IDE Integration

For Cursor IDE, you can use the deeplink (replace with your credentials):

```json
{
  "mcpServers": {
    "langfuse-better": {
      "command": "uvx",
      "args": ["langfuse-mcp-better", "--public-key", "YOUR_KEY", "--secret-key", "YOUR_SECRET", "--host", "https://cloud.langfuse.com"]
    }
  }
}
```

> **💡 Note**: Cursor IDE deeplinks work best when configured manually in `.cursor/mcp.json`. See [Configuration](#configuration-with-mcp-clients) section below for details.

## Features

- Integration with Langfuse for trace and observation data
- Tool suite for AI agents to query trace data
- Exception and error tracking capabilities
- Session and user activity monitoring
- **Training data extraction** for fine-tuning and reinforcement learning
  - LangGraph node hierarchy filtering
  - Multiple output formats (OpenAI, Anthropic, generic, DPO)
  - Rich metadata including token usage and model parameters

## Available Tools

The MCP server provides the following tools for AI agents:

### Core Tools
- `fetch_traces` - Find traces based on criteria like user ID, session ID, etc.
- `fetch_trace` - Get a specific trace by ID
- `fetch_observations` - Get observations filtered by type
- `fetch_observation` - Get a specific observation by ID
- `fetch_sessions` - List sessions in the current project
- `get_session_details` - Get detailed information about a session
- `get_user_sessions` - Get all sessions for a user

### Exception & Error Tools
- `find_exceptions` - Find exceptions and errors in traces
- `find_exceptions_in_file` - Find exceptions in a specific file
- `get_exception_details` - Get detailed information about an exception
- `get_error_count` - Get the count of errors

### Training Data Tools
- `fetch_llm_training_data` - **[NEW]** Extract LLM training data from LangGraph nodes for fine-tuning and reinforcement learning. Supports multiple output formats (OpenAI, Anthropic, generic, DPO) and filtering by node hierarchy.

### Utility Tools
- `get_data_schema` - Get schema information for the data structures

## Setup

### Install `uv`

First, make sure `uv` is installed. For installation instructions, see the [`uv` installation docs](https://docs.astral.sh/uv/getting-started/installation/).

If you already have an older version of `uv` installed, you might need to update it with `uv self update`.

### Installation from PyPI

> **Requirement**: The server depends on the Langfuse Python SDK v3. Installations automatically pull `langfuse>=3.0.0` and require Python 3.10–3.13.

```bash
# Using pip
pip install langfuse-mcp-better

# Using uv
uv pip install langfuse-mcp-better
```

### Development Installation

If you're iterating on this repository, install the local checkout:

```bash
# from the repo root
uv pip install --editable .
```

### Recommended local environment

For development we suggest creating an isolated environment pinned to Python 3.11 (the version used in CI):

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv pip install --python .venv/bin/python -e .
```

All subsequent examples assume the virtual environment is activated.

### Obtain Langfuse credentials

You'll need your Langfuse credentials:
- Public key
- Secret key
- Host URL (usually https://cloud.langfuse.com or your self-hosted URL)

You can store these in a local `.env` file instead of passing CLI flags each time:

```
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

When present, the MCP server reads these values automatically. CLI arguments still override the environment if provided.

## Running the Server

Run the server using `uvx` or the installed command:

```bash
# Using uvx (no installation needed)
uvx langfuse-mcp-better --public-key YOUR_KEY --secret-key YOUR_SECRET --host https://cloud.langfuse.com

# Using the installed command
langfuse-mcp-better --public-key YOUR_KEY --secret-key YOUR_SECRET --host https://cloud.langfuse.com

# Backward compatible command also available
langfuse-mcp --public-key YOUR_KEY --secret-key YOUR_SECRET --host https://cloud.langfuse.com
```

> **Local checkout tip**: During development run `uv run python -m langfuse_mcp ...` to execute the code in your working tree.

The server writes diagnostic logs to `/tmp/langfuse_mcp.log`. Remove the `--host` switch if you are targeting the default Cloud endpoint.
Use `--log-level` (e.g., `--log-level DEBUG`) and `--log-to-console` to control verbosity during debugging.

### Run with Docker

#### Option 1: Pull from GitHub Container Registry (Recommended)

Pull and run the pre-built image:

```bash
docker pull ghcr.io/avivsinai/langfuse-mcp:latest
docker run --rm -i \
  -e LANGFUSE_PUBLIC_KEY=YOUR_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY=YOUR_SECRET_KEY \
  -e LANGFUSE_HOST=https://cloud.langfuse.com \
  -e LANGFUSE_MCP_LOG_FILE=/logs/langfuse_mcp.log \
  -v "$(pwd)/logs:/logs" \
  ghcr.io/avivsinai/langfuse-mcp:latest
```

Available tags:
- `latest` - Most recent release
- `v0.2.0` - Specific version
- `0.2` - Major.minor version

#### Option 2: Build from source

Build the image from the repository root so the container installs the current checkout instead of the latest PyPI release:

```bash
docker build -t langfuse-logs-mcp .
docker run --rm -i \
  -e LANGFUSE_PUBLIC_KEY=YOUR_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY=YOUR_SECRET_KEY \
  -e LANGFUSE_HOST=https://cloud.langfuse.com \
  -e LANGFUSE_MCP_LOG_FILE=/logs/langfuse_mcp.log \
  -v "$(pwd)/logs:/logs" \
  langfuse-logs-mcp
```

> **Why no `-t`?** Allocating a pseudo-TTY can interfere with MCP stdio clients. Use `-i` only so the server communicates over plain stdin/stdout.

The Dockerfile copies the local source tree and installs it with `pip install .`, so the container always runs your latest commits - a must while testing features that have not shipped on PyPI.


## Configuration with MCP clients

### Configure for Cursor

Create a `.cursor/mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "langfuse-better": {
      "command": "uvx",
      "args": ["langfuse-mcp-better", "--public-key", "YOUR_KEY", "--secret-key", "YOUR_SECRET", "--host", "https://cloud.langfuse.com"]
    }
  }
}
```

### Configure for Claude Desktop

Add to your Claude settings:

```json
{
  "command": ["uvx"],
  "args": ["langfuse-mcp-better"],
  "type": "stdio",
  "env": {
    "LANGFUSE_PUBLIC_KEY": "YOUR_KEY",
    "LANGFUSE_SECRET_KEY": "YOUR_SECRET",
    "LANGFUSE_HOST": "https://cloud.langfuse.com"
  }
}
```

## Output Modes

Each tool supports different output modes to control the level of detail in responses:

- `compact` (default): Returns a summary with large values truncated
- `full_json_string`: Returns the complete data as a JSON string
- `full_json_file`: Saves the complete data to a file and returns a summary with file information

## Using the Training Data Tool

The `fetch_llm_training_data` tool is specifically designed for extracting training data from LangGraph applications. It provides powerful filtering and formatting capabilities for machine learning workflows.

### Key Features

- **🚀 Automatic Pagination & Time Segmentation**: 
  - Request any amount of data (1000, 10000+) - pagination handled automatically
  - Query any time range (30 days, 60 days, 90+ days) - automatically splits into 7-day segments
  - No API limits or time restrictions exposed to users
- **🔍 Smart Filtering**: 
  - `ls_model_name`: Partial matching (case-insensitive) - "Qwen3_235B" matches all variants
  - `langgraph_node` and `agent_name`: Exact matching for precision
  - At least one filter required
- **Multiple Output Formats**: Support for OpenAI, Anthropic, generic, and DPO formats
- **Rich Metadata**: Includes token usage, model parameters, timestamps, and node information
- **Flexible Combinations**: Combine multiple filters for precise data extraction
- **Transparent**: Shows `pages_fetched`, `time_segments_processed`, and `total_raw_observations` in metadata

### Output Formats

#### OpenAI Format (`output_format="openai"`)
Perfect for OpenAI fine-tuning:
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI is artificial intelligence..."}
  ],
  "metadata": {
    "model": "gpt-4",
    "usage": {"total_tokens": 150},
    "langgraph_node": "llm_call",
    "agent_name": "supervisor",
    "ls_model_name": "gpt-4-turbo"
  }
}
```

#### Anthropic Format (`output_format="anthropic"`)
Optimized for Claude fine-tuning:
```json
{
  "system": "You are a helpful assistant",
  "messages": [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI is artificial intelligence..."}
  ],
  "metadata": {...}
}
```

#### Generic Format (`output_format="generic"`)
Simple prompt/completion pairs:
```json
{
  "prompt": "What is AI?",
  "completion": "AI is artificial intelligence...",
  "metadata": {...}
}
```

#### DPO Format (`output_format="dpo"`)
For Direct Preference Optimization:
```json
{
  "prompt": "What is AI?",
  "chosen": "AI is artificial intelligence...",
  "rejected": null,
  "metadata": {
    "_note": "rejected field is null - add negative samples for DPO training"
  }
}
```

### Automatic Pagination & Time Segmentation

**No more API limits or time restrictions!** The tool automatically handles both pagination and long time ranges:

```python
# Request 5000 samples from last 30 days - no problem!
fetch_llm_training_data(
    age=43200,  # 30 days (exceeds 7-day API limit)
    ls_model_name="gpt-4-turbo",
    limit=5000,  # Automatically fetches across multiple API calls
    output_format="openai"
)

# The tool will:
# 1. Split 30 days into 5 time segments (7 days each)
# 2. For each segment, paginate through API calls (100 items each)
# 3. Aggregate and return all samples across all segments
# 4. Show metadata: time_segments_processed=5, pages_fetched=50, total_raw_observations=5000
```

**Time Segmentation Details:**
- Queries > 7 days are automatically split into 7-day segments
- Each segment is processed with pagination
- Works seamlessly with any time range (30 days, 60 days, 90+ days)
- You never see API time limit errors!

### Usage Examples

#### Extract all LLM calls from a specific LangGraph node
```python
# Get 1000 LLM interactions from the "agent_llm" node in the last 24 hours
fetch_llm_training_data(
    age=1440,  # 24 hours in minutes
    langgraph_node="agent_llm",
    limit=1000,  # Default: will auto-paginate if needed
    output_format="openai"
)
```

#### Filter by agent name
```python
# Get 5000 LLM calls from the "supervisor" agent in the last week
fetch_llm_training_data(
    age=10080,  # 7 days
    agent_name="supervisor",
    limit=5000,  # Automatically handles pagination
    output_format="generic"
)
```

#### Filter by model name (partial matching)
```python
# Extract 10,000 Qwen model calls using partial name (30 days automatically segmented)
# "Qwen3_235B" will match all variants like:
#   - Qwen3_235B_A22B_Instruct_2507
#   - Qwen3_235B_A22B_Instruct_2507_ShenZhen
#   - Qwen3_235B_A22B_Instruct_2507_Beijing
fetch_llm_training_data(
    age=43200,  # 30 days (automatically split into 5 time segments)
    ls_model_name="Qwen3_235B",  # Partial name - matches all variants!
    limit=10000,  # Large scale - automatically paginated and segmented
    output_format="openai"
    # include_metadata=False by default - pure training data
)
```

#### Combine multiple filters
```python
# Extract data with specific node and model combination
fetch_llm_training_data(
    age=10080,
    langgraph_node="reasoning_node",
    ls_model_name="gpt-4-turbo",
    output_format="openai"
)
```

#### Save complete data to file
```python
# Extract data and save to file for offline processing
fetch_llm_training_data(
    age=10080,
    agent_name="supervisor",
    output_format="openai",
    output_mode="full_json_file"  # Saves to configured dump directory
)
```

### LangGraph Integration

The tool expects LangGraph applications to include specific metadata in their observations:

```python
# In your LangGraph application, add metadata to track nodes
from langfuse import Langfuse

langfuse = Langfuse()

# When creating observations, include the required metadata fields
generation = langfuse.generation(
    name="llm_call",
    input=messages,
    output=response,
    metadata={
        "langgraph_node": "reasoning_node",      # Required for filtering by node
        "agent_name": "supervisor",              # Required for filtering by agent
        "ls_model_name": "gpt-4-turbo"          # Required for filtering by model
    }
)
```

### Metadata Fields (Optional)

**By default (`include_metadata=False`), only training data is returned** - pure messages/prompts without metadata. This is what you want for model training.

Set `include_metadata=True` only when you need metadata for:
- **Data Analysis**: Token usage, cost tracking
- **Quality Control**: Filtering by performance metrics
- **Debugging**: Tracing back to original traces
- **Reproducibility**: Understanding data sources

When `include_metadata=True`, each sample includes:
- `observation_id`, `trace_id`: For tracing back to source
- `timestamp`: When the LLM call was made
- `model`, `model_parameters`: Model configuration
- `usage`: Token usage statistics (for cost analysis)
- `langgraph_node`, `agent_name`, `ls_model_name`: Source information

**⚠️ Important**: Metadata is NOT used during model training. Keep it disabled (default) for cleaner training files.

## Development

### Clone the repository

```bash
git clone https://github.com/futumaster/langfuse-mcp-better.git
cd langfuse-mcp-better
```

### Create a virtual environment and install dependencies

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install --python .venv/bin/python -e ".[dev]"
```

### Set up environment variables

```bash
export LANGFUSE_SECRET_KEY="your-secret-key"
export LANGFUSE_PUBLIC_KEY="your-public-key"
export LANGFUSE_HOST="https://cloud.langfuse.com"  # Or your self-hosted URL
```

### Testing

Run the unit test suite (mirrors CI):

```bash
pytest
```

To run the demo client:

```bash
uv run examples/langfuse_client_demo.py --public-key YOUR_PUBLIC_KEY --secret-key YOUR_SECRET_KEY
```


## Version Management

This project uses dynamic versioning based on Git tags:

1. The version is automatically determined from git tags using `uv-dynamic-versioning`
2. To create a new release:
   - Tag your commit with `git tag v0.1.2` (following semantic versioning)
   - Push the tag with `git push --tags`
   - Create a GitHub release from the tag
3. The GitHub workflow will automatically build and publish the package with the correct version to PyPI

For a detailed history of changes, please see the [CHANGELOG.md](CHANGELOG.md) file.

## Langfuse 3.x migration notes

- The MCP server now uses the Langfuse Python SDK v3 resource clients (`langfuse.api.trace.list`, `langfuse.api.observations.get_many`, etc.) and must currently run on Python 3.10–3.13 because the upstream SDK still relies on Pydantic v1 internals.
- Unit tests use a v3-style fake client that fails if legacy `fetch_*` helpers are invoked, helping catch regressions early.
- Tool responses now include pagination metadata when the Langfuse API returns cursors, while retaining the existing MCP interface.
- Diagnostic logs continue to stream to `/tmp/langfuse_mcp.log`; this is useful when verifying the upgraded integration against a live Langfuse deployment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Cache Management

We use the `cachetools` library to implement efficient caching with proper size limits:

- Uses `cachetools.LRUCache` for better reliability
- Configurable cache size via the `CACHE_SIZE` constant
- Automatically evicts the least recently used items when caches exceed their size limits
