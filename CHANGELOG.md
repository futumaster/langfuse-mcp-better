# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.2] - 2024-11-01

### Fixed
- **Chinese character readability**: All JSON output now uses `ensure_ascii=False`
  - Chinese and other Unicode characters are now displayed directly instead of being escaped
  - Example: "你好" instead of "\u4f60\u597d"
  - Affects all exported training data and saved files
  - Greatly improves readability for non-ASCII languages

## [1.2.1] - 2024-11-01

### Changed
- **Improved `ls_model_name` filtering**: Now supports partial matching (case-insensitive)
  - Users can search with short model names (e.g., "Qwen3_235B") to match all variants
  - "Qwen3_235B" now matches "Qwen3_235B_A22B_Instruct_2507_ShenZhen", etc.
  - Case-insensitive: "qwen" matches "Qwen3_235B_A22B_Instruct_2507"
  - `langgraph_node` and `agent_name` remain exact match (as intended)

### Fixed
- Resolved user-reported issue where partial model names failed to find data
- Improved user experience by reducing trial-and-error in model name queries

### Enhanced
- Added comprehensive test for partial model name matching
- Updated documentation with partial matching examples
- Created detailed explanation document: `MODEL_NAME_PARTIAL_MATCHING.md`

## [1.2.0] - 2024-11-01

### Added
- **Automatic Pagination**: `fetch_llm_training_data` now handles large data requests automatically
  - Removed `page` parameter - pagination is now handled internally
  - Increased default `limit` from 100 to 1000
  - Users can now request any amount of data (e.g., 1000, 10000) without hitting API limits
  - Internal batching with 100-item pages to respect LangFuse API constraints
  - New metadata fields: `pages_fetched` and `total_raw_observations` for transparency

### Changed
- **BREAKING**: Removed `page` parameter from `fetch_llm_training_data`
  - Users no longer need to manually paginate
  - All pagination is handled automatically by the MCP server

### Enhanced
- Improved logging for pagination process (shows progress across pages)
- Better error handling for large data requests
- Documentation updated with automatic pagination examples

## [1.1.0] - 2024-11-01

### Changed
- **BREAKING**: `fetch_llm_training_data` filter parameters updated to match real LangFuse metadata structure
  - Renamed `node_name` → `langgraph_node` (matches `metadata.langgraph_node`)
  - Removed `node_path` parameter (not commonly used in practice)
  - Renamed `model` → `ls_model_name` (matches `metadata.ls_model_name`)
  - Added `agent_name` parameter (matches `metadata.agent_name`)
  - **At least one filter parameter is now required** (`langgraph_node`, `agent_name`, or `ls_model_name`)

### Added
- Comprehensive documentation: `TESTING_SUMMARY.md` and `PARAMETER_UPDATE_SUMMARY.md`
- Real-world usage examples with actual LangFuse data

### Enhanced
- Tested `fetch_llm_training_data` with real LangFuse data source (verified with production data)
- Updated metadata structure to include `langgraph_node`, `agent_name`, and `ls_model_name`
- Improved documentation with real-world examples and complete metadata structure reference
- Updated all 5 unit tests to reflect new parameter names
- Enhanced README with migration guide and best practices

## [1.0.0] - 2024-11-01

### Changed
- **BREAKING**: Rebranded as `langfuse-mcp-better` - now installable via `pip install langfuse-mcp-better`
- Command renamed to `langfuse-mcp-better` (backward compatible `langfuse-mcp` command still available)
- Enhanced project description to highlight training data extraction capabilities

### Added
- **NEW TOOL**: `fetch_llm_training_data` for extracting LLM training data from LangGraph nodes
  - Support for LangGraph node hierarchy filtering (`node_name`, `node_path`)
  - Multiple output formats: OpenAI, Anthropic, generic, and DPO
  - Model-based filtering (e.g., filter by GPT-4, Claude-3)
  - Rich metadata including token usage, model parameters, and timestamps
  - Time-range based queries
