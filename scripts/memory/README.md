# Memory Maintenance System

## Overview

The Memory Maintenance System provides automated workflows for maintaining the Claude Code Agent Framework's memory intelligence while ensuring optimal performance and preventing memory fragmentation.

## Quick Start

### Using Make Commands (Recommended)
```bash
# Check memory system status
make memory-status

# Validate and fix memory issues
make memory-validate

# Run full maintenance
make memory-maintenance

# Show memory dashboard
make memory-dashboard

# Enable periodic maintenance
make memory-setup

# Show help
make memory-help
```

### Using Memory Manager Directly
```bash
# Show quick status
./scripts/memory/memory_manager.sh status

# Validate with fixes and detailed report
./scripts/memory/memory_manager.sh validate --fix --report

# Run full maintenance
./scripts/memory/memory_manager.sh maintenance full

# Show interactive dashboard
./scripts/memory/memory_manager.sh dashboard

# Show help
./scripts/memory/memory_manager.sh --help
```

## Memory Maintenance Scripts

### 1. `memory_manager.sh` - Unified Interface
Single entry point for all memory maintenance operations.

**Commands:**
- `status` - Quick memory system status
- `validate [--fix] [--report]` - Comprehensive memory validation
- `maintenance [full|periodic|post-quality]` - Memory maintenance operations  
- `dashboard` - Interactive memory system dashboard
- `setup-periodic [--enable|--disable|--status]` - Periodic maintenance management

### 2. `auto_maintenance.sh` - Automated Maintenance
Core maintenance script for memory optimization and cleanup.

**Features:**
- Memory file consolidation (prevents fragmentation)
- Log rotation and cleanup
- Memory consistency validation
- Performance optimization and deduplication
- Memory health monitoring

**Modes:**
- `full` - Complete maintenance cycle
- `periodic` - Regular maintenance (hourly)
- `post-quality` - Light maintenance after quality enforcement

### 3. `validate_memory.sh` - Memory Validation
Comprehensive memory structure and content validation.

**Features:**
- Memory structure validation (required files/directories)
- Content validation (file sizes, format, structure)
- Performance validation (memory usage limits)
- Configuration validation (settings.json integration)
- Automatic issue fixing with `--fix` option

### 4. `setup_periodic_maintenance.sh` - Periodic Maintenance
Setup and manage automated periodic memory maintenance.

**Features:**
- macOS launchd integration (preferred)
- Linux cron integration (fallback)
- Automatic maintenance every hour
- Status monitoring and management
- Easy enable/disable operations

### 5. `memory_dashboard.sh` - Monitoring Dashboard
Real-time memory system monitoring and health dashboard.

**Features:**
- Live memory statistics and health metrics
- File breakdown and usage analysis
- Performance metrics and trends
- Alert checking and health scoring
- Report generation

**Modes:**
- Default: Show current dashboard
- `--live` - Live monitoring with auto-refresh
- `--report` - Generate detailed report
- `--alerts` - Check for system alerts

## Integration with Quality Enforcement

The memory maintenance system is integrated with the quality enforcement hook (`essential_quality.sh`) to automatically trigger light maintenance after code changes.

**Configuration:**
```bash
# Enable memory maintenance integration (default: enabled)
export CLAUDE_MEMORY_MAINTENANCE_ENABLED=true

# Disable memory maintenance integration
export CLAUDE_MEMORY_MAINTENANCE_ENABLED=false
```

## Periodic Maintenance

### Enable Automatic Maintenance
```bash
# Enable periodic maintenance (runs every hour)
make memory-setup

# Or directly:
./scripts/memory/setup_periodic_maintenance.sh --enable
```

### Check Status
```bash
./scripts/memory/setup_periodic_maintenance.sh --status
```

### Disable Automatic Maintenance
```bash
make memory-stop

# Or directly:
./scripts/memory/setup_periodic_maintenance.sh --disable
```

## Configuration

### Memory Maintenance Thresholds
```bash
# Maximum memory files before consolidation
MAX_MEMORY_FILES=15

# Maximum log size before rotation (lines)
MAX_LOG_SIZE_LINES=500

# File cleanup older than (days)
CLEANUP_OLDER_THAN_DAYS=7

# Performance log retention (days)
PERFORMANCE_LOG_RETENTION_DAYS=3
```

