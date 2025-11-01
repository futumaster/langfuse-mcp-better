#!/usr/bin/env python3
"""Demo script for extracting LLM training data from Langfuse.

This script demonstrates how to use the fetch_llm_training_data tool
to extract training data from LangGraph applications for fine-tuning
and reinforcement learning.
"""

import asyncio
import json
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def parse_response(result):
    """Extract data from MCP response."""
    if not hasattr(result, "content") or not result.content:
        return None, None

    raw_text = result.content[0].text or ""
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return raw_text, None

    if isinstance(payload, dict) and "data" in payload:
        return payload.get("data"), payload.get("metadata")

    return payload, None


async def demo_training_data_extraction():
    """Demonstrate various training data extraction scenarios."""
    pk = os.getenv("LANGFUSE_PUBLIC_KEY")
    sk = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not pk or not sk:
        print("Error: LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY must be set")
        return

    params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "-m",
            "langfuse_mcp",
            "--public-key",
            pk,
            "--secret-key",
            sk,
            "--host",
            host,
            "--log-level",
            "INFO",
        ],
    )

    print("=" * 80)
    print("LLM Training Data Extraction Demo")
    print("=" * 80)

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Example 1: Extract all LLM calls in OpenAI format
            print("\n1. Extracting all LLM calls (last 24h) in OpenAI format...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 1440,  # 24 hours
                    "output_format": "openai",
                    "limit": 5,
                },
            )
            data, metadata = await parse_response(result)
            if data:
                print(f"   Found {len(data)} training samples")
                print(f"   First sample preview:")
                print(f"   {json.dumps(data[0], indent=2)[:500]}...")
            else:
                print("   No data found")

            # Example 2: Filter by specific node
            print("\n2. Extracting from specific LangGraph node...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 10080,  # 7 days
                    "node_name": "agent_llm",
                    "output_format": "generic",
                    "limit": 10,
                },
            )
            data, metadata = await parse_response(result)
            if data:
                print(f"   Found {len(data)} samples from 'agent_llm' node")
            else:
                print("   No data found for this node")

            # Example 3: Filter by node hierarchy
            print("\n3. Extracting from node hierarchy (agent.reasoning.*)...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 10080,
                    "node_path": "agent.reasoning",
                    "output_format": "anthropic",
                    "limit": 5,
                },
            )
            data, metadata = await parse_response(result)
            if data:
                print(f"   Found {len(data)} samples from reasoning nodes")
                if metadata:
                    print(f"   Filters applied: {metadata.get('filters')}")
            else:
                print("   No data found for this path")

            # Example 4: Filter by model
            print("\n4. Extracting GPT-4 calls only...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 10080,
                    "model": "gpt-4",
                    "output_format": "openai",
                    "limit": 5,
                },
            )
            data, metadata = await parse_response(result)
            if data:
                print(f"   Found {len(data)} GPT-4 training samples")
                # Show metadata for first sample
                if data and "metadata" in data[0]:
                    meta = data[0]["metadata"]
                    print(f"   Sample metadata:")
                    print(f"     Model: {meta.get('model')}")
                    print(f"     Usage: {meta.get('usage')}")
                    print(f"     Node: {meta.get('node_name')}")
            else:
                print("   No GPT-4 data found")

            # Example 5: DPO format for preference learning
            print("\n5. Extracting in DPO format for preference learning...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 10080,
                    "output_format": "dpo",
                    "include_metadata": True,
                    "limit": 3,
                },
            )
            data, metadata = await parse_response(result)
            if data:
                print(f"   Found {len(data)} samples in DPO format")
                print("   Note: 'rejected' field is null - you'll need to add negative samples")
                if data:
                    sample = data[0]
                    print(f"   Sample structure: {list(sample.keys())}")
            else:
                print("   No data found")

            # Example 6: Save to file
            print("\n6. Extracting and saving to file...")
            result = await session.call_tool(
                "fetch_llm_training_data",
                {
                    "age": 10080,
                    "output_format": "openai",
                    "output_mode": "full_json_file",
                    "limit": 100,
                },
            )
            data, metadata = await parse_response(result)
            if metadata and metadata.get("file_path"):
                print(f"   Data saved to: {metadata['file_path']}")
                print(f"   Total samples: {metadata.get('item_count', 0)}")
            else:
                print("   File save not configured or failed")

    print("\n" + "=" * 80)
    print("Demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(demo_training_data_extraction())

