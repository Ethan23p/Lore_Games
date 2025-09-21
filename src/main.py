from .lore_objects import Agent, Environment
from .ai_handler import AIHandler
from . import config
from .flows import MainFlow, SimpleFlow
import os
import shutil
import asyncio


class Game:
    """
    The main game loop.
    """

    def __init__(self):
        ai_handler = AIHandler()
        self.env = Environment(
            ai_handler=ai_handler, initial_reality=config.INITIAL_REALITY
        )
        self.agents = [
            Agent(agent["name"], agent["personality"], ai_handler=ai_handler)
            for agent in config.AGENTS
        ]

        if config.FLOW == "main":
            self.flow = MainFlow()
        elif config.FLOW == "simple":
            self.flow = SimpleFlow()
        else:
            raise ValueError(f"Unknown flow type: {config.FLOW}")

    def _setup_logging(self):
        """
        Cleans and creates the log directory.
        """
        if config.LOGGING_ENABLED:
            log_dir = ".state_dump"
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            os.makedirs(log_dir)

    async def setup(self):
        """
        Initializes the game state.
        """
        self._setup_logging()
        
        # Have all agents perceive the initial state concurrently
        perception_tasks = [self.env.reflect(agent.agent_name) for agent in self.agents]
        perspectives = await asyncio.gather(*perception_tasks)
        for agent, perspective in zip(self.agents, perspectives):
            agent.perceive(perspective)


    async def run_turn(self, turn_num: int):
        """
        Runs a single turn of the simulation.
        """
        self.env.turn = turn_num
        await self.flow.execute_turn(self.env, self.agents)


async def main():
    """
    The main entry point for the asynchronous simulation.
    """
    game = Game()
    await game.setup()
    turn_counter = 1
    try:
        while True:
            await game.run_turn(turn_counter)
            await asyncio.to_thread(input, "\nPress Enter to advance to the next turn...")
            turn_counter += 1
    except KeyboardInterrupt:
        print("\nSimulation ended by user.")


if __name__ == "__main__":
    asyncio.run(main())