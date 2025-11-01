"""Unit tests for langfuse-mcp tool functions."""

from __future__ import annotations

import asyncio
import json

import pytest

from tests.fakes import FakeContext, FakeLangfuse


@pytest.fixture()
def state(tmp_path):
    """Return an MCPState instance using the fake client."""
    from langfuse_mcp.__main__ import MCPState

    return MCPState(langfuse_client=FakeLangfuse(), dump_dir=str(tmp_path))


def test_fetch_traces_with_observations(state):
    """fetch_traces should use the v3 traces resource and embed observations."""
    from langfuse_mcp.__main__ import fetch_traces

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_traces(
            ctx,
            age=10,
            name=None,
            user_id=None,
            session_id=None,
            metadata=None,
            page=1,
            limit=50,
            tags=None,
            include_observations=True,
            output_mode="compact",
        )
    )
    assert result["metadata"]["item_count"] == 1
    assert result["data"][0]["id"] == "trace_1"
    assert isinstance(result["data"][0]["observations"], list)
    assert result["data"][0]["observations"][0]["id"] == "obs_1"
    assert state.langfuse_client.api.trace.last_list_kwargs is not None
    trace_kwargs = state.langfuse_client.api.trace.last_list_kwargs
    assert trace_kwargs["limit"] == 50
    assert "observations" in (trace_kwargs.get("fields") or "")


def test_fetch_trace(state):
    """fetch_trace should pull from the v3 traces resource."""
    from langfuse_mcp.__main__ import fetch_trace

    ctx = FakeContext(state)
    result = asyncio.run(fetch_trace(ctx, trace_id="trace_1", include_observations=True, output_mode="compact"))
    assert result["data"]["id"] == "trace_1"
    assert result["data"]["observations"][0]["id"] == "obs_1"
    assert state.langfuse_client.api.trace.last_get_kwargs == {"trace_id": "trace_1"}


def test_fetch_observations(state):
    """fetch_observations should call the v3 observations resource."""
    from langfuse_mcp.__main__ import fetch_observations

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_observations(
            ctx,
            type=None,
            age=10,
            name=None,
            user_id=None,
            trace_id=None,
            parent_observation_id=None,
            page=1,
            limit=50,
            output_mode="compact",
        )
    )
    assert result["metadata"]["item_count"] == 1
    assert result["data"][0]["id"] == "obs_1"
    assert state.langfuse_client.api.observations.last_get_many_kwargs is not None
    obs_kwargs = state.langfuse_client.api.observations.last_get_many_kwargs
    assert obs_kwargs["limit"] == 50


def test_fetch_observation(state):
    """fetch_observation should hit the observations resource."""
    from langfuse_mcp.__main__ import fetch_observation

    ctx = FakeContext(state)
    result = asyncio.run(fetch_observation(ctx, observation_id="obs_1", output_mode="compact"))
    assert result["data"]["id"] == "obs_1"
    assert state.langfuse_client.api.observations.last_get_kwargs == {"observation_id": "obs_1"}


def test_fetch_sessions(state):
    """fetch_sessions should rely on the v3 sessions resource."""
    from langfuse_mcp.__main__ import fetch_sessions

    ctx = FakeContext(state)
    result = asyncio.run(fetch_sessions(ctx, age=10, page=1, limit=50, output_mode="compact"))
    assert result["metadata"]["item_count"] == 1
    assert result["data"][0]["id"] == "session_1"
    assert state.langfuse_client.api.sessions.last_list_kwargs is not None
    sessions_kwargs = state.langfuse_client.api.sessions.last_list_kwargs
    assert sessions_kwargs["limit"] == 50


def test_get_session_details(state):
    """get_session_details should reuse the v3 traces resource."""
    from langfuse_mcp.__main__ import get_session_details

    ctx = FakeContext(state)
    result = asyncio.run(get_session_details(ctx, session_id="session_1", include_observations=True, output_mode="compact"))
    assert result["data"]["found"] is True
    assert result["data"]["trace_count"] == 1
    assert state.langfuse_client.api.trace.last_list_kwargs is not None
    trace_kwargs = state.langfuse_client.api.trace.last_list_kwargs
    assert trace_kwargs["session_id"] == "session_1"


def test_fetch_traces_full_json_string(state):
    """fetch_traces should honor explicit output mode strings."""
    from langfuse_mcp.__main__ import fetch_traces

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_traces(
            ctx,
            age=10,
            name=None,
            user_id=None,
            session_id=None,
            metadata=None,
            page=1,
            limit=50,
            tags=None,
            include_observations=False,
            output_mode="full_json_string",
        )
    )
    assert isinstance(result, str)
    loaded = json.loads(result)
    assert isinstance(loaded, list)


