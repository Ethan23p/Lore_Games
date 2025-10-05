# tests/test_app.py

import pytest
import asyncio
from app import LoreGamesApp
from ai_handler import AIHandler

async def run_turn_integration_test(monkeypatch):
    """Core async logic for the integration test."""
    # 1. Mock the AIHandler to return a predictable response
    async def mock_generate(*args, **kwargs):
        return "mocked AI response"

    monkeypatch.setattr(AIHandler, "generate", mock_generate)

    # 2. Set up the application
    app = LoreGamesApp()
    app.setup()
    await app._prime_agents()

    # 3. Store initial state for later comparison
    initial_turn = app.current_turn
    agent_id = list(app.agents.keys())[0]
    initial_memory_len = len(app.agents[agent_id].memory)

    # 4. Execute the turn
    await app._execute_turn()

    # 5. Assert that the state has changed as expected
    assert app.current_turn == initial_turn + 1
    assert len(app.agents[agent_id].memory) == initial_memory_len + 1
    assert app.environment.reality[app.current_turn] == "mocked AI response"

def test_execute_turn_integration_sync(monkeypatch):
    """Synchronous wrapper to run the async integration test."""
    asyncio.run(run_turn_integration_test(monkeypatch))
