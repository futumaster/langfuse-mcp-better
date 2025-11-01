# Publishing langfuse-mcp-better to PyPI

This guide explains how to publish `langfuse-mcp-better` to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org
2. **API Token**: Generate an API token in your PyPI account settings
3. **TestPyPI Account** (optional but recommended): Create at https://test.pypi.org

## Version Management

This project uses semantic versioning with git tags:

- Version format: `v1.0.0`, `v1.0.1`, etc.
- Tag pattern configured in `pyproject.toml`: `tag-pattern = "v*"`

## Publishing Workflow

### 1. Prepare the Release

Make sure all changes are committed and tests pass:

```bash
# Run tests
uv run pytest

# Check for linting issues
uv run ruff check .
```

### 2. Update CHANGELOG.md

Update the `CHANGELOG.md` file with the new version and release date:

```markdown
## [1.0.0] - 2025-01-15

### Added
- New feature description
...
```

### 3. Create a Git Tag

```bash
# Commit your changes
git add .
git commit -m "Release v1.0.0"

# Create an annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Enhanced Langfuse MCP with training data extraction"
```

### 4. Build the Package

Clean any previous builds and create a new wheel:

```bash
# Remove old builds
rm -rf dist/

# Build wheel (skip source distribution)
uv build --wheel --no-build-logs --index-strategy unsafe-best-match
```

This will create a file like `dist/langfuse_mcp_better-1.0.0-py3-none-any.whl`

### 5. Test with TestPyPI (Recommended)

First publish to TestPyPI to verify everything works:

```bash
uv publish --index testpypi dist/langfuse_mcp_better-1.0.0-py3-none-any.whl
```

When prompted:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

Test the installation:

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ langfuse-mcp-better

# Test it works
langfuse-mcp-better --help
```

### 6. Publish to PyPI

Once you've verified everything works on TestPyPI:

```bash
uv publish dist/langfuse_mcp_better-1.0.0-py3-none-any.whl
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token

### 7. Push to GitHub

```bash
# Push the commit
git push origin main

# Push the tag
git push origin v1.0.0
```

### 8. Create a GitHub Release (Optional)

Go to your GitHub repository and create a release from the tag with the changelog notes.

## Troubleshooting

### Authentication Issues

If you get authentication errors:

1. Make sure you're using `__token__` as the username (not your PyPI username)
2. Verify your API token is correct and has upload permissions
3. For TestPyPI, use a TestPyPI token, not a PyPI token

### Version Conflicts

If you get "File already exists" errors:

1. You cannot re-upload the same version to PyPI
2. Increment the version number and create a new tag
3. Rebuild and try again

### Import Errors After Installation

If users report import errors:

1. Verify the package structure in `pyproject.toml`
2. Check that `packages = ["langfuse_mcp"]` is correct
3. Ensure `__init__.py` files exist in all package directories

## Version Numbering

Follow semantic versioning:

- **Major version (1.x.x)**: Breaking changes
- **Minor version (x.1.x)**: New features, backward compatible
- **Patch version (x.x.1)**: Bug fixes

For this enhanced version:
- Start with `v1.0.0` to indicate it's a major enhanced fork
- Use `v1.1.0` for new features
- Use `v1.0.1` for bug fixes

## Automated Publishing (Future)

Consider setting up GitHub Actions to automate publishing:

1. When a tag is pushed
2. Run tests
3. Build package
4. Publish to PyPI

Example workflow file can be added to `.github/workflows/publish.yml`