def test_find_exceptions_returns_envelope(state):
    """find_exceptions should return the standard response envelope."""
    from langfuse_mcp.__main__ import find_exceptions

    ctx = FakeContext(state)
    result = asyncio.run(find_exceptions(ctx, age=60, group_by="file"))
    assert set(result.keys()) == {"data", "metadata"}
    assert isinstance(result["data"], list)
    assert result["metadata"].get("item_count") == len(result["data"])


def test_get_user_sessions_returns_envelope(state):
    """get_user_sessions should always return an envelope structure."""
    from langfuse_mcp.__main__ import get_user_sessions

    ctx = FakeContext(state)
    result = asyncio.run(get_user_sessions(ctx, user_id="user_1", age=60, include_observations=False, output_mode="compact"))
    assert set(result.keys()) == {"data", "metadata"}
    assert isinstance(result["data"], list)


def test_negative_age_rejected(state):
    """All age parameters should be validated."""
    from langfuse_mcp.__main__ import fetch_traces

    ctx = FakeContext(state)
    with pytest.raises(ValueError):
        asyncio.run(
            fetch_traces(
                ctx,
                age=-5,
                name=None,
                user_id=None,
                session_id=None,
                metadata=None,
                page=1,
                limit=10,
                tags=None,
                include_observations=False,
                output_mode="compact",
            )
        )


def test_truncate_large_strings_case_insensitive():
    """Large field detection should be case-insensitive."""
    from langfuse_mcp.__main__ import MAX_FIELD_LENGTH, truncate_large_strings

    payload = {"Metadata.langfusePrompt": "x" * (MAX_FIELD_LENGTH + 50)}
    truncated, _ = truncate_large_strings(payload)
    value = truncated["Metadata.langfusePrompt"]
    assert isinstance(value, str)
    assert value.endswith("...")
    assert len(value) <= MAX_FIELD_LENGTH + len("...")


def test_fetch_llm_training_data_openai_format(state):
    """fetch_llm_training_data should format data in OpenAI format."""
    from langfuse_mcp.__main__ import fetch_llm_training_data

    # Add mock observations with LangGraph metadata
    state.langfuse_client.api.observations._mock_observations = [
        {
            "id": "obs_train_1",
            "type": "GENERATION",
            "trace_id": "trace_1",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-4",
            "input": {"messages": [{"role": "user", "content": "What is AI?"}]},
            "output": "AI is artificial intelligence.",
            "metadata": {
                "langgraph_node": "llm_call",
                "agent_name": "test_agent",
                "ls_model_name": "gpt-4-turbo",
            },
            "usage": {"total_tokens": 50},
        }
    ]

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_llm_training_data(
            ctx,
            age=1440,
            langgraph_node="llm_call",
            agent_name=None,
            ls_model_name=None,
            limit=100,
            output_format="openai",
            include_metadata=True,
            output_mode="compact",
        )
    )

    assert result["metadata"]["item_count"] == 1
    assert result["metadata"]["output_format"] == "openai"
    assert "data" in result
    sample = result["data"][0]
    assert "messages" in sample
    assert len(sample["messages"]) >= 2
    assert sample["messages"][-1]["role"] == "assistant"
    assert "metadata" in sample
    assert sample["metadata"]["langgraph_node"] == "llm_call"


def test_fetch_llm_training_data_generic_format(state):
    """fetch_llm_training_data should format data in generic prompt/completion format."""
    from langfuse_mcp.__main__ import fetch_llm_training_data

    state.langfuse_client.api.observations._mock_observations = [
        {
            "id": "obs_train_2",
            "type": "GENERATION",
            "trace_id": "trace_1",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-3.5-turbo",
            "input": "Explain machine learning",
            "output": "Machine learning is a subset of AI...",
            "metadata": {
                "langgraph_node": "reasoning_node",
                "agent_name": "reasoning_agent",
                "ls_model_name": "gpt-3.5-turbo",
            },
        }
    ]

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_llm_training_data(
            ctx,
            age=1440,
            langgraph_node="reasoning_node",
            agent_name=None,
            ls_model_name=None,
            limit=100,
            output_format="generic",
            include_metadata=True,
            output_mode="compact",
        )
    )

    assert result["metadata"]["item_count"] == 1
    sample = result["data"][0]
    assert "prompt" in sample
    assert "completion" in sample
    assert sample["prompt"] == "Explain machine learning"
    assert sample["completion"] == "Machine learning is a subset of AI..."


