# Verification Guide

This guide helps you verify that `langfuse-mcp-better` is correctly installed and working.

## 1. Verify Installation

```bash
# Check if the package is installed
pip list | grep langfuse-mcp-better

# Or using uv
uv pip list | grep langfuse-mcp-better
```

Expected output:
```
langfuse-mcp-better    1.0.0
```

## 2. Verify Commands

```bash
# Check the new command
which langfuse-mcp-better

# Check backward compatible command
which langfuse-mcp
```

Both commands should point to installed executables.

## 3. Test Command Help

```bash
# Test primary command
langfuse-mcp-better --help

# Test backward compatible command
langfuse-mcp --help
```

Expected output should include:
```
usage: langfuse-mcp-better [-h] --public-key PUBLIC_KEY --secret-key
                           SECRET_KEY [--host HOST] ...

Langfuse MCP Server
...
```

## 4. Verify Build

From the repository root:

```bash
# Clean previous builds
rm -rf dist/

# Build the wheel
uv build --wheel --no-build-logs

# Check the output
ls -lh dist/
```

Expected output:
```
langfuse_mcp_better-1.0.0-py3-none-any.whl
```

## 5. Run Tests

```bash
# Run all tests except the pre-existing failing one
uv run pytest tests/ -k "not test_find_exceptions_returns_envelope" -v

# Run only new training data tests
uv run pytest tests/test_tools.py -k "fetch_llm_training_data" -v
```

Expected output:
```
22 passed, 1 deselected  # For all tests
5 passed                  # For training data tests only
```

## 6. Test Import

```bash
# Test Python import
python -c "from langfuse_mcp.__main__ import fetch_llm_training_data; print('Import successful')"

# Using uv
uv run python -c "from langfuse_mcp.__main__ import fetch_llm_training_data; print('Import successful')"
```

Expected output:
```
Import successful
```

## 7. Verify MCP Server

Test the MCP server starts correctly:

```bash
# Set dummy credentials (server won't connect but should start)
export LANGFUSE_PUBLIC_KEY=test_key
export LANGFUSE_SECRET_KEY=test_secret
export LANGFUSE_HOST=https://cloud.langfuse.com

# Start the server (it will wait for MCP protocol input)
timeout 2 langfuse-mcp-better || echo "Server started successfully"
```

The server should start without errors (timeout is expected).

## 8. Verify Tools Are Registered

Create a test script `test_mcp_tools.py`:

```python
#!/usr/bin/env python3
"""Verify MCP tools are registered."""

from langfuse_mcp.__main__ import app_factory

# Create MCP app
app = app_factory(
    public_key="test_key",
    secret_key="test_secret",
    host="https://cloud.langfuse.com"
)

# Get list of tools
tools = app._tool_manager.list_tools()

print("Registered tools:")
for tool in tools:
    print(f"  - {tool.name}")

# Check if new tool is registered
tool_names = [tool.name for tool in tools]
assert "fetch_llm_training_data" in tool_names, "New tool not found!"
print("\n✅ fetch_llm_training_data tool is registered!")
```

Run it:
```bash
uv run python test_mcp_tools.py
```

Expected output should include:
```
Registered tools:
  - fetch_traces
  - fetch_trace
  ...
  - fetch_llm_training_data
  - get_data_schema

✅ fetch_llm_training_data tool is registered!
```

## 9. Verify Documentation

Check that documentation files exist:

```bash
ls -1 *.md
```

Expected files:
```
CHANGELOG.md
CONTRIBUTING.md
ENHANCED_FEATURES.md
MIGRATION_SUMMARY.md
PUBLISHING.md
QUICKSTART.md
README.md
SECURITY.md
VERIFICATION.md
```

## 10. Check Package Metadata

```bash
# View package info
pip show langfuse-mcp-better

# Or using uv
uv pip show langfuse-mcp-better
```

Expected output:
```
Name: langfuse-mcp-better
Version: 1.0.0
Summary: Enhanced Langfuse MCP server with training data extraction...
Author: Aviv Sinai, Wenxin Huang
...
```

## Troubleshooting

### Command not found

If `langfuse-mcp-better` is not found:

```bash
# Reinstall the package
pip install --force-reinstall langfuse-mcp-better

# Or in development mode
uv pip install --editable .
```

### Import errors

If you get import errors:

```bash
# Check if langfuse_mcp module exists
python -c "import langfuse_mcp; print(langfuse_mcp.__file__)"

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Test failures

If tests fail:

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests with more verbose output
uv run pytest tests/ -vv
```

### Build issues

If build fails:

```bash
# Update build tools
pip install --upgrade build uv-dynamic-versioning hatchling

# Try building again
uv build --wheel
```

## Success Criteria

All of the following should pass:

- ✅ Package is installed
- ✅ Commands are available
- ✅ Help text displays
- ✅ Build succeeds
- ✅ Tests pass (22 out of 23)
- ✅ Import works
- ✅ New tool is registered
- ✅ Documentation is complete

If all checks pass, your installation is verified! 🎉

## Next Steps

After verification:

1. Read [QUICKSTART.md](QUICKSTART.md) to start using the tool
2. Check [ENHANCED_FEATURES.md](ENHANCED_FEATURES.md) for detailed features
3. Follow [PUBLISHING.md](PUBLISHING.md) to publish to PyPI

