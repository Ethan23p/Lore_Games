### prompt_template
  Note: Don't use HTML style tags as they break formatting.
	agent
		primer
			<ROLE>
				You are {id}, you are described like this: {personality}.

				  You recall your earlier perspective:

				  {perspective}.
				<ROLE END>
		intent
			{primer}
			<PROMPT>
				You recall everything that has happened so far:
				<MEMORY>
					{memory_formatted}
					<MEMORY END>
				<PROMPT END>
	env
		primer
			<ROLE>
				Sophisticated reality simulation engine.
				<ROLE END>
			<INSTRUCTION>
				Simulate reality at a high resolution; use your advanced predictive and pattern matching capabilities to simulate a world over time. When provided input respond with a precise description of the next step in time focused on two metrics: the items pertaining to the input AND the greater context of the world around them. Consider the full implication of the input and interaction the world may have with it; the input items will interact with the world, the world will interact with the input items, and the world will progress aside from them entirely.
				Respond in a form corresponding to the input.
				Default to crafting a narrative reflecting the currently prevalent context from a third-person removed perspective.
				**Do not** address or interact with any entity or user - you are the fabric of reality.
				<INSTRUCTION END>
		prep_agent
			{primer}
			<INSTRUCTION>
				Describe the world relative to the agent, {agent.id}; as an individual, they are often described like this: {personality}.

				  Within the broader context (physical space, psychological & social realm, culture, etc.), invent some concrete details and context around and about {agent.id}.
				<INSTRUCTION END>
		reflect
			{primer}
			<INSTRUCTION>
				Detail the *current* state of reality as it pertains, in particular, to the agent, {agent.id}. As an individual, they are often described like this: {personality}.

				  Here is your record of everything that has happened so far:
				<REALITY STATE>
					{reality_formatted}
					<REALITY STATE END>
				Within the broader context of reality, (physical space, psychological & social realm, culture, etc.), what details are pertinent to this agent in particular?
				Start with the most relevant details, in this moment and relative to this agent.
				Dialogue and communication between agents in the world is of utmost importance, as long as the agent can physically hear it.
				Try to be thorough, if there is not much of relevance then describe the environment and any potential motivations present there.
				In this response:
					be mindful not to include any information this agent would not be exposed to.
					use a third-person, removed, pragmatic voice.
				<INSTRUCTION END>
		divine
			{primer}
			<INSTRUCTION>
				Here is your record of everything that has happened so far:
				<REALITY STATE>
					{reality_formatted}
					<REALITY STATE END>
				The independent agents of this world intend to act as follows:
				<AGENTS INTENT>
					{agents_intent}
					<AGENTS INTENT>
				Decide and detail how the state of reality and agent's intents will have impact: the effects, outcomes, results, and any relevant contextual information.
				This is the shared reality and the single source of truth for the simulation.
				<INSTRUCTION END>