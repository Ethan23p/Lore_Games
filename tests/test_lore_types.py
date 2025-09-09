from src.lore_types import Agent, Environment, TurnId
from src.ai_handler import AIHandler

def test_agent_initialization():
    """
    Tests that an Agent can be initialized without errors.
    """
    ai_handler = AIHandler()
    agent = Agent(name="Test Agent", personality="test_personality", ai_handler=ai_handler)
    assert agent.name == "Test Agent"
    assert agent.personality == "test_personality"
    assert agent.id is not None
    assert isinstance(agent.memory, list)
    assert agent.ai is not None

def test_environment_initialization():
    """
    Tests that an Environment can be initialized without errors.
    """
    ai_handler = AIHandler()
    agent = Agent(name="Test Agent", personality="test", ai_handler=ai_handler)
    env = Environment(agents=[agent], initial_reality="A test world.", ai_handler=ai_handler)
    assert env.reality is not None
    assert isinstance(env.reality, list)
    assert len(env.reality) == 1
    assert "A test world." in env.reality[0].content
    assert env.ai is not None

def test_run_single_turn_with_clean_ai_payloads():
    """
    Verifies state changes with the new, cleaner mock AI payloads.
    """
    # Setup
    ai_handler = AIHandler()
    agents = [Agent(name="Alice", personality="curious", ai_handler=ai_handler)]
    env = Environment(agents=agents, initial_reality="A room with a red button.", ai_handler=ai_handler)
    
    # Action
    env.run_turn(TurnId(0))
    
    # Assert
    # Environment state
    assert len(env.reality) == 2
    assert "A lone figure can be seen" in env.reality[1].content # From divination
    
    # Agent state
    alice = agents[0]
    assert len(alice.memory) == 1
    assert "The world feels vast" in alice.memory[0].content # From introspect

def test_history_compilation_with_clean_payloads():
    """
    Ensures perception compiles the history of clean AI-generated payloads.
    """
    # Setup
    ai_handler = AIHandler()
    agents = [Agent(name="Bob", personality="cautious", ai_handler=ai_handler)]
    env = Environment(agents=agents, initial_reality="It is morning.", ai_handler=ai_handler)
    
    # Action
    env.run_turn(TurnId(0))
    env.run_turn(TurnId(1))
    
    perception = env.reflect(agents[0], TurnId(2))
    
    # Assert
    assert "It is morning." in perception.content
    assert "A lone figure can be seen" in perception.content # Check for divination content from turns 0 and 1

def test_clean_ai_driven_type_flow():
    """
    Checks that the clean AI payloads flow through the interaction types.
    """
    # Setup
    ai_handler = AIHandler()
    agent = Agent(name="Carol", personality="bold", ai_handler=ai_handler)
    env = Environment(agents=[agent], initial_reality="A single choice.", ai_handler=ai_handler)
    
    # Action
    perception = env.reflect(agent, TurnId(0))
    intention = agent.run_turn(perception)
    action = env.physics(intention)
    
    # Assert
    assert "I will walk towards the distant mountain." in intention.content
    assert "The agent begins walking towards the mountain." in action.content
