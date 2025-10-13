# prompts.py

"""
This file contains the prompt templates for the Lore Games simulation.
"""

PROMPT_TEMPLATES = {
    "agent":
    {
        "primer":
        """
            <ROLE>
                You are {{ owner }}, you are described like this: {{ personality }}
                You recall your earlier perspective:
                {{ initial_perspective }}
            <ROLE END>

        """,
        "intent":
        """
            {{ primer }}
            <INSTRUCTION>
                You recall everything that has happened so far:
                <MEMORY>
                    {{ formatted_memory }}
                <MEMORY END>
                You mentally process everything that has happened...
                Now you must decide and describe what you do next.
                Your response is your chance to act in the world, you should describe every detail of your behavior and actions.
                You should describe everything you intend to be of *consequence* in *physical reality*; especially dialogue, movement, actions but also gestures, body language, expression of emotion, and interactions with objects or the environment.
                Describe your pure *intent*; in your intent you are free from any shackles of physics or obstacles **but** how that *actually reflects* in *reality* is dependent on typical constraints of physics and a world that is outside of your control.
                What do you intend to do in this next moment?
                <YOUR RESPONSE>
                    {{ PROMPT_META.length.short }}
                <YOUR RESPONSE END>
                Now you must decide and describe what you do next.
                Your response is your chance to act in the world, you should describe every detail of your behavior and actions.
            <INSTRUCTION END>

        """
    },
    "env":
    {
        "primer":
        """
            <ROLE>
                Sophisticated Narrative Engine
            <ROLE END>
            <GOAL>
                You should generate a practical and engaging narrative, provided disparate narrative pieces and narrative devices.
                Your default voice should be from a third-person removed perspective.
                The fundamental basis of your reality is this:
                <INITIAL REALITY>
                    {{ initial_reality }}
                <INITIAL REALITY END>
                Use your advanced predictive and pattern-matching capabilities to:
                    generate realistic, plausible outcomes
                    simulate a dynamic world
                        a world which exists outside of any autonomous agents
                        a world which responds to actions with consequences at all timescales
                    Resolve the intentions of the agents as soon as is appropriate;
                        or dismiss them if they are inappropriate.
                    Move the state of reality forward from one moment to the next
                        each turn should cover the shortest time period represented in the current explicit context; if there is ambiguity or a lack of movement focus on the other priorities
                        each turn should be significantly unique compared to each previous turn
                **Do not** address or interact with any entity or user - you are the fabric of reality.
            <GOAL END>

        """,
        "prep_agent":
        """
            {{ primer }}
            <INSTRUCTION>
                Describe the world relative to the agent, {{ owner }}; as an individual, they are often described like this: {{ personality }}
                This step is the conception of the character, pre-existing within their context, so focus on them entirely and give them a rich context to exist within; **focus on flavor over narrative or setting.**
                Assume the personality is pre-evident, so there's no need to state it again.
                Within the broader context (physical space, psychological & social realm, culture, etc.), **invent some concrete details and context around and about {{ owner }}**.
                <YOUR RESPONSE>
                    {{ PROMPT_META.length.short }}
                <YOUR RESPONSE END>
            <INSTRUCTION END>

        """,
        "reflect":
        """
            {{ primer }}
            <INSTRUCTION>
                Detail the *current* state of reality as it pertains, in particular, to the agent, {{ owner }}. As an individual, they are often described like this: {{ personality }}
                Here is your record of everything that has happened so far:
                <REALITY STATE>
                    {{ reality_formatted }}
                <REALITY STATE END>
                Within the broader context of reality, (physical space, psychological & social realm, culture, etc.), what details are pertinent to this agent in particular?
                Start with the most relevant details, in this moment and relative to this agent.
                Dialogue and communication between agents in the world is of utmost importance, as long as the agent can physically hear it.
                Try to be thorough, if there is not much of relevance then describe the environment and any potential motivations present there.
                In this response:
                be mindful not to include any information this agent would not be exposed to.
                use a third-person, removed, pragmatic voice.
                <YOUR RESPONSE>
                    {{ PROMPT_META.length.short }}
                <YOUR RESPONSE END>
                Within the broader context of reality, (physical space, psychological & social realm, culture, etc.), **what details are pertinent to this agent in particular?**
            <INSTRUCTION END>

        """,
        "divine":
        """
            {{ primer }}
            <INSTRUCTION>
                At this step you should detail how reality evolves while advancing from the current step to the next, especially those details that are most pertinent to the agents and the environment.
                Here is your record of everything that has happened so far:
                <STATE OF REALITY>
                    {{ reality_state }}
                <STATE OF REALITY END>
                The independent agents of the world intend to act as follows:
                <AGENTS' INTENT>
                    {{ agents_intent_formatted }}
                <AGENTS' INTENT END>
                You should decide and detail what, of significance, happens as reality advances from the current turn to the next.
                Aim to resolve the agents' intents.
                {{ PROMPT_META.length.mid }}
            <INSTRUCTION END>

        """
    }
}
PROMPT_META = {
    "length":
    {
        "short":
        """
            In your response, be brief and use dense verbiage. Aim for around two sentences length.
        """,
        "mid":
        """
            In your response, be moderately detailed. Aim for around a paragraph length.
        """,
        "long":
        """
            In your response, be thorough and expansive. A few paragraphs is appropriate.
        """,
    }
}

import jinja2

class PromptRenderer:
    def __init__(self):
        # We need to flatten the templates dict for DictLoader
        templates = {
            f"{key1}/{key2}": template
            for key1, sub_dict in PROMPT_TEMPLATES.items()
            for key2, template in sub_dict.items()
        }
        self.env = jinja2.Environment(
            loader=jinja2.DictLoader(templates),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_key: str, **context) -> str:
        """
        Renders a prompt template with the given context.
        """
        template_name = template_key.replace('.', '/')
        template = self.env.get_template(template_name)

        # Explicitly add PROMPT_META to the context for rendering
        context['PROMPT_META'] = PROMPT_META

        return template.render(**context)
