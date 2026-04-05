import json
import os
from agents.base_agent import BaseAgent, AgentResponse, Skill


class TariffAgent(BaseAgent):

    def __init__(self):
        super().__init__('tariff_agent', '关税政策分析智能体')
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
        if context is None:
            context = {}

        if user_permissions:
            for skill in self.get_enabled_skills():
                if skill.permissions_required:
                    for perm in skill.permissions_required:
                        if not user_permissions.has_permission(perm):
                            return AgentResponse(
                                response="权限不足，无法执行关税分析操作",
                                agent_id=self.agent_id,
                                intent_name='tariff_analysis',
                                skills_used=[],
                                success=False,
                                error=f"缺少必要权限: {perm}",
                                permissions_checked=skill.permissions_required
                            )

            if hasattr(user_permissions, 'data_scopes'):
                has_scope = any(user_permissions.has_data_scope('tariff:*') or
                               user_permissions.has_data_scope('*') for _ in [1])
                if not has_scope and user_permissions.data_scopes:
                    return AgentResponse(
                        response="数据范围权限不足，无法访问关税数据",
                        agent_id=self.agent_id,
                        intent_name='tariff_analysis',
                        skills_used=[],
                        success=False,
                        error="数据范围权限不足",
                        data_scope_used=user_permissions.data_scopes
                    )

        try:
            result = await self.call_llm(message, context)
            result.permissions_checked = ['tariff:read'] if user_permissions else []
            result.data_scope_used = ['tariff:*'] if user_permissions else []
            result.skills_used = ['tariff_analysis']
            return result
        except Exception as e:
            return AgentResponse(
                response=f"调用LLM失败: {str(e)}",
                agent_id=self.agent_id,
                intent_name='tariff_analysis',
                skills_used=['tariff_analysis'],
                success=False,
                error=str(e)
            )
