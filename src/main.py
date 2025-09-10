from .lore_objects import Agent, Environment
from . import config
import os
import shutil


class Game:
    """
    The main game loop.
    """

    def __init__(self):
        self.env = Environment()
        self.agents = [
            Agent(agent["name"], agent["personality"]) for agent in config.AGENTS
        ]
        self.num_turns = config.NUM_TURNS

    def setup(self):
        """
        Initializes the game state and cleans the log directory.
        """
        if config.LOGGING_ENABLED:
            log_dir = ".state_dump"
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            os.makedirs(log_dir)

        print("--- SETUP ---")
        for agent in self.agents:
            perspective = self.env.reflect(agent.agent_name)
            agent.perceive(perspective)
            print(
                f"{agent.agent_name} perception: "
                f"{agent.perception.content if agent.perception else 'None'}"
            )
        print("-------------")

    def main_loop(self):
        """
        The main game loop.
        """
        for i in range(self.num_turns):
            self.env.turn = i
            print(f"--- TURN {i} ---")

            # Agents introspect and intend
            for agent in self.agents:
                agent.introspect(self.env.turn)
                intention = agent.intend(self.env.turn)
                self.env.agents_intentions[agent.agent_name] = intention
                print(f"{agent.agent_name} intention: {intention.content}")

            # Environment processes intentions into actions
            for agent_name, intention in self.env.agents_intentions.items():
                self.env.physics(intention)

            # Environment divines the outcome of the turn
            divination = self.env.divine()
            print(f"Divination: {divination.content}")

            # Agents perceive the new reality
            for agent in self.agents:
                perspective = self.env.reflect(agent.agent_name)
                agent.perceive(perspective)
                print(
                f"{agent.agent_name} perception: "
                f"{agent.perception.content if agent.perception else 'None'}"
            )
            print("-------------")

    def run(self):
        """
        Runs the game.
        """
        self.setup()
        self.main_loop()


if __name__ == "__main__":
    game = Game()
    game.run()
