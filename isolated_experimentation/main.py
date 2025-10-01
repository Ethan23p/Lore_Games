# main.py

def __main__():

    def init():
        app()
        app.init_agents()
        app.init_env()
        app.prime_agents()

    def main_loop():
        app.agent_turn()
        app.env_turn()