### Memory Validation Limits
```bash
# Maximum file size per memory file
MAX_FILE_SIZE_BYTES=102400  # 100KB

# Minimum file size to be valid
MIN_FILE_SIZE_BYTES=100     # 100 bytes

# Total memory limit across all files
MAX_TOTAL_MEMORY_MB=5       # 5MB
```

### Dashboard Configuration
```bash
# Live dashboard refresh interval
REFRESH_INTERVAL=5          # seconds

# Alert thresholds
ALERT_THRESHOLD_MB=3        # Memory usage alert
FILE_COUNT_THRESHOLD=12     # File count alert
```

## Log Files

All memory maintenance operations log to dedicated files:

- **Memory Manager**: `.claude/memory_manager.log`
- **Auto Maintenance**: `.claude/memory_maintenance.log`
- **Memory Validation**: `.claude/memory_validation.log`
- **Dashboard Operations**: `.claude/memory_dashboard.log`
- **Setup Operations**: `.claude/maintenance_setup.log`
- **Periodic Maintenance**: `.claude/periodic_maintenance.log`

## Health Monitoring

The system includes comprehensive health monitoring:

### Health Score Calculation
- **Memory Usage**: -30 points if exceeding 3MB
- **File Count**: -20 points if more than 12 files
- **Required Files**: -25 points if missing required files
- **Maintenance Frequency**: -15 points if no maintenance in 24 hours

### Health Status Levels
- **EXCELLENT**: 90-100 points
- **GOOD**: 75-89 points  
- **WARNING**: 60-74 points
- **CRITICAL**: <60 points

### Alerts
Automatic alerts trigger when:
- Memory usage exceeds 3MB
- File count exceeds 12 files
- Health score falls below 70
- No maintenance in 24+ hours

## Troubleshooting

### Common Issues

**Memory Manager Reports Missing Scripts**
```bash
# Make scripts executable
chmod +x scripts/memory/*.sh
```

**Periodic Maintenance Not Running**
```bash
# Check status
./scripts/memory/setup_periodic_maintenance.sh --status

# Re-enable if needed
./scripts/memory/setup_periodic_maintenance.sh --disable
./scripts/memory/setup_periodic_maintenance.sh --enable
```

**Memory Validation Failures**
```bash
# Run validation with automatic fixes
make memory-validate

# Or manually fix issues
./scripts/memory/validate_memory.sh --fix --report
```

**High Memory Usage Warnings**
```bash
# Run maintenance to clean up old files
make memory-maintenance

# Check dashboard for details
make memory-dashboard
```

### Debugging

Enable debug logging by setting:
```bash
export CLAUDE_MEMORY_DEBUG=true
```

Check specific log files for detailed information:
```bash
# View recent maintenance activity
tail -f .claude/memory_maintenance.log

# View validation results  
cat .claude/memory_validation_report.md

# View setup issues
tail -f .claude/maintenance_setup.log
```

## Performance

### Maintenance Performance
- **Light Maintenance**: <30s (post-quality)
- **Periodic Maintenance**: <60s (hourly)
- **Full Maintenance**: <120s (on-demand)

### Memory Usage
- **Target**: <1MB total memory files
- **Warning**: >3MB total memory files  
- **Critical**: >5MB total memory files

### File Limits
- **Target**: <10 memory files
- **Warning**: >12 memory files
- **Maximum**: 15 files (triggers consolidation)

## Best Practices

1. **Run periodic maintenance**: Enable automatic maintenance for optimal performance
2. **Monitor health regularly**: Use `make memory-status` to check system health
3. **Validate after changes**: Run validation after significant memory modifications
4. **Review logs periodically**: Check maintenance logs for issues or warnings
5. **Use the dashboard**: Monitor trends and performance metrics via dashboard
6. **Keep archives**: Old memory files are archived, not deleted, for recovery

## Architecture

The memory maintenance system follows a modular architecture:

```
memory_manager.sh (Unified Interface)
   auto_maintenance.sh (Core Maintenance)
   validate_memory.sh (Validation & Fixing)
   setup_periodic_maintenance.sh (Automation)
   memory_dashboard.sh (Monitoring)
```

Each script is independent but coordinates through the unified manager interface for consistent operation and logging.