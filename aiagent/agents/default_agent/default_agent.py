import json
import os
from agents.base_agent import BaseAgent, AgentResponse, Skill


class DefaultAgent(BaseAgent):

    def __init__(self):
        super().__init__('default_agent', '通用智能体')
        self._load_skills()
        self._load_prompt()

    def _load_skills(self):
        skills_path = os.path.join(os.path.dirname(__file__), 'skills', 'skills.json')
        if os.path.exists(skills_path):
            with open(skills_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
                self.skills = [Skill.from_dict(s) for s in skills_data]

    def _load_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'system_prompt.md')
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self._system_prompt = f.read()

    async def execute(self, message: str, context: dict = None, user_permissions=None) -> AgentResponse:
        try:
            result = await self.call_llm(message, context)
            result.skills_used = ['general_query']
            return result
        except Exception as e:
            return AgentResponse(
                response=f"调用LLM失败: {str(e)}",
                agent_id=self.agent_id,
                intent_name='general_query',
                skills_used=['general_query'],
                success=False,
                error=str(e)
            )
