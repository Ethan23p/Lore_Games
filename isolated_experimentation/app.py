# app.py
class app:

    def config():

    def __init__():
        config()
        ai_handler()

    def init_agents():
        for agent in config.initial_agents:
            new_agent = agent(agent.id, agent.personality)
            agents[agent.id = new_agent]

    def init_env():
        env(config.env)

    def prime_agents():
        for agent in agents
            agent_initial_perspective = env.initial_reflection(agent.id, agent.personality)
            agent.prime(agent_initial_perspective)

    def agent_turn():
        for agent in agents
            agent_perspective = env.reflect(agent.id, agent.personality)
            agent.add_memory(agent_perspective)
            agent_intention = agent.intent()
            env.add_intention(agent.id, agent_intention)

    def env_turn():
        env.divine()
