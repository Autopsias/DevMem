import pytest
from datetime import datetime, timedelta
import re
from typing import Dict, Any

from src.privacy.data_manager import (
    DataPrivacyManager,
    PrivacyRule,
    RetentionPolicy,
    AuditEntry
)

@pytest.fixture
def data_manager() -> DataPrivacyManager:
    return DataPrivacyManager()

@pytest.fixture
def test_data() -> Dict[str, Any]:
    return {
        "user": {
            "email": "test@example.com",
            "ip_address": "192.168.1.1",
            "card": "4111-1111-1111-1111",
            "api_key": "api_key = 'secret123'"
        },
        "log": "User login from 192.168.1.1 with test@example.com"
    }

def test_default_privacy_rules(data_manager: DataPrivacyManager):
    """Test default privacy rules configuration"""
    rules = data_manager.privacy_rules
    
    # Check default rules exist
    assert "email" in rules
    assert "ip_address" in rules
    assert "credit_card" in rules
    assert "api_key" in rules
    
    # Verify rule properties
    email_rule = rules["email"]
    assert email_rule.name == "email"
    assert "EMAIL" in email_rule.replacement
    
    # Test pattern compilation
    for rule in rules.values():
        assert re.compile(rule.pattern)  # Should not raise error

def test_default_retention_policies(data_manager: DataPrivacyManager):
    """Test default retention policies configuration"""
    policies = data_manager.retention_policies
    
    # Check default policies exist
    assert "execution_logs" in policies
    assert "metrics" in policies
    assert "audit_logs" in policies
    
    # Verify policy properties
    log_policy = policies["execution_logs"]
    assert log_policy.retention_days == 90
    assert log_policy.anonymize_after_days == 30
    
    metrics_policy = policies["metrics"]
    assert metrics_policy.retention_days == 365
    assert metrics_policy.anonymize_after_days is None

def test_data_anonymization(data_manager: DataPrivacyManager, test_data: Dict[str, Any]):
    """Test data anonymization"""
    # Anonymize nested dictionary
    anon_data = data_manager.anonymize_data(test_data)
    
    # Check user data anonymization
    user = anon_data["user"]
    assert user["email"] == "[EMAIL]"
    assert user["ip_address"] == "[IP]"
    assert user["card"] == "[CREDIT_CARD]"
    assert "[API_KEY]" in user["api_key"]
    
    # Check log anonymization
    assert "[IP]" in anon_data["log"]
    assert "[EMAIL]" in anon_data["log"]
    
    # Test selective rule application
    partial_anon = data_manager.anonymize_data(
        test_data,
        rules=["email", "ip_address"]
    )
    assert partial_anon["user"]["email"] == "[EMAIL]"
    assert partial_anon["user"]["ip_address"] == "[IP]"
    assert partial_anon["user"]["card"] == test_data["user"]["card"]

def test_retention_checking(data_manager: DataPrivacyManager):
    """Test data retention status checking"""
    now = datetime.now()
    
    # Test retention for execution logs
    assert data_manager.check_retention(
        "execution_logs",
        now - timedelta(days=10)
    ) == "retain"
    
    assert data_manager.check_retention(
        "execution_logs",
        now - timedelta(days=40)
    ) == "anonymize"
    
    assert data_manager.check_retention(
        "execution_logs",
        now - timedelta(days=100)
    ) == "delete"
    
    # Test retention for metrics (no anonymization)
    assert data_manager.check_retention(
        "metrics",
        now - timedelta(days=300)
    ) == "retain"
    
    assert data_manager.check_retention(
        "metrics",
        now - timedelta(days=400)
    ) == "delete"
    
    # Test invalid data type
    with pytest.raises(ValueError):
        data_manager.check_retention("invalid", now)

