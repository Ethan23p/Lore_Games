import asyncio
from mcp_agent.core.fastagent import FastAgent
from src.lore_types import Agent, Environment, TurnId
from src.ai_handler import AIHandler
from src.state_logger import StateLogger

# --- Application Setup ---

fast = FastAgent("Lore Games Agent")

@fast.agent(
  instruction="You are a helpful assistant, ready to help with lore and games."
)
async def main():
  """
  Main entry point for the agent.

  This will start the agent in interactive mode.
  """
  async with fast.run() as agent:
    await agent.interactive()

# --- Simulation Mock-up ---

def run_simulation_mockup():
    """
    This function initializes and runs the simulation by calling the
    encapsulated turn logic in the Environment class.
    """
    # --- Configuration Stub ---
    config = {
        "enable_state_logging": True,
        "initial_reality": "A vast, empty plain stretches under a grey sky.",
        "agents": [
            {"name": "Alice", "personality": "curious"},
            {"name": "Bob", "personality": "cautious"}
        ],
        "max_turns": 3
    }

    print("--- Initializing Simulation ---")

    # Initialization
    logger = StateLogger() if config["enable_state_logging"] else None
    ai_handler = AIHandler()

    agents = [
        Agent(
            name=p["name"],
            personality=p["personality"],
            ai_handler=ai_handler,
            logger=logger
        ) for p in config["agents"]
    ]
    env = Environment(
        agents=agents,
        initial_reality=config["initial_reality"],
        ai_handler=ai_handler,
        logger=logger
    )
    turn_counter = TurnId(0)

    print(f"Initialized {len(agents)} agents and environment.")
    if logger:
        print(f"State logging is enabled. Output will be in '{logger.output_dir}/'")


    # --- Main Loop ---
    print("\n--- Starting Main Loop ---")
    while turn_counter < config["max_turns"]:
        print(f"\n--- Turn {turn_counter} ---")

        if logger:
            logger.clear_turn_logs()

        env.run_turn(turn_counter)

        turn_counter = TurnId(turn_counter + 1)

if __name__ == "__main__":
    # We are not running the FastAgent for now, just the simulation mockup.
    # print("Starting Lore Games Agent...")
    # asyncio.run(main())

    run_simulation_mockup()