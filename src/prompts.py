class PromptLibrary:
    """
    A library of prompt templates for the simulation.
    """

    TEMPLATES = {
        "primers": {
            "agent": "You are {agent_name}. You have been described like so: {personality}.",
            "environment": (
                "You are a sophisticated AI tasked with simulating an imagined world with consistency, "
                "coherence, and attention to detail. All inputs expand the state of this world, and "
                "your job is to describe realistic outcomes as they unfold."
            ),
        },
        "main_flow": {
            "perspective": (
                "Your task now is to describe in detail what {agent_name} perceives in the present moment. "
                "Emphasize the most relevant sights, sounds, feelings, and conditions specific to their "
                "perspective, maintaining coherence with the world's history."
                "The state of the world, up to this point: {reality}"
            ),
            "introspection": (
                "You are {agent_name}, you've been described as: {personality}.\n\n"
                "This is your personal retelling of everything that has happened so far:\n{memory}\n\n"
                "Given the following new information:\n> {perception}\n\n"
                "Taking into consideration these latest happenings, private matters that may have come up so far, "
                "your personal motivations:\nWhat do you add to your personal retelling, your memory, for this moment?"
            ),
            "intention": (
                "You are {agent_name}, you've been described as: {personality}.\n\n"
                "This is your personal retelling of everything that has happened so far:\n{memory}\n\n"
                "This is what's happening and what's most relevant to you, in the current moment:\n> {perception}\n\n"
                "Taking into consideration these latest happenings, private matters that may have come up so far, "
                "your personal motivations:\nWhat do you intend to do next, in the physical realm?"
            ),
            "action": (
                "You will be responding with either 'true' or 'false'.\n\n"
                "This is the narrative detailing of everything that has happened so far:\n{reality}\n\n"
                "The agent, {intent_owner}, intends to do the following:\n> {intent}\n\n"
                "Your task is to evaluate if the intent expressed by {intent_owner} is physically possible. "
                "You have two possible responses and should choose one, respond with:\n"
                "'true' if the intended action is at least possible.\n"
                "'false' if the intended action is not possible at all."
            ),
            "divination": (
                "This is the narrative detailing of everything that has happened so far:\n{reality}\n\n"
                "The independent agents of this world intend to act as follows:\n> {agents_intent}\n\n"
                "The agents' intents should succeed, but may fail. You must decide in the service of "
                "consistency, coherence, conflicting forces. The agents' intents may directly oppose "
                "each other; the outcome of this, too, you must decide.\n\n"
                "Your task now is to decide how the above reality is impacted by the actions of the "
                "agents, the passage of time."
            ),
        },
        "simple_flow": {
            "reflect": (
                "Setting:\n{reality}\n"
                "You must describe the world relative to the agent, {agent_name}; as an individual, "
                "they are often described like this: {personality}.\n"
                "Within the broader context (physical space, psychological & social realm, etc.), "
                "what is the unspoken details and context around and about {agent_name}?"
            ),
            "planning": (
                "This is the world around you:\n{reality}\n"
                "Within this latest context, what do you do next?"
            ),
            "divination": (
                "This is the narrative detailing of everything that has happened so far:\n{reality}\n\n"
                "The independent agents of this world intend to act as follows:\n> {agents_intent}\n\n"
                "The agents' intents should succeed, but may fail. You must decide in the service of "
                "consistency, coherence, conflicting forces. The agents' intents may directly oppose "
                "each other; the outcome of this, too, you must decide.\n\n"
                "Your task now is to decide how the above reality is impacted by the actions of the "
                "agents, the passage of time."
            ),
        },
    }