def test_audit_logging(data_manager: DataPrivacyManager):
    """Test audit logging functionality"""
    # Add various audit entries
    data_manager.add_audit_entry(
        "create",
        "execution_logs",
        "log123",
        user_id="user1",
        details={"source": "test"}
    )
    
    data_manager.add_audit_entry(
        "anonymize",
        "execution_logs",
        "log123",
        user_id="user1"
    )
    
    data_manager.add_audit_entry(
        "read",
        "metrics",
        "metric456",
        user_id="user2"
    )
    
    # Test unfiltered retrieval
    all_entries = data_manager.get_audit_log()
    assert len(all_entries) == 3
    
    # Test filtering by operation
    create_entries = data_manager.get_audit_log(operations=["create"])
    assert len(create_entries) == 1
    assert create_entries[0].operation == "create"
    
    # Test filtering by user
    user1_entries = data_manager.get_audit_log(user_id="user1")
    assert len(user1_entries) == 2
    assert all(e.user_id == "user1" for e in user1_entries)
    
    # Test filtering by date range
    recent_entries = data_manager.get_audit_log(
        start_date=datetime.now() - timedelta(minutes=1)
    )
    assert len(recent_entries) == 3

def test_privacy_report(data_manager: DataPrivacyManager):
    """Test privacy report generation"""
    # Add test audit entries
    data_manager.add_audit_entry(
        "create",
        "execution_logs",
        "log1",
        success=True
    )
    data_manager.add_audit_entry(
        "read",
        "execution_logs",
        "log1",
        success=True
    )
    data_manager.add_audit_entry(
        "anonymize",
        "execution_logs",
        "log1",
        success=False
    )
    
    # Generate report
    report = data_manager.generate_privacy_report()
    
    # Check report structure
    assert "summary" in report
    assert "operations" in report
    assert "data_types" in report
    assert "retention_policies" in report
    
    # Check operation counts
    ops = report["operations"]
    assert ops["create"]["total"] == 1
    assert ops["create"]["success"] == 1
    assert ops["anonymize"]["failure"] == 1
    
    # Check data type counts
    assert report["data_types"]["execution_logs"] == 3
    
    # Check retention policies
    policies = report["retention_policies"]
    assert "execution_logs" in policies
    assert policies["execution_logs"]["retention_days"] == 90

def test_custom_privacy_rules(data_manager: DataPrivacyManager):
    """Test adding custom privacy rules"""
    # Add custom rule
    data_manager.add_privacy_rule(
        "phone",
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "[PHONE]",
        "Phone number anonymization"
    )
    
    # Test new rule
    test_data = "Call me at 123-456-7890"
    anon_data = data_manager.anonymize_data(test_data, rules=["phone"])
    assert anon_data == "Call me at [PHONE]"
    
    # Test invalid pattern
    with pytest.raises(ValueError):
        data_manager.add_privacy_rule(
            "invalid",
            "[",  # Invalid regex
            "replacement",
            "description"
        )
        
    # Test duplicate name
    with pytest.raises(ValueError):
        data_manager.add_privacy_rule(
            "phone",
            r'\d+',
            "replacement",
            "description"
        )

def test_custom_retention_policies(data_manager: DataPrivacyManager):
    """Test adding custom retention policies"""
    # Add custom policy
    data_manager.add_retention_policy(
        "user_data",
        retention_days=180,
        anonymize_after_days=90,
        description="User data retention"
    )
    
    # Test new policy
    now = datetime.now()
    assert data_manager.check_retention(
        "user_data",
        now - timedelta(days=60)
    ) == "retain"
    
    assert data_manager.check_retention(
        "user_data",
        now - timedelta(days=120)
    ) == "anonymize"
    
    assert data_manager.check_retention(
        "user_data",
        now - timedelta(days=200)
    ) == "delete"
    
    # Test invalid retention days
    with pytest.raises(ValueError):
        data_manager.add_retention_policy(
            "invalid",
            retention_days=0,
            anonymize_after_days=None,
            description="Invalid"
        )
        
    # Test invalid anonymization days
    with pytest.raises(ValueError):
        data_manager.add_retention_policy(
            "invalid",
            retention_days=30,
            anonymize_after_days=40,  # Greater than retention days
            description="Invalid"
        )