- Comprehensive test suite for training data extraction (5 new tests)
- Demo script: `examples/demo_training_data_extraction.py`
- Extensive documentation for training data extraction workflows

### Enhanced
- README with detailed training data extraction guide
- Examples documentation with new training data extraction demo

## [0.2.1] - 2025-10-20

### Fixed
- Added guardrails to prevent running on Python 3.14+, documenting that the current Langfuse SDK dependency only supports Python 3.10–3.13 and updating packaging metadata so `uvx langfuse-mcp` resolves a compatible interpreter automatically.

## [0.2.0] - 2025-01-06

### Changed
- **BREAKING**: Migrated to Langfuse SDK v3.x (requires `langfuse>=3.0.0`)
- **BREAKING**: Tool responses now use envelope format `{"data": ..., "metadata": {...}}`
- Updated test doubles and unit tests to model the v3 API surface and ensure compatibility going forward
- MCP CLI now reads Langfuse credentials (`public_key`, `secret_key`, `host`) from a `.env` file or environment variables by default, keeping CLI flags optional
- Normalized output mode handling, tool envelopes, and logging configuration; added CLI options for log level/console output and standardized responses across all tools
- Docker image installs the local repository (`pip install .`) so containers run the same code under development instead of the last PyPI release, and now bundles `git` so dynamic versioning works during image builds
- README now documents how to execute the working tree with `uv run --from /path/to/langfuse-mcp`, clarifies why Docker builds should come from the local checkout, and shows how to install the repository version with `uv pip install --editable .`

### Added
- Docker support with Dockerfile for containerized deployments
- Environment variable support for credentials via `.env` files
- Enhanced logging configuration with `--log-level` and `--log-to-console` flags
- Pagination metadata in API responses

### Removed
- Dropped Langfuse v2 SDK support (now requires v3)

## [0.1.8] - 2025-01-05

### Added
- Comprehensive test suite with 10 tests covering all functionality
- Enhanced CI workflow with improved logging and verbose output
- Complete documentation with proper docstrings for all test files

### Changed
- Improved GitHub Actions workflow for better visibility and debugging
- Enhanced repository structure with complete test coverage

### Fixed
- All linting and formatting issues resolved
- Proper dependency management and build process

## [0.1.7] - 2025-01-05

### Changed
- Pinned Langfuse dependency to stable v2 branch (`>=2.60,<3.0.0`) for compatibility
- Enhanced CI matrix to test both Langfuse v2 and v3 (v3 allowed to fail)
- Removed uv.lock from version control as recommended for libraries

### Added
- Optional dev-v3 dependency group for future Langfuse v3 migration testing

## [0.1.6] - 2025-04-01

## [0.1.5] - 2025-03-31

### Added
- Enhanced README with detailed output processing information
- Added publish guidelines in project documentation

### Changed
- Improved data processing and output handling
- Increased get_error_count max age limit from 100 minutes to 7 days
- Updated documentation to include README reference in Cursor rules

## [0.1.4] - 2025-03-25

### Added
- Enhanced response processing with truncation for large fields
- Added more robust date parsing
- Improved exception handling

### Changed
- Refactored MCP runner and updated logging 
- Removed Optional type hints from function signatures for better compatibility
- Updated project metadata and build configuration

## [0.1.2] - 2025-03-20

### Added
- Added dynamic versioning with uv-dynamic-versioning
- Version history documentation
- Recommended GitHub Actions for CI/CD

### Changed
- Removed mcp.json from git history and added to gitignore
- Improved test configuration

## [0.1.1] - 2025-03-15

### Added
- Initial release with basic MCP server functionality
- Tool for retrieving traces based on filters
- Tool for finding exceptions grouped by file, function, or type
- Tool for getting detailed exception information
- Tool for retrieving sessions
- Tool for getting error counts
- Tool for fetching data schema

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2025-XX-XX
- Initial release 
