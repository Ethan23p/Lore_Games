from abc import ABC, abstractmethod
from typing import List
from .lore_objects import Environment, Agent
import asyncio


class Flow(ABC):
    """
    Abstract base class for a simulation flow.
    """

    async def _perceive_concurrently(self, env: Environment, agents: List[Agent]):
        """
        Helper to have all agents perceive the environment concurrently.
        """
        perception_tasks = [env.reflect(agent.agent_name) for agent in agents]
        perspectives = await asyncio.gather(*perception_tasks)
        for agent, perspective in zip(agents, perspectives):
            agent.perceive(perspective)

    @abstractmethod
    async def execute_turn(self, env: Environment, agents: List[Agent]):
        """
        Executes a single turn of the simulation using a specific flow.
        """
        raise NotImplementedError


class MainFlow(Flow):
    """
    The main simulation flow, involving introspection, intention, and physics.
    """

    async def _agent_turn(self, agent: Agent, env: Environment):
        """
        Executes the full perceive->introspect->intend->physics sequence for a single agent.
        """
        # 1. Perceive
        perspective = await env.reflect(agent.agent_name)
        agent.perceive(perspective)

        # 2. Introspect
        await agent.introspect(env.turn)

        # 3. Intend
        intention = await agent.intend(env.turn)
        env.agents_intentions[agent.agent_name] = intention

        # 4. Physics
        await env.physics(intention)

    async def execute_turn(self, env: Environment, agents: List[Agent]):
        # Run the full P-I-I-P sequence for all agents concurrently
        await asyncio.gather(*[self._agent_turn(agent, env) for agent in agents])

        # Environment divines the outcome of the turn
        await env.divine(env.agents_actions)


class SimpleFlow(Flow):
    """
    A simplified flow for quick testing and demos.
    """

    async def execute_turn(self, env: Environment, agents: List[Agent]):
        # Agents perceive the current reality and form a plan concurrently
        await self._perceive_concurrently(env, agents)

        current_reality = env.reality[-1].content if env.reality else env.initial_reality
        plan_tasks = [agent.plan(env.turn, current_reality) for agent in agents]
        plans = await asyncio.gather(*plan_tasks)

        for agent, plan in zip(agents, plans):
            env.agents_plans[agent.agent_name] = plan

        # Environment divines a new reality directly from plans
        await env.divine(env.agents_plans)