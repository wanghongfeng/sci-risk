from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import json


@dataclass
class UserPermissions:
    user_id: str
    username: str
    permissions: List[str] = field(default_factory=list)
    data_scopes: List[str] = field(default_factory=list)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_permission(self, permission: str) -> bool:
        if permission in self.permissions:
            return True
        wildcard = permission.split(':')[0] + ':*'
        return wildcard in self.permissions or '*' in self.permissions

    def has_data_scope(self, scope: str) -> bool:
        if scope in self.data_scopes:
            return True
        if '*' in self.data_scopes:
            return True
        prefix = scope.split(':')[0]
        return f"{prefix}:*" in self.data_scopes

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


@dataclass
class TokenData:
    token: str
    user_id: str
    username: str
    permissions: List[str]
    data_scopes: List[str]
    issued_at: datetime
    expires_at: datetime

    def to_permissions(self) -> UserPermissions:
        return UserPermissions(
            user_id=self.user_id,
            username=self.username,
            permissions=self.permissions,
            data_scopes=self.data_scopes,
            expires_at=self.expires_at
        )


class AuthService:
    """
    认证服务 - 验证Token并提取用户权限
    伪装实现：支持 JWT 和简单Token两种模式
    """

    def __init__(self, secret_key: str = "your-secret-key-change-in-production"):
        self.secret_key = secret_key
        self.algorithm = "HS256"

    def validate_token(self, token: str) -> TokenData:
        """
        验证Token并返回用户权限信息
        抛出异常如果Token无效
        """
        if not token:
            raise ValueError("Token不能为空")

        if token.startswith("mock_"):
            return self._parse_mock_token(token)

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenData(
                token=token,
                user_id=payload.get("user_id", ""),
                username=payload.get("username", ""),
                permissions=payload.get("permissions", []),
                data_scopes=payload.get("data_scopes", []),
                issued_at=datetime.fromtimestamp(payload.get("iat", 0)),
                expires_at=datetime.fromtimestamp(payload.get("exp", 0))
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token已过期")
        except jwt.InvalidTokenError:
            raise ValueError("无效的Token")

    def _parse_mock_token(self, token: str) -> TokenData:
        """
        解析Mock Token格式: mock_userId_username_permission1,permission2_scope1,scope2
        示例: mock_001_zhangsan tariff:read,policy:read tariff:*,policy:*
        """
        parts = token[5:].split("_")
        if len(parts) < 3:
            raise ValueError("Mock Token格式错误")

        user_id = parts[0]
        username = parts[1]
        permissions = parts[2].split(",") if parts[2] else []
        data_scopes = parts[3].split(",") if len(parts) > 3 and parts[3] else []

        now = datetime.now()
        return TokenData(
            token=token,
            user_id=user_id,
            username=username,
            permissions=permissions,
            data_scopes=data_scopes,
            issued_at=now,
            expires_at=now + timedelta(hours=24)
        )

    def check_skill_permission(self, user_perms: UserPermissions, skill_required_perms: List[str]) -> bool:
        """
        检查用户是否有技能所需的权限
        """
        for required in skill_required_perms:
            if not user_perms.has_permission(required):
                return False
        return True

    def check_data_scope(self, user_perms: UserPermissions, required_scope: str) -> bool:
        """
        检查用户是否有访问特定数据范围的权限
        """
        return user_perms.has_data_scope(required_scope)

    @staticmethod
    def create_test_token(user_id: str, username: str, permissions: List[str], data_scopes: List[str]) -> str:
        """
        创建测试用Token（仅用于开发和测试）
        """
        now = datetime.now()
        payload = {
            "user_id": user_id,
            "username": username,
            "permissions": permissions,
            "data_scopes": data_scopes,
            "iat": now,
            "exp": now + timedelta(hours=24)
        }
        return jwt.encode(payload, "test-secret", algorithm="HS256")
