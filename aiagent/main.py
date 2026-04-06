from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import uvicorn
from pathlib import Path

ENV = os.environ.get('ENVIRONMENT', 'local')
ENV_FILE = Path(__file__).parent / f'.env.{ENV}'

def load_env_file():
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env_file()

from core.intent_classifier import IntentClassifier
from services.agent_factory import AgentFactory
from security.auth_service import AuthService

app = FastAPI(title="AI Agent Gateway", version="1.0.0")

classifier = IntentClassifier()
agent_factory = AgentFactory()
auth_service = AuthService()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ClassifyRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    intent: Dict[str, Any]
    agent_id: str
    agent_name: str
    skills_used: List[str]
    success: bool
    user_info: Optional[Dict[str, Any]] = None
    permissions_checked: List[str] = []
    data_scope_used: List[str] = []


@app.get("/")
async def root():
    return {"message": "AI Agent Gateway API", "version": "1.0.0"}


@app.post("/api/ai/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    user_permissions = None
    user_info = None

    TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

    if authorization:
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        if token:
            try:
                token_data = auth_service.validate_token(token)
                user_permissions = token_data.to_permissions()
                user_info = {
                    "user_id": token_data.user_id,
                    "username": token_data.username,
                    "permissions": token_data.permissions,
                    "data_scopes": token_data.data_scopes
                }

                if user_permissions.is_expired():
                    raise HTTPException(status_code=401, detail="Token已过期")

            except ValueError as e:
                raise HTTPException(status_code=401, detail=str(e))

    if TEST_MODE and user_permissions is None:
        from security.auth_service import UserPermissions
        user_permissions = UserPermissions(
            user_id="test_user",
            username="test_user",
            permissions=["*"],
            data_scopes=["*"]
        )
        user_info = {
            "user_id": "test_user",
            "username": "test_user",
            "permissions": ["*"],
            "data_scopes": ["*"],
            "test_mode": True
        }

    intent = await classifier.classify(req.message)
    agent = agent_factory.get_agent(intent.agent_id)
    result = await agent.execute(req.message, req.context or {}, user_permissions)

    agent_info = agent.get_info()

    return ChatResponse(
        response=result.response,
        intent={
            'intent_name': intent.intent_name,
            'confidence': intent.confidence,
            'keywords': intent.keywords
        },
        agent_id=agent_info['agent_id'],
        agent_name=agent_info['agent_name'],
        skills_used=result.skills_used,
        success=result.success,
        user_info=user_info,
        permissions_checked=result.permissions_checked,
        data_scope_used=result.data_scope_used
    )


@app.post("/api/ai/classify")
async def classify(
    req: ClassifyRequest,
    authorization: Optional[str] = Header(None)
):
    intent = await classifier.classify(req.message)

    user_info = None
    if authorization:
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        try:
            token_data = auth_service.validate_token(token)
            user_info = {
                "user_id": token_data.user_id,
                "username": token_data.username
            }
        except ValueError:
            pass

    result = {
        'intent_name': intent.intent_name,
        'confidence': intent.confidence,
        'keywords': intent.keywords,
        'agent_id': intent.agent_id
    }

    if user_info:
        result['user_info'] = user_info

    return result


@app.get("/api/ai/agents")
async def list_agents():
    return agent_factory.list_agents()


@app.get("/api/ai/agent/{agent_id}")
async def get_agent(agent_id: str):
    agent = agent_factory.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.get_info()


@app.get("/api/ai/agent/{agent_id}/skills")
async def get_agent_skills(agent_id: str):
    agent = agent_factory.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.get_info()['skills']


@app.get("/api/ai/agent/{agent_id}/mcp")
async def get_agent_mcp(agent_id: str):
    import json
    import os

    agent = agent_factory.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    mcp_path = None
    if agent_id == 'tariff_agent':
        mcp_path = os.path.join(os.path.dirname(__file__), 'agents', 'tariff_agent', 'mcp', 'mcp_config.json')
    elif agent_id == 'default_agent':
        mcp_path = os.path.join(os.path.dirname(__file__), 'agents', 'default_agent', 'mcp', 'mcp_config.json')

    if mcp_path and os.path.exists(mcp_path):
        with open(mcp_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    raise HTTPException(status_code=404, detail="MCP配置未找到")


@app.post("/api/auth/validate")
async def validate_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="缺少Authorization头")

    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization

    try:
        token_data = auth_service.validate_token(token)
        return {
            "valid": True,
            "user_id": token_data.user_id,
            "username": token_data.username,
            "permissions": token_data.permissions,
            "data_scopes": token_data.data_scopes,
            "expires_at": token_data.expires_at.isoformat() if token_data.expires_at else None
        }
    except ValueError as e:
        return {
            "valid": False,
            "error": str(e)
        }


@app.post("/api/auth/create_test_token")
async def create_test_token(user_id: str, username: str, permissions: str, data_scopes: str):
    """
    创建测试用Token（仅用于开发和测试）
    permissions: 逗号分隔，如 "tariff:read,policy:read"
    data_scopes: 逗号分隔，如 "tariff:*,policy:*"
    """
    perm_list = [p.strip() for p in permissions.split(",") if p.strip()]
    scope_list = [s.strip() for s in data_scopes.split(",") if s.strip()]

    token = AuthService.create_test_token(user_id, username, perm_list, scope_list)
    return {"token": token}


if __name__ == "__main__":
    port = int(os.environ.get('AI_AGENT_PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)