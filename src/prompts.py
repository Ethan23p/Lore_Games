# prompts.py

"""
This file contains the prompt templates for the Lore Games simulation.
"""
from .config import get_config
import jinja2

PROMPT_INITIAL = {
    "initial_reality": "A sprawling shantytown built on the interconnected rooftops of a sleeping city. An unwanted inheritance saddles Charlie with a derelict hovel that's more of a hazard than a home. But this cursed gift contains the shantytown's greatest opportunity - a concealed stairway into a lost dungeon - and Charlie begins to wonder if there's a fortune to be made from selling tickets to the peril below.",
    "agent_definitions": [
        {
            "name": "Charlie",
            "personality": "A goblin which once survived being thrown into a ceremonial bonfire; Charlie has a new appreciation for life.",
        },
        {
            "name": "Delta",
            "personality": "A mechanoid which speaks through a lo-fi speaker, Delta is fascinated by biology.",
        },
    ]
}

PROMPT_TEMPLATES = {
    "agent":
    {
        "primer":
        """
<ROLE>
    You are {{ entity_id }}, you are described like this: {{ personality }}
    You recall your earlier perspective:
        <INITIAL PERSPECTIVE>
            {{ initial_perspective }}
        <INITIAL PERSPECTIVE END>
<ROLE END>
""",
        "intent":
        """
{{ primer }}
<PROMPT>
    At this step you should describe your intention for the current turn.
    You recall everything that has happened so far:
        <MEMORY>
            {{ formatted_memory }}
        <MEMORY END>
    You should describe your intention for the current turn based on recent happenings.
    In your response, you should:
        describe what you intend to be of consequence in physical reality.
        especially:
            dialogue
            movement
            actions
            interactions
        bias toward *action*. (As opposed to inaction.)
    You are free to describe your pure intent, though the outcome is still subject to typical constraints such as: physics, a world outside of your control, the free will of other beings.
    What do you intend to do during this turn?
<PROMPT END>
"""
    },
    "env":
    {
        "primer": {
            "narrative_writer":
            """
<ROLE>
    Sophisticated Narrative Writer
<ROLE END>
<GOAL>
    You should write an engaging and plausible narrative within the given reality and considering the provided narrative beats.
    Your default voice should be in a third-person removed perspective.
    The fundamental seed of this reality:
        <INITIAL REALITY>
            {{ initial_reality }}
        <INITIAL REALITY END>
    Autonomous agents exist within this reality, you will be cooperatively crafting the story as they establish intentions within their local context.
    Use your vast knowledge of fiction, history, mythology to:
        Write engaging, interesting narrative content.
        Write self-consistent, plausible content.
        Build a dynamic world which:
            Exists outside of any particular narrative arc.
            Responds to actions with consequences, and at all timescales.
            Is consistent with any *established reality* and resolves the *intentions of the agents*.
    **Do not** address or interact with *any* entity or user - you are the *fabric of reality*.
<GOAL END>
""",
            "simulation_engine":
            """
<ROLE>
    Sophisticated Simulation Engine
<ROLE END>
<GOAL>
    You should generate a consistent, thorough simulation of the given reality.
    Your default voice should be from a third-person removed point of view.
    The fundamental basis of your reality is this:
        <INITIAL REALITY>
            {{ initial_reality }}
        <INITIAL REALITY END>
    Autonomous agents exist within this reality; you will be establishing a ground truth reality while integrating their intentions within their local context.
    Use your advanced predictive and pattern-matching capabilities to:
        generate realistic, self-consistent outcomes
        advances time forward, one turn at a time
        Simulate a dynamic world which:
            exists outside of any autonomous agents
            a world which responds to actions with reactions, consequences at all timescales
            Is consistent with any *established reality* and resolves the *intentions of the agents*.
    **Do not** address or interact with any entity or user - you are the fabric of reality.
<GOAL END>
"""
        },
        "prep_agent":
        """
{{ primer }}
<INSTRUCTION>
    Describe the world, broadly, relative to the agent, {{ owner }}.
    As an individual, they are often described like this: {{ personality }}
    This step is introductory, invent details which are interesting and define their character and their context, broadly. Consider various angles:
        physical space
        the psychological environment
        the social realm
        their culture
        etc.
<INSTRUCTION END>
<IN YOUR RESPONSE>
    {{ PROMPT_META.length.short }}
<IN YOUR RESPONSE END>
""",
        "reflect":
        """
{{ primer }}
<INSTRUCTION>
    Describe the state of the environment during the current turn relative to the agent: {{ owner }}.
    As an individual, they are often described like this: {{ personality }}
    Here is your record of everything that has happened so far:
        <FULL STATE OF REALITY>
            {{ reality_formatted }}
        <FULL STATE OF REALITY END>
    Considering:
        most recent events
        physical space
        their psychological environment
        the social realm
        their culture
    Describe the current state of the environment relative to {{ owner }}. Be mindful:
        of what is most relevant to this agent at this moment
        that dialogue and communication between agents is of utmost importance (assuming they can possibly perceive it)
        to clearly communicating the impact/outcome of their actions
        that you are thorough and, if there is little to say, then you can describe potential motivations, then you can describe the environment
        not to include any information that {{ owner }} would not be able to perceive or would not be exposed to
    What details are most pertinent to this agent?
<INSTRUCTION END>
<IN YOUR RESPONSE>
    {{ PROMPT_META.length.short }}
<IN YOUR RESPONSE END>
""",
        "divine":
        """
{{ primer }}
<INSTRUCTION>
    At this step you should advance time by one turn; detail how reality evolves due to the events of the current turn, especially that which is pertinent to the agents or environment.
    Here is your record of everything that has happened so far:
        <STATE OF REALITY>
            {{ reality_state }}
        <STATE OF REALITY END>
    The autonomous agents have decided their intentions for this turn:
        <AGENTS' INTENT>
            {{ agents_intent_formatted }}
        <AGENTS' INTENT END>
    You are establishing the shared world, the single source of truth within reality.
    You should advance time by one turn; detail how reality evolves due to the events of the current turn considering the outcomes of the intentions as well as the greater context of the dynamic world.
<INSTRUCTION END>
<PARAMETERS>
    {{ PROMPT_META.length.mid }}
<PARAMETERS END>
"""
    }
}
PROMPT_META = {
    "length":
    {
        "short": "In your response, be brief and use dense verbiage. Aim for around two sentences in length.",
        "mid": "In your response, be moderately detailed. Aim for around a paragraph in length.",
        "long": "In your response, be thorough and expansive. A few paragraphs is appropriate. (But not more.)"
    }
}

def flatten_templates(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + '/' + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_templates(v, new_key))
        else:
            items.append((new_key, v))
    return items

class PromptRenderer:
    def __init__(self):
        # We need to flatten the templates dict for DictLoader
        templates = dict(flatten_templates(PROMPT_TEMPLATES))
        self.env = jinja2.Environment(
            loader=jinja2.DictLoader(templates),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.config = get_config()

    def render(self, template_key: str, **context) -> str:
        """
        Renders a prompt template with the given context.
        """
        template_name = template_key.replace('.', '/')

        # Special handling for the generic 'env.primer' key to select the correct style
        if template_name == 'env/primer':
            primer_style = self.config['environment']['primer_style']
            primer_key = f'env/primer/{primer_style}'
            template = self.env.get_template(primer_key)
            return template.render(**context)

        template = self.env.get_template(template_name)

        # Explicitly add PROMPT_META to the context for rendering
        context['PROMPT_META'] = PROMPT_META

        return template.render(**context)