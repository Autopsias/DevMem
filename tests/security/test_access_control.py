import pytest
from datetime import datetime, timedelta
import jwt
from typing import Set

from src.security.access_control import (
    AccessControl,
    User,
    Role,
    Permission,
    AccessToken
)

@pytest.fixture
def access_control() -> AccessControl:
    return AccessControl()

@pytest.fixture
def test_user(access_control: AccessControl) -> User:
    return access_control.create_user("testuser", "developer")

def test_default_roles(access_control: AccessControl):
    """Test default role configuration"""
    # Check default roles exist
    assert "admin" in access_control.roles
    assert "developer" in access_control.roles
    assert "operator" in access_control.roles
    assert "reader" in access_control.roles
    
    # Check admin permissions
    admin_role = access_control.roles["admin"]
    assert Permission.ADMIN in admin_role.permissions
    assert Permission.READ in admin_role.permissions
    assert Permission.WRITE in admin_role.permissions
    assert Permission.EXECUTE in admin_role.permissions
    
    # Check developer permissions
    dev_role = access_control.roles["developer"]
    assert Permission.READ in dev_role.permissions
    assert Permission.WRITE in dev_role.permissions
    assert Permission.EXECUTE in dev_role.permissions
    assert Permission.ADMIN not in dev_role.permissions
    
    # Check operator permissions
    op_role = access_control.roles["operator"]
    assert Permission.READ in op_role.permissions
    assert Permission.EXECUTE in op_role.permissions
    assert Permission.WRITE not in op_role.permissions
    assert Permission.ADMIN not in op_role.permissions
    
    # Check reader permissions
    reader_role = access_control.roles["reader"]
    assert Permission.READ in reader_role.permissions
    assert len(reader_role.permissions) == 1

def test_user_creation(access_control: AccessControl):
    """Test user creation and properties"""
    user = access_control.create_user("testuser", "developer", mfa_enabled=True)
    
    assert user.username == "testuser"
    assert user.role == "developer"
    assert user.mfa_enabled
    assert user.active
    assert user.last_login is None
    assert len(user.id) == 16  # Check ID generation
    
    # Verify user is stored
    assert user.id in access_control.users
    stored_user = access_control.users[user.id]
    assert stored_user.username == user.username
    
    # Test invalid role
    with pytest.raises(ValueError):
        access_control.create_user("invalid", "nonexistent_role")

def test_role_creation(access_control: AccessControl):
    """Test role creation and modification"""
    # Create new role
    permissions = {Permission.READ, Permission.WRITE}
    role = access_control.create_role(
        "test_role",
        permissions,
        "Test role description"
    )
    
    assert role.name == "test_role"
    assert role.permissions == permissions
    assert role.description == "Test role description"
    
    # Update role permissions
    new_permissions = {Permission.READ, Permission.EXECUTE}
    access_control.update_role_permissions("test_role", new_permissions)
    
    updated_role = access_control.roles["test_role"]
    assert updated_role.permissions == new_permissions
    
    # Test duplicate role
    with pytest.raises(ValueError):
        access_control.create_role("test_role", permissions, "Duplicate")
        
    # Test updating nonexistent role
    with pytest.raises(ValueError):
        access_control.update_role_permissions(
            "nonexistent",
            {Permission.READ}
        )

def test_token_generation(access_control: AccessControl, test_user: User):
    """Test access token generation and validation"""
    # Generate token
    token = access_control.generate_access_token(test_user.id)
    
    assert token.user_id == test_user.id
    assert token.scope == access_control.roles["developer"].permissions
    assert token.expires_at > datetime.now()
    
    # Verify token is stored
    assert token.token in access_control.active_tokens
    
    # Verify last login updated
    assert test_user.last_login is not None
    
    # Test MFA requirement
    mfa_user = access_control.create_user(
        "mfa_user",
        "developer",
        mfa_enabled=True
    )
    
    with pytest.raises(ValueError):
        access_control.generate_access_token(mfa_user.id)
        
    # Test with invalid MFA code
    with pytest.raises(ValueError):
        access_control.generate_access_token(mfa_user.id, "123")
        
    # Test with valid MFA code
    token = access_control.generate_access_token(mfa_user.id, "123456")
    assert token is not None

def test_token_validation(access_control: AccessControl, test_user: User):
    """Test access token validation"""
    token = access_control.generate_access_token(test_user.id)
    
    # Validate token
    validated = access_control.validate_token(token.token)
    assert validated is not None
    assert validated.user_id == test_user.id
    assert validated.scope == token.scope
    
    # Test invalid token
    assert access_control.validate_token("invalid") is None
    
    # Test expired token
    token.expires_at = datetime.now() - timedelta(hours=1)
    assert access_control.validate_token(token.token) is None
    assert token.token not in access_control.active_tokens

def test_permission_checking(access_control: AccessControl, test_user: User):
    """Test permission checking functionality"""
    token = access_control.generate_access_token(test_user.id)
    
    # Check developer permissions
    assert access_control.check_permission(token.token, Permission.READ)
    assert access_control.check_permission(token.token, Permission.WRITE)
    assert access_control.check_permission(token.token, Permission.EXECUTE)
    assert not access_control.check_permission(token.token, Permission.ADMIN)
    
    # Check user permissions directly
    assert access_control.check_user_permission(test_user.id, Permission.READ)
    assert not access_control.check_user_permission(test_user.id, Permission.ADMIN)
    
    # Test invalid token
    assert not access_control.check_permission("invalid", Permission.READ)
    
    # Test nonexistent user
    assert not access_control.check_user_permission("nonexistent", Permission.READ)

def test_token_revocation(access_control: AccessControl, test_user: User):
    """Test token revocation"""
    token = access_control.generate_access_token(test_user.id)
    
    # Revoke token
    access_control.revoke_token(token.token)
    
    # Verify token is revoked
    assert token.token not in access_control.active_tokens
    assert access_control.validate_token(token.token) is None
    
    # Test revoking nonexistent token
    access_control.revoke_token("nonexistent")  # Should not raise error

def test_user_deactivation(access_control: AccessControl, test_user: User):
    """Test user deactivation"""
    token = access_control.generate_access_token(test_user.id)
    
    # Deactivate user
    access_control.deactivate_user(test_user.id)
    
    # Verify user is deactivated
    assert not test_user.active
    assert token.token not in access_control.active_tokens
    
    # Verify token generation fails
    with pytest.raises(ValueError):
        access_control.generate_access_token(test_user.id)
        
    # Verify permissions are revoked
    assert not access_control.get_user_permissions(test_user.id)
    
    # Test deactivating nonexistent user
    with pytest.raises(ValueError):
        access_control.deactivate_user("nonexistent")