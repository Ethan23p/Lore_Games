from .lore_objects import Agent, Environment
from .ai_handler import AIHandler
from . import config
import os
import shutil


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

    def _setup_logging(self):
        """
        Cleans and creates the log directory.
        """
        if config.LOGGING_ENABLED:
            log_dir = ".state_dump"
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            os.makedirs(log_dir)

    def setup(self):
        """
        Initializes the game state.
        """
        self._setup_logging()

        for agent in self.agents:
            perspective = self.env.reflect(agent.agent_name)
            agent.perceive(perspective)

    def _run_turn(self, turn_num: int):
        """
        Runs a single turn of the simulation.
        """
        self.env.turn = turn_num
        self.env.advance_turn(self.agents)

    def run(self):
        """
        Runs the game, advancing turns on user input.
        """
        self.setup()
        turn_counter = 0
        try:
            while True:
                self._run_turn(turn_counter)
                input("\nPress Enter to advance to the next turn...")
                turn_counter += 1
        except KeyboardInterrupt:
            print("\nSimulation ended by user.")


if __name__ == "__main__":
    game = Game()
    game.run()
