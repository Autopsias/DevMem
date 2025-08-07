# System Maintenance Guide for Simplified Claude Code Framework

## Overview

This guide provides comprehensive maintenance procedures for the simplified Claude Code Framework, focusing on essential system health, monitoring, and emergency response procedures.

## Quick Reference

### Daily Operations
```bash
# Quick health check
make memory-status && make system-health

# Validate system integrity  
make validate-system

# Check recent logs
make log-summary
```

### Weekly Maintenance
```bash
# Full system maintenance
make system-maintenance

# Memory optimization
make memory-maintenance

# Security audit
make security-check
```

## 1. Regular Maintenance Procedures

### 1.1 Daily Health Checks

#### Memory System Health
```bash
# Quick memory status
make memory-status

# Expected output:
#  Memory Health: GOOD (85/100)
# =Á Memory Files: 8/15 
# =¾ Memory Usage: 1.2MB/3MB
# ñ Last Maintenance: 2h ago
```

#### Essential Services Status
```bash
# Check essential hooks
./scripts/system/check_essential_hooks.sh

# Validate configurations
python scripts/validate_native_config.py
```

#### Log Health Check
```bash
# Check log sizes and rotation
./scripts/system/log_health_check.sh

# Expected behavior:
# - Security logs < 100 lines
# - Quality logs < 200 lines  
# - Memory logs < 500 lines
# - Automatic rotation working
```

### 1.2 Weekly Deep Maintenance

#### Complete System Maintenance
```bash
# Run comprehensive maintenance
make system-maintenance

# This includes:
# - Memory cleanup and optimization
# - Log rotation and archival
# - Configuration validation
# - Performance optimization
# - Security audit
```

#### Memory Optimization
```bash
# Full memory maintenance with report
make memory-maintenance
make memory-dashboard

# Review memory trends and optimization opportunities
```

#### Configuration Audit
```bash
# Validate all configurations
./scripts/system/config_audit.sh

# Check for:
# - Settings.json consistency
# - Hook configuration validity
# - Environment variable alignment
# - Permission compliance
```

### 1.3 Monthly System Review

#### Performance Analysis
```bash
# Generate performance report
./scripts/system/performance_analysis.sh

# Review:
# - Agent response times
# - Memory usage trends
# - Hook execution performance
# - System resource utilization
```

#### Security Assessment
```bash
# Run security audit
./scripts/system/security_assessment.sh

# Check:
# - Permission configurations
# - Hook security compliance
# - Log file access controls
# - Sensitive data exposure
```

## 2. Health Check Procedures

### 2.1 System Health Monitoring

#### Automated Health Checks
The system includes automated health monitoring through several components:

```bash
# Primary health check script
./scripts/system/system_health.sh

# Health check components:
# 1. Essential hooks functionality
# 2. Memory system health
# 3. Configuration integrity
# 4. Log system health
# 5. Permission compliance
```

#### Health Score Calculation
```
Total Health Score = Memory Health (40%) + Config Health (25%) + 
                    Log Health (20%) + Security Health (15%)

Health Levels:
- EXCELLENT: 90-100 points (=â)
- GOOD: 75-89 points (=á)  
- WARNING: 60-74 points (=à)
- CRITICAL: <60 points (=4)
```

#### Key Health Metrics

**Memory Health Indicators:**
- Memory usage < 3MB (Target: <1MB)
- File count < 12 (Target: <10)
- No missing required memory files
- Recent maintenance activity (<24h)

**Configuration Health Indicators:**
- Valid settings.json structure
- Essential hooks properly configured
- Environment variables set correctly
- No permission conflicts

**Log Health Indicators:**
- Log files within size limits
- Automatic rotation functioning
- No error patterns in recent logs
- Proper log file permissions

**Security Health Indicators:**
- Essential security hook active
- No dangerous commands in recent logs
- Proper file permissions
- No security violations detected

### 2.2 Proactive Monitoring

#### Threshold Monitoring
```bash
# Set up monitoring thresholds
export MEMORY_WARNING_THRESHOLD_MB=3
export LOG_WARNING_THRESHOLD_LINES=200  
export HEALTH_SCORE_WARNING_THRESHOLD=70

# Monitor via cron (optional)
# Add to crontab for automated monitoring:
# 0 */6 * * * /path/to/scripts/system/health_monitor.sh
```

#### Alert Configuration
```bash
# Enable health alerts (logs to .claude/health_alerts.log)
export HEALTH_ALERTS_ENABLED=true
export HEALTH_ALERT_EMAIL_ENABLED=false  # Email alerts disabled by default
```

## 3. Monitoring Procedures

### 3.1 Log Monitoring

#### Essential Log Files
```
.claude/security.log          - Security hook events
.claude/quality.log           - Code quality enforcement
.claude/memory_maintenance.log - Memory maintenance operations  
.claude/system_health.log     - System health monitoring
```