def test_fetch_llm_training_data_filters_by_ls_model_name(state):
    """fetch_llm_training_data should filter by ls_model_name with partial matching."""
    from langfuse_mcp.__main__ import fetch_llm_training_data

    state.langfuse_client.api.observations._mock_observations = [
        {
            "id": "obs_qwen_full",
            "type": "GENERATION",
            "trace_id": "trace_1",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "qwen",
            "input": "Test prompt",
            "output": "Test response",
            "metadata": {
                "langgraph_node": "llm_call",
                "ls_model_name": "Qwen3_235B_A22B_Instruct_2507",
            },
        },
        {
            "id": "obs_qwen_variant",
            "type": "GENERATION",
            "trace_id": "trace_2",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "qwen",
            "input": "Test prompt 2",
            "output": "Test response 2",
            "metadata": {
                "langgraph_node": "llm_call",
                "ls_model_name": "Qwen3_235B_A22B_Instruct_2507_ShenZhen",
            },
        },
        {
            "id": "obs_gpt",
            "type": "GENERATION",
            "trace_id": "trace_3",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-3.5-turbo",
            "input": "Test prompt 3",
            "output": "Test response 3",
            "metadata": {
                "langgraph_node": "llm_call",
                "ls_model_name": "gpt-3.5-turbo",
            },
        },
    ]

    ctx = FakeContext(state)
    # Test partial matching: "Qwen3_235B" should match both Qwen variants
    result = asyncio.run(
        fetch_llm_training_data(
            ctx,
            age=1440,
            langgraph_node=None,
            agent_name=None,
            ls_model_name="Qwen3_235B",  # Partial name
            limit=100,
            output_format="generic",
            include_metadata=False,
            output_mode="compact",
        )
    )

    assert result["metadata"]["item_count"] == 2
    # Should return both Qwen observations (full and variant)


def test_fetch_llm_training_data_filters_by_agent_name(state):
    """fetch_llm_training_data should filter by agent_name."""
    from langfuse_mcp.__main__ import fetch_llm_training_data

    state.langfuse_client.api.observations._mock_observations = [
        {
            "id": "obs_supervisor",
            "type": "GENERATION",
            "trace_id": "trace_1",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-4",
            "input": "Supervise the task",
            "output": "Task supervised",
            "metadata": {
                "langgraph_node": "supervisor_node",
                "agent_name": "supervisor",
            },
        },
        {
            "id": "obs_worker",
            "type": "GENERATION",
            "trace_id": "trace_2",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-4",
            "input": "Execute task",
            "output": "Task executed",
            "metadata": {
                "langgraph_node": "worker_node",
                "agent_name": "worker",
            },
        },
    ]

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_llm_training_data(
            ctx,
            age=1440,
            langgraph_node=None,
            agent_name="supervisor",
            ls_model_name=None,
            limit=100,
            output_format="generic",
            include_metadata=True,
            output_mode="compact",
        )
    )

    assert result["metadata"]["item_count"] == 1
    sample = result["data"][0]
    assert sample["metadata"]["agent_name"] == "supervisor"


def test_fetch_llm_training_data_dpo_format(state):
    """fetch_llm_training_data should format data in DPO format."""
    from langfuse_mcp.__main__ import fetch_llm_training_data

    state.langfuse_client.api.observations._mock_observations = [
        {
            "id": "obs_dpo",
            "type": "GENERATION",
            "trace_id": "trace_1",
            "start_time": "2024-01-01T00:00:00Z",
            "model": "gpt-4",
            "input": "Write a poem",
            "output": "Roses are red...",
            "metadata": {
                "langgraph_node": "poet",
                "agent_name": "poet_agent",
                "ls_model_name": "gpt-4",
            },
        }
    ]

    ctx = FakeContext(state)
    result = asyncio.run(
        fetch_llm_training_data(
            ctx,
            age=1440,
            langgraph_node="poet",
            agent_name=None,
            ls_model_name=None,
            limit=100,
            output_format="dpo",
            include_metadata=True,
            output_mode="compact",
        )
    )

    assert result["metadata"]["item_count"] == 1
    sample = result["data"][0]
    assert "prompt" in sample
    assert "chosen" in sample
    assert "rejected" in sample
    assert sample["rejected"] is None  # Should be None by default
    assert "metadata" in sample
    assert "_note" in sample["metadata"]  # Should have note about rejected samples
