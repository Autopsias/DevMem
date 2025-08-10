from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
import jwt
import json
import hashlib
import secrets
from enum import Enum
import logging

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

@dataclass
class Role:
    name: str
    permissions: Set[Permission]
    description: str

@dataclass
class User:
    id: str
    username: str
    role: str
    last_login: Optional[datetime]
    mfa_enabled: bool
    active: bool

@dataclass
class AccessToken:
    token: str
    user_id: str
    expires_at: datetime
    scope: Set[Permission]

class AccessControl:
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.active_tokens: Dict[str, AccessToken] = {}
        self.logger = logging.getLogger("access_control")
        
        # Initialize default roles
        self._initialize_default_roles()
        
    def _initialize_default_roles(self) -> None:
        """Initialize default role configuration"""
        self.roles = {
            "admin": Role(
                name="admin",
                permissions={
                    Permission.READ,
                    Permission.WRITE,
                    Permission.EXECUTE,
                    Permission.ADMIN
                },
                description="Full system access"
            ),
            "developer": Role(
                name="developer",
                permissions={
                    Permission.READ,
                    Permission.WRITE,
                    Permission.EXECUTE
                },
                description="Development access"
            ),
            "operator": Role(
                name="operator",
                permissions={
                    Permission.READ,
                    Permission.EXECUTE
                },
                description="Operation and monitoring access"
            ),
            "reader": Role(
                name="reader",
                permissions={Permission.READ},
                description="Read-only access"
            )
        }
        
    def create_user(
        self,
        username: str,
        role: str,
        mfa_enabled: bool = False
    ) -> User:
        """Create a new user with specified role"""
        if role not in self.roles:
            raise ValueError(f"Invalid role: {role}")
            
        user_id = self._generate_user_id(username)
        
        user = User(
            id=user_id,
            username=username,
            role=role,
            last_login=None,
            mfa_enabled=mfa_enabled,
            active=True
        )
        
        self.users[user_id] = user
        return user
        
    def deactivate_user(self, user_id: str) -> None:
        """Deactivate a user"""
        if user_id not in self.users:
            raise ValueError(f"User not found: {user_id}")
            
        self.users[user_id].active = False
        self._revoke_user_tokens(user_id)
        
    def create_role(
        self,
        name: str,
        permissions: Set[Permission],
        description: str
    ) -> Role:
        """Create a new role"""
        if name in self.roles:
            raise ValueError(f"Role already exists: {name}")
            
        role = Role(
            name=name,
            permissions=permissions,
            description=description
        )
        
        self.roles[name] = role
        return role
        
    def update_role_permissions(
        self,
        role_name: str,
        permissions: Set[Permission]
    ) -> None:
        """Update permissions for a role"""
        if role_name not in self.roles:
            raise ValueError(f"Role not found: {role_name}")
            
        self.roles[role_name].permissions = permissions
        
        # Revoke tokens for affected users
        affected_users = [
            user_id
            for user_id, user in self.users.items()
            if user.role == role_name
        ]
        for user_id in affected_users:
            self._revoke_user_tokens(user_id)
            
    def generate_access_token(
        self,
        user_id: str,
        mfa_code: Optional[str] = None
    ) -> AccessToken:
        """Generate access token for a user"""
        if user_id not in self.users:
            raise ValueError(f"User not found: {user_id}")
            
        user = self.users[user_id]
        if not user.active:
            raise ValueError("User is not active")
            
        if user.mfa_enabled and not mfa_code:
            raise ValueError("MFA code required")
            
        if user.mfa_enabled and not self._validate_mfa(user_id, mfa_code):
            raise ValueError("Invalid MFA code")
            
        # Get user's permissions from role
        role = self.roles[user.role]
        
        # Generate JWT token
        expiration = datetime.now() + timedelta(hours=8)
        token_data = {
            "sub": user_id,
            "scope": [p.value for p in role.permissions],
            "exp": int(expiration.timestamp())
        }
        
        token = jwt.encode(
            token_data,
            self._get_signing_key(),
            algorithm="HS256"
        )
        
        # Create access token
        access_token = AccessToken(
            token=token,
            user_id=user_id,
            expires_at=expiration,
            scope=role.permissions
        )
        
        # Store active token
        self.active_tokens[token] = access_token
        
        # Update last login
        self.users[user_id].last_login = datetime.now()
        
        return access_token
        
    def validate_token(self, token: str) -> Optional[AccessToken]:
        """Validate an access token"""
        try:
            # Verify JWT signature and expiration
            token_data = jwt.decode(
                token,
                self._get_signing_key(),
                algorithms=["HS256"]
            )
            
            # Check if token is active
            if token not in self.active_tokens:
                return None
                
            access_token = self.active_tokens[token]
            
            # Verify token has not expired
            if access_token.expires_at < datetime.now():
                self._revoke_token(token)
                return None
                
            return access_token
            
        except jwt.InvalidTokenError:
            return None
            
    def check_permission(
        self,
        token: str,
        required_permission: Permission
    ) -> bool:
        """Check if token has required permission"""
        access_token = self.validate_token(token)
        if not access_token:
            return False
            
        return required_permission in access_token.scope
        
    def revoke_token(self, token: str) -> None:
        """Revoke an access token"""
        if token in self.active_tokens:
            self._revoke_token(token)
            
    def _revoke_token(self, token: str) -> None:
        """Internal method to revoke a token"""
        if token in self.active_tokens:
            del self.active_tokens[token]
            
    def _revoke_user_tokens(self, user_id: str) -> None:
        """Revoke all tokens for a user"""
        tokens_to_revoke = [
            token
            for token, access_token in self.active_tokens.items()
            if access_token.user_id == user_id
        ]
        for token in tokens_to_revoke:
            self._revoke_token(token)
            
    def _generate_user_id(self, username: str) -> str:
        """Generate unique user ID"""
        timestamp = datetime.now().timestamp()
        random = secrets.token_hex(8)
        data = f"{username}-{timestamp}-{random}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
        
    def _get_signing_key(self) -> str:
        """Get key for signing tokens"""
        # In production, this would load from secure storage
        return "your-256-bit-secret"
        
    def _validate_mfa(self, user_id: str, mfa_code: str) -> bool:
        """Validate MFA code"""
        # In production, this would validate against MFA provider
        return len(mfa_code) == 6 and mfa_code.isdigit()
        
    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get permissions for a user"""
        if user_id not in self.users:
            raise ValueError(f"User not found: {user_id}")
            
        user = self.users[user_id]
        if not user.active:
            return set()
            
        return self.roles[user.role].permissions
        
    def check_user_permission(
        self,
        user_id: str,
        permission: Permission
    ) -> bool:
        """Check if user has a specific permission"""
        try:
            user_permissions = self.get_user_permissions(user_id)
            return permission in user_permissions
        except ValueError:
            return False