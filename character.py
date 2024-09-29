from agent import Agent
from mistralai import ToolCall


class Character:

    def __init__(self, agent: Agent, bio: str):
        self.agent = agent
        self.bio = bio

    async def get_response(self, messages: list[dict], tools: list[dict] = []) -> tuple[str, list[ToolCall]]:
        response, actions = await self.agent.complete(messages, tools)
        return response, actions
