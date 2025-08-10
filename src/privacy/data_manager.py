from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
import json
import logging
import hashlib
import re
from pathlib import Path

@dataclass
class PrivacyRule:
    name: str
    pattern: str  # Regex pattern
    replacement: str  # Replacement pattern or callback name
    description: str

@dataclass
class RetentionPolicy:
    data_type: str
    retention_days: int
    anonymize_after_days: Optional[int]  # Days after which to anonymize instead of delete
    description: str

@dataclass
class AuditEntry:
    timestamp: datetime
    operation: str  # "create", "read", "update", "delete", "anonymize"
    data_type: str
    identifier: str  # Data identifier (hashed)
    user_id: Optional[str]
    success: bool
    details: Dict[str, Any]

class DataPrivacyManager:
    def __init__(self):
        self.privacy_rules: Dict[str, PrivacyRule] = {}
        self.retention_policies: Dict[str, RetentionPolicy] = {}
        self.audit_log: List[AuditEntry] = []
        self.logger = logging.getLogger("data_privacy")
        
        # Initialize default privacy rules
        self._initialize_privacy_rules()
        
        # Initialize default retention policies
        self._initialize_retention_policies()
        
    def _initialize_privacy_rules(self) -> None:
        """Initialize default privacy rules"""
        self.privacy_rules = {
            "email": PrivacyRule(
                name="email",
                pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                replacement="[EMAIL]",
                description="Email address anonymization"
            ),
            "ip_address": PrivacyRule(
                name="ip_address",
                pattern=r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                replacement="[IP]",
                description="IP address anonymization"
            ),
            "credit_card": PrivacyRule(
                name="credit_card",
                pattern=r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
                replacement="[CREDIT_CARD]",
                description="Credit card number anonymization"
            ),
            "api_key": PrivacyRule(
                name="api_key",
                pattern=r'(?i)(api[_-]?key|token|secret)["\']?\s*[:=]\s*["\'][^"\']+["\']',
                replacement="[API_KEY]",
                description="API key/token anonymization"
            )
        }
        
    def _initialize_retention_policies(self) -> None:
        """Initialize default retention policies"""
        self.retention_policies = {
            "execution_logs": RetentionPolicy(
                data_type="execution_logs",
                retention_days=90,
                anonymize_after_days=30,
                description="Pattern execution logs retention"
            ),
            "metrics": RetentionPolicy(
                data_type="metrics",
                retention_days=365,
                anonymize_after_days=None,  # Never anonymize metrics
                description="Performance metrics retention"
            ),
            "audit_logs": RetentionPolicy(
                data_type="audit_logs",
                retention_days=730,  # 2 years
                anonymize_after_days=None,  # Never anonymize audit logs
                description="Privacy audit logs retention"
            )
        }
        
    def anonymize_data(self, data: Any, rules: Optional[List[str]] = None) -> Any:
        """Anonymize data according to privacy rules"""
        if isinstance(data, str):
            return self._anonymize_text(data, rules)
        elif isinstance(data, dict):
            return {
                k: self.anonymize_data(v, rules)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [
                self.anonymize_data(item, rules)
                for item in data
            ]
        return data
        
    def _anonymize_text(self, text: str, rules: Optional[List[str]] = None) -> str:
        """Anonymize text using specified rules or all rules"""
        if rules:
            active_rules = {
                name: rule
                for name, rule in self.privacy_rules.items()
                if name in rules
            }
        else:
            active_rules = self.privacy_rules
            
        result = text
        for rule in active_rules.values():
            result = re.sub(rule.pattern, rule.replacement, result)
            
        return result
        
    def check_retention(self, data_type: str, creation_date: datetime) -> str:
        """Check retention status for data"""
        if data_type not in self.retention_policies:
            raise ValueError(f"No retention policy for data type: {data_type}")
            
        policy = self.retention_policies[data_type]
        age_days = (datetime.now() - creation_date).days
        
        if age_days > policy.retention_days:
            return "delete"
        elif (
            policy.anonymize_after_days
            and age_days > policy.anonymize_after_days
        ):
            return "anonymize"
            
        return "retain"
        
    def add_audit_entry(
        self,
        operation: str,
        data_type: str,
        identifier: str,
        user_id: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an audit log entry"""
        # Hash identifier to avoid storing sensitive data
        hashed_id = hashlib.sha256(identifier.encode()).hexdigest()
        
        entry = AuditEntry(
            timestamp=datetime.now(),
            operation=operation,
            data_type=data_type,
            identifier=hashed_id,
            user_id=user_id,
            success=success,
            details=details or {}
        )
        
        self.audit_log.append(entry)
        
    def get_audit_log(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        operations: Optional[List[str]] = None,
        data_type: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[AuditEntry]:
        """Get filtered audit log entries"""
        filtered = self.audit_log
        
        if start_date:
            filtered = [
                entry for entry in filtered
                if entry.timestamp >= start_date
            ]
            
        if end_date:
            filtered = [
                entry for entry in filtered
                if entry.timestamp <= end_date
            ]
            
        if operations:
            filtered = [
                entry for entry in filtered
                if entry.operation in operations
            ]
            
        if data_type:
            filtered = [
                entry for entry in filtered
                if entry.data_type == data_type
            ]
            
        if user_id:
            filtered = [
                entry for entry in filtered
                if entry.user_id == user_id
            ]
            
        return filtered
        
    def generate_privacy_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate privacy compliance report"""
        # Get relevant audit entries
        entries = self.get_audit_log(start_date, end_date)
        
        # Count operations by type
        operation_counts = {}
        for entry in entries:
            if entry.operation not in operation_counts:
                operation_counts[entry.operation] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0
                }
            operation_counts[entry.operation]["total"] += 1
            if entry.success:
                operation_counts[entry.operation]["success"] += 1
            else:
                operation_counts[entry.operation]["failure"] += 1
                
        # Count operations by data type
        data_type_counts = {}
        for entry in entries:
            if entry.data_type not in data_type_counts:
                data_type_counts[entry.data_type] = 0
            data_type_counts[entry.data_type] += 1
            
        return {
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            },
            "summary": {
                "total_operations": len(entries),
                "success_rate": sum(
                    1 for e in entries if e.success
                ) / len(entries) if entries else 0
            },
            "operations": operation_counts,
            "data_types": data_type_counts,
            "retention_policies": {
                data_type: {
                    "retention_days": policy.retention_days,
                    "anonymize_after_days": policy.anonymize_after_days
                }
                for data_type, policy in self.retention_policies.items()
            }
        }
        
    def add_privacy_rule(
        self,
        name: str,
        pattern: str,
        replacement: str,
        description: str
    ) -> None:
        """Add a new privacy rule"""
        if name in self.privacy_rules:
            raise ValueError(f"Rule already exists: {name}")
            
        # Validate regex pattern
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {str(e)}")
            
        self.privacy_rules[name] = PrivacyRule(
            name=name,
            pattern=pattern,
            replacement=replacement,
            description=description
        )
        
    def add_retention_policy(
        self,
        data_type: str,
        retention_days: int,
        anonymize_after_days: Optional[int],
        description: str
    ) -> None:
        """Add a new retention policy"""
        if data_type in self.retention_policies:
            raise ValueError(f"Policy already exists: {data_type}")
            
        if retention_days < 1:
            raise ValueError("Retention days must be positive")
            
        if (
            anonymize_after_days is not None
            and anonymize_after_days >= retention_days
        ):
            raise ValueError(
                "Anonymization must occur before final retention period"
            )
            
        self.retention_policies[data_type] = RetentionPolicy(
            data_type=data_type,
            retention_days=retention_days,
            anonymize_after_days=anonymize_after_days,
            description=description
        )