import os
from src.lore_objects import Agent, Environment, Perception
from src.main import Game

def test_agent_introspection_updates_memory():
    """
    Tests that an agent's memory is updated after introspection.
    """
    agent = Agent(agent_name="TestAgent", personality="A test personality.")
    agent.perception = Perception(owner="TestAgent", birth_turn=0, content="A test perception.")
    agent.introspect(birth_turn=0)
    assert len(agent.memory) == 1

def test_environment_divination_updates_reality():
    """
    Tests that the environment's reality is updated after divination.
    """
    env = Environment()
    env.divine()
    assert len(env.reality) == 1

def test_single_turn_updates_state_and_logs():
    """
    Tests that a single turn correctly updates game state and creates log files.
    """
    game = Game()
    game.setup()
    game._run_turn(0)

    # Test state changes
    assert len(game.env.reality) == 1
    assert len(game.agents[0].memory) == 1

    # Test log file creation
    log_file_path = os.path.join(".state_dump", "Charlie", "Introspection.md")
    assert os.path.exists(log_file_path)