#### Log Monitoring Commands
```bash
# Monitor security events
tail -f .claude/security.log

# Check quality enforcement
tail -n 20 .claude/quality.log

# Review memory maintenance
less .claude/memory_maintenance.log

# View system health history
./scripts/system/health_history.sh
```

#### Log Analysis
```bash
# Analyze log patterns
./scripts/system/log_analyzer.sh

# Generate log summary
./scripts/system/log_summary.sh --period=7days

# Check for anomalies
./scripts/system/anomaly_detector.sh
```

### 3.2 Performance Monitoring

#### System Performance Metrics
```bash
# Monitor system performance
./scripts/system/performance_monitor.sh

# Track metrics:
# - Hook execution time
# - Memory maintenance duration
# - Agent response latency
# - System resource usage
```

#### Performance Baselines
```
Baseline Performance Targets:
- Security hook: <5s execution time
- Quality hook: <10s execution time
- Memory maintenance: <30s (light), <120s (full)
- System health check: <15s
- Agent selection: <1s
```

### 3.3 Resource Monitoring

#### Disk Space Monitoring
```bash
# Check disk space usage
./scripts/system/disk_usage_monitor.sh

# Monitor specific directories:
# .claude/ directory size
# Log file growth rates
# Memory file accumulation
```

#### Memory Usage Monitoring
```bash
# System memory usage
./scripts/system/memory_usage_monitor.sh

# Process memory usage
./scripts/system/process_monitor.sh
```

## 4. Emergency Response Procedures

### 4.1 System Recovery Procedures

#### Emergency System Reset
```bash
# Emergency system reset (CAUTION: Resets all configurations)
./scripts/emergency/system_reset.sh --confirm

# This will:
# 1. Backup current configurations
# 2. Reset to default settings
# 3. Reinitialize memory system
# 4. Restart essential services
```

#### Memory System Recovery
```bash
# Memory corruption recovery
./scripts/emergency/memory_recovery.sh

# Steps:
# 1. Backup corrupted memory files
# 2. Restore from known good state
# 3. Validate memory consistency
# 4. Restart memory maintenance
```

#### Configuration Recovery
```bash
# Restore configuration from backup
./scripts/emergency/config_recovery.sh

# Hook system recovery
./scripts/emergency/hook_recovery.sh
```

### 4.2 Emergency Diagnostics

#### Rapid Diagnostics
```bash
# Emergency diagnostic collection
./scripts/emergency/collect_diagnostics.sh

# Generates:
# - System state snapshot
# - Recent log excerpts
# - Configuration dump
# - Memory system status
# - Performance metrics
```

#### Critical Issue Detection
```bash
# Detect critical system issues
./scripts/emergency/critical_issue_detector.sh

# Checks for:
# - Corrupted configuration files
# - Failed essential hooks
# - Memory system failures
# - Security violations
# - Resource exhaustion
```

### 4.3 Emergency Contacts and Escalation

#### Issue Severity Levels

**Level 1 - Information**
- Health score 75-89
- Warning thresholds exceeded
- Non-critical performance degradation
- Action: Monitor, schedule maintenance

**Level 2 - Warning**  
- Health score 60-74
- Multiple warning conditions
- System performance impact
- Action: Investigate, implement fixes

**Level 3 - Critical**
- Health score <60
- Essential system failures
- Security violations
- Action: Immediate emergency response

**Level 4 - Emergency**
- System completely non-functional
- Data integrity threats
- Security breaches
- Action: Emergency recovery procedures

#### Emergency Response Workflow
```
1. Detect Issue ’ Run diagnostics ’ Collect logs
2. Assess Severity ’ Determine response level
3. Execute Response ’ Document actions
4. Validate Recovery ’ Monitor stability
5. Post-Incident Review ’ Update procedures
```

## 5. Maintenance Scripts Reference

### 5.1 Core Maintenance Scripts

#### System Health Scripts
```bash
# Main system health check
./scripts/system/system_health.sh [--detailed] [--json]

# Component health checks
./scripts/system/check_essential_hooks.sh
./scripts/system/check_memory_health.sh  
./scripts/system/check_config_health.sh
./scripts/system/check_log_health.sh
```

#### Maintenance Operations
```bash
# Full system maintenance
./scripts/system/full_maintenance.sh

# Component maintenance
./scripts/system/log_maintenance.sh
./scripts/system/config_maintenance.sh
./scripts/system/security_maintenance.sh
```

#### Emergency Scripts
```bash
# Emergency diagnostics
./scripts/emergency/collect_diagnostics.sh
./scripts/emergency/system_reset.sh
./scripts/emergency/memory_recovery.sh
./scripts/emergency/config_recovery.sh
```

### 5.2 Monitoring Scripts

#### Automated Monitoring
```bash
# Health monitoring daemon
./scripts/monitoring/health_monitor.sh [--daemon]

# Performance monitoring
./scripts/monitoring/performance_monitor.sh

# Log monitoring
./scripts/monitoring/log_monitor.sh [--follow]
```

