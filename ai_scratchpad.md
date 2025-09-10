# programmatic v6

## Objects

 interaction
  interaction.init()
   owner: entity name
   birth_turn: turn
   content: string
   prompt: string
  interaction.prompt()
  interaction.generate()
  subclasses:
   perspective
    prompt = "Given [reality], what does [agent name] perceive at this moment?"
   perception
   introspection
    prompt =
     "You are [agent name], you've been described as [personality]."
     "Your memory of what has happened so far: [memory]"
     "What you have noticed recently: [perception]"
     "Consider these latest events, private matters, your motivations. What do you want to add to your memory?"
   intention
    prompt =
     "You are [agent name], you've been described as [personality]."
     "What has happened so far: [memory]"
     "What you've noticed recently: [perception]"
     "What do you *intend* to do next, in the physical realm? If your intent is conceivable, you will attempt to execute; be mindful that if your intent is not possible, you will effectively do nothing at all."
   action
    prompt = "Given [reality], can [intent.owner] do [intent]?"
   divination
    prompt = "Given [reality] and the agents' intention to do the following, what happens next? [agents' actions]"
 agent
  agent.init()
   agent name: string
   personality: string
   memory: list[introspection]
  agent.perceive(perspective) -> perception # blindly accept currently primed perspective.
   agent.perception = perspective
  agent.introspect() -> introspection # integrate latest events, consider private matters, consider motivations, consider personality.
   introspection = agent.introspect.generate(prompt)
   memory[current_turn] = introspection
  agent.intent() -> intention # put forward intention within the physical, simulated realm.
   intention = agent.intent.generate(prompt)
   env.physics(agent name, intention)
 environment
  env.init()
   reality: list[divinations]
   cause-and-effect ledger
    agents' intentions: dict[owner]
    agents' actions: dict[owner]
  env.physics(intention) -> action # Simply evaluate if stated intention is conceivable or not; if so, passes it through, if not, express idleness, indecision, or a freeze reflex.
   is_possible: bool = env.physics.evaluate(prompt)
    if [possible] then
     action = intention
    else
     action = idle
   agents' actions[intent.owner] = action
  env.divine(agents' actions) -> divination # Taking into consideration all agents' intentions in equal parts, what happens next.
   divination = env.divine.generate(prompt)
   reality[current_turn] = divination
  env.reflect(agent name) -> perspective # Considering the state of the environment, especially pertaining to this agent, what would the agent perceive starting with events and status which are most salient.
   pespective = env.reflect.generate(prompt)
   agent.perceive(perspective)
 AI handler # 100% using dummy AI for the initial bulk of building.
  ai handler.generate(prompt: string)

## Logical Flow

  init()
   env.init()
   for each: agent
    agent.init()
    env.reflect(agent name)
   main_loop()
  main_loop()
   for each: agent
    agent.introspect()
    agent.intent()
   env.divine()
   for each: agent
    env.reflect(agent name)

## Implementation Notes
