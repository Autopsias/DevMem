import pytest
from pathlib import Path
import sys
from typing import Dict, List, Type, Optional
import asyncio

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.validation.validator import ValidationFramework
from src.compliance.automated_validator import ComplianceValidator
from src.patterns.base import PatternBase

class TestAnthropicCompliance:
    @pytest.fixture
    def validation_framework(self) -> ValidationFramework:
        return ValidationFramework()
    
    @pytest.fixture
    def compliance_validator(self) -> ComplianceValidator:
        return ComplianceValidator()

    async def test_basic_compliance_validation(self, compliance_validator: ComplianceValidator):
        pattern = {"type": "sequential", "input": "test"}
        validation = await compliance_validator.validate_pattern_compliance(pattern)
        assert validation.compliance_score >= 0.98, "Failed to meet minimum compliance score"
        assert not validation.violations, "Unexpected compliance violations"

    async def test_security_compliance_validation(self, compliance_validator: ComplianceValidator):
        pattern = {
            "type": "sequential",
            "input": "test",
            "security": {"access_level": "restricted"}
        }
        validation = await compliance_validator.validate_security_compliance(pattern)
        assert validation.security_score >= 0.98, "Failed to meet security compliance threshold"
        assert validation.data_handling_compliant, "Data handling non-compliant"

    async def test_audit_trail_validation(self, compliance_validator: ComplianceValidator):
        pattern = {"type": "sequential", "input": "test"}
        await compliance_validator.validate_pattern_compliance(pattern)
        audit_entries = compliance_validator.get_audit_entries()
        
        assert len(audit_entries) > 0, "No audit trail entries generated"
        assert "pattern_validation" in audit_entries[0].event_type
        assert audit_entries[0].timestamp is not None

    async def test_compliance_regression_detection(self, compliance_validator: ComplianceValidator):
        # Generate baseline compliance data
        baseline_patterns = [
            {"type": "sequential", "input": f"test_{i}"} 
            for i in range(10)
        ]
        baseline_scores = []
        for pattern in baseline_patterns:
            validation = await compliance_validator.validate_pattern_compliance(pattern)
            baseline_scores.append(validation.compliance_score)
        
        # Validate no regression from baseline
        test_pattern = {"type": "sequential", "input": "test_new"}
        validation = await compliance_validator.validate_pattern_compliance(test_pattern)
        
        regression = compliance_validator.detect_compliance_regression(
            [validation.compliance_score],
            baseline_scores
        )
        assert not regression, "Compliance regression detected"

    def test_compliance_reporting(self, compliance_validator: ComplianceValidator):
        report = compliance_validator.generate_compliance_report()
        assert "compliance_summary" in report
        assert "security_assessment" in report
        assert "recommendations" in report
        assert report["compliance_summary"]["score"] >= 0.98