#### Report Generation
```bash
# System status report
./scripts/reporting/system_status_report.sh

# Performance analysis report
./scripts/reporting/performance_report.sh [--period=7d]

# Maintenance summary report
./scripts/reporting/maintenance_report.sh
```

## 6. Best Practices

### 6.1 Preventive Maintenance

1. **Regular Health Checks**: Run daily health checks to catch issues early
2. **Proactive Monitoring**: Set up monitoring for key metrics and thresholds
3. **Timely Updates**: Keep configurations and scripts updated
4. **Documentation**: Document all maintenance activities and changes
5. **Testing**: Test emergency procedures in non-production environment

### 6.2 Performance Optimization

1. **Memory Management**: Regular memory maintenance prevents fragmentation
2. **Log Rotation**: Automatic log rotation prevents disk space issues
3. **Configuration Review**: Regular configuration audits ensure optimal settings
4. **Resource Monitoring**: Monitor system resources to prevent bottlenecks
5. **Performance Baselines**: Establish and monitor performance baselines

### 6.3 Security Maintenance

1. **Security Audits**: Regular security assessments and compliance checks
2. **Permission Reviews**: Periodic review of file and directory permissions
3. **Access Monitoring**: Monitor access patterns and unusual activities
4. **Security Updates**: Keep security configurations current and tested
5. **Incident Response**: Maintain updated incident response procedures

## 7. Troubleshooting Guide

### 7.1 Common Issues

#### Memory System Issues
```bash
# Issue: High memory usage
# Solution: Run memory cleanup
make memory-maintenance

# Issue: Memory corruption
# Solution: Restore from backup
./scripts/emergency/memory_recovery.sh

# Issue: Missing memory files
# Solution: Validate and repair
make memory-validate
```

#### Hook System Issues
```bash
# Issue: Hooks not executing
# Solution: Check permissions and validate
./scripts/system/check_essential_hooks.sh
chmod +x scripts/hooks/*.sh

# Issue: Hook timeouts
# Solution: Review hook performance
./scripts/system/hook_performance_analysis.sh

# Issue: Hook failures
# Solution: Check logs and configuration
tail -f .claude/security.log
tail -f .claude/quality.log
```

#### Configuration Issues
```bash
# Issue: Invalid settings.json
# Solution: Validate and repair
python scripts/validate_native_config.py

# Issue: Environment variables not set
# Solution: Check and restore environment
./scripts/system/check_environment.sh

# Issue: Permission errors
# Solution: Fix permissions
./scripts/system/fix_permissions.sh
```

### 7.2 Emergency Procedures

#### System Unresponsive
1. Collect diagnostic information
2. Check system resources
3. Review recent logs
4. Attempt graceful recovery
5. If necessary, emergency reset

#### Data Corruption
1. Stop all operations immediately
2. Backup current state
3. Assess corruption extent
4. Restore from known good backup
5. Validate system integrity

#### Security Breach
1. Isolate affected systems
2. Assess breach scope
3. Implement containment measures
4. Document incident details
5. Execute recovery procedures

## 8. Appendices

### 8.1 Configuration Templates

#### Essential Hook Configuration
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/scripts/hooks/essential_security.sh",
            "timeout": 5,
            "description": "Essential bash security validation"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/scripts/hooks/essential_quality.sh", 
            "timeout": 10,
            "description": "Essential code quality enforcement"
          }
        ]
      }
    ]
  }
}
```

### 8.2 Environment Variables Reference

```bash
# Core system configuration
export CLAUDE_AGENT_FRAMEWORK_ENABLED=true
export CLAUDE_AGENT_NATURAL_DELEGATION=true
export QUALITY_GATES_ENABLED=true
export SECURITY_SCANNING_ENABLED=true

# Memory maintenance configuration
export CLAUDE_MEMORY_MAINTENANCE_ENABLED=true
export MEMORY_WARNING_THRESHOLD_MB=3
export LOG_WARNING_THRESHOLD_LINES=200

# Performance configuration  
export CLAUDE_AGENT_PERFORMANCE_TARGET_MS=1000
export CLAUDE_AGENT_MAX_CONTEXT_TOKENS=32000

# Health monitoring configuration
export HEALTH_ALERTS_ENABLED=true
export HEALTH_SCORE_WARNING_THRESHOLD=70
```

### 8.3 Log File Locations

```
System Logs:
- .claude/security.log              - Security hook events
- .claude/quality.log               - Quality enforcement
- .claude/system_health.log         - System health monitoring

Memory Management Logs:
- .claude/memory_maintenance.log    - Memory maintenance operations
- .claude/memory_validation.log     - Memory validation results
- .claude/memory_dashboard.log      - Dashboard operations

Emergency Logs:
- .claude/emergency_diagnostics.log - Emergency diagnostic collection
- .claude/system_recovery.log       - Recovery operations
- .claude/health_alerts.log         - System health alerts
```

This maintenance guide provides comprehensive procedures for maintaining the simplified Claude Code Framework while ensuring optimal performance, security, and reliability.