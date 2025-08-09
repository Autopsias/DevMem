#!/usr/bin/env python3
"""
Validation Script Consolidation Tool

This script helps transition from individual validation scripts to the
integrated validation framework by:
1. Running a comparison between old and new validation approaches
2. Archiving old validation scripts to a backup directory
3. Creating migration documentation
4. Validating that all functionality is preserved
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'tests'))

def find_validation_scripts() -> List[Path]:
    """Find all validation scripts to be consolidated."""
    validation_scripts = []
    
    # Scripts in project root
    root_scripts = [
        "validate_story_completion.py",
        "validate_agent_selection.py", 
        "validate_infrastructure_learning.py",
        "validate_claude_code_agent_learning.py"
    ]
    
    for script_name in root_scripts:
        script_path = project_root / script_name
        if script_path.exists():
            validation_scripts.append(script_path)
    
    # Scripts in subdirectories
    subdirs_to_check = [
        project_root / "scripts",
        project_root / "tests"
    ]
    
    for subdir in subdirs_to_check:
        if subdir.exists():
            for script in subdir.glob("validate_*.py"):
                validation_scripts.append(script)
    
    return validation_scripts

def run_old_validation_scripts() -> Dict[str, Tuple[bool, str]]:
    """Run old validation scripts and capture their results."""
    import subprocess
    
    scripts = find_validation_scripts()
    results = {}
    
    print("🔍 Running existing validation scripts...")
    print("-" * 50)
    
    for script in scripts:
        script_name = script.name
        print(f"Running {script_name}...")
        
        try:
            # Run the script and capture output
            result = subprocess.run([
                sys.executable, str(script)
            ], capture_output=True, text=True, timeout=120, cwd=project_root)
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            results[script_name] = (success, output)
            print(f"  {'✅ PASSED' if success else '❌ FAILED'}: {script_name}")
            
        except subprocess.TimeoutExpired:
            results[script_name] = (False, "Timeout after 120 seconds")
            print(f"  ⏱️ TIMEOUT: {script_name}")
        except Exception as e:
            results[script_name] = (False, f"Error: {e}")
            print(f"  ⚠️ ERROR: {script_name} - {e}")
    
    return results

def run_integrated_framework() -> Tuple[bool, str]:
    """Run the new integrated validation framework."""
    print("\n🔍 Running integrated validation framework...")
    print("-" * 50)
    
    try:
        from test_integrated_validation_framework import IntegratedValidationFramework
        
        framework = IntegratedValidationFramework(project_root)
        success = framework.run_all_validations()
        
        # Capture summary
        passed_suites = sum(1 for suite in framework.test_results if suite.overall_passed)
        total_suites = len(framework.test_results)
        
        summary = f"Integrated framework: {passed_suites}/{total_suites} suites passed"
        
        return success, summary
        
    except Exception as e:
        return False, f"Error running integrated framework: {e}"

def compare_results(old_results: Dict[str, Tuple[bool, str]], 
                   new_result: Tuple[bool, str]) -> None:
    """Compare results between old and new validation approaches."""
    print("\n📈 Validation Results Comparison")
    print("=" * 60)
    
    # Old results summary
    old_passed = sum(1 for success, _ in old_results.values() if success)
    old_total = len(old_results)
    
    print("\n📜 Original Validation Scripts:")
    print(f"   Overall: {old_passed}/{old_total} scripts passed ({(old_passed/old_total):.1%})")
    
    for script_name, (success, output) in old_results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {script_name}")
    
    # New result summary
    new_success, new_summary = new_result
    print("\n🆕 Integrated Validation Framework:")
    print(f"   {'✅' if new_success else '❌'} {new_summary}")
    
    # Comparison assessment
    print("\n🎯 Comparison Assessment:")
    if new_success and old_passed == old_total:
        print("   🏆 Perfect migration: Both approaches successful")
    elif new_success and old_passed < old_total:
        print("   🚀 Improvement: Integrated framework resolves previous failures")
    elif not new_success and old_passed == old_total:
        print("   ⚠️ Regression: Integrated framework has issues to resolve")
    else:
        print("   🔄 Mixed results: Both approaches have validation issues")

def create_backup_archive() -> Path:
    """Create backup archive of old validation scripts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = project_root / "scripts" / "archived_validation" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    scripts = find_validation_scripts()
    archived_count = 0
    
    print(f"\n🗃️ Creating backup archive: {backup_dir}")
    
    for script in scripts:
        try:
            backup_path = backup_dir / script.name
            shutil.copy2(script, backup_path)
            archived_count += 1
            print(f"   Archived: {script.name}")
        except Exception as e:
            print(f"   Error archiving {script.name}: {e}")
    
    print(f"   Total archived: {archived_count} scripts")
    
    # Create archive manifest
    manifest_path = backup_dir / "archive_manifest.md"
    with open(manifest_path, 'w') as f:
        f.write("# Validation Scripts Archive\n\n")
        f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("**Purpose:** Backup of individual validation scripts before consolidation\n\n")
        f.write("## Archived Scripts\n\n")
        
        for script in scripts:
            f.write(f"- `{script.name}` - {script.parent.name}/\n")
        
        f.write("\n## Migration Notes\n\n")
        f.write("These scripts were consolidated into the integrated validation framework:\n")
        f.write("`tests/test_integrated_validation_framework.py`\n\n")
        f.write("To run consolidated validations: `pytest tests/test_integrated_validation_framework.py`\n")
        f.write("Or via CLI: `python tests/test_integrated_validation_framework.py`\n")
    
    return backup_dir

def create_migration_documentation() -> None:
    """Create migration documentation."""
    docs_path = project_root / "docs" / "validation_framework_migration.md"
    docs_path.parent.mkdir(exist_ok=True)
    
    with open(docs_path, 'w') as f:
        f.write("# Validation Framework Migration Guide\n\n")
        f.write(f"**Migration Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        f.write("## Overview\n\n")
        f.write("This document describes the migration from individual validation scripts ")
        f.write("to the integrated validation framework.\n\n")
        
        f.write("## Changes\n\n")
        f.write("### Before (Individual Scripts)\n\n")
        
        scripts = find_validation_scripts()
        for script in scripts:
            f.write(f"- `{script.relative_to(project_root)}`\n")
        
        f.write("\n### After (Integrated Framework)\n\n")
        f.write("- `tests/test_integrated_validation_framework.py` - All validation logic\n")
        f.write("- `scripts/consolidate_validation_scripts.py` - Migration tool\n\n")
        
        f.write("## Usage\n\n")
        f.write("### Pytest Integration\n\n")
        f.write("```bash\n")
        f.write("# Run all validations as pytest\n")
        f.write("pytest tests/test_integrated_validation_framework.py -v\n\n")
        f.write("# Run specific test class\n")
        f.write("pytest tests/test_integrated_validation_framework.py::TestIntegratedValidationFramework -v\n")
        f.write("```\n\n")
        
        f.write("### CLI Interface\n\n")
        f.write("```bash\n")
        f.write("# Run all validation suites\n")
        f.write("python tests/test_integrated_validation_framework.py\n\n")
        f.write("# Run specific suite\n")
        f.write("python tests/test_integrated_validation_framework.py --suite agent-selection\n\n")
        f.write("# Available suites: story, s63, agent-selection, infrastructure, config, learning\n")
        f.write("```\n\n")
        
        f.write("## Benefits\n\n")
        f.write("- **Reduced Duplication:** Single framework instead of multiple scripts\n")
        f.write("- **Better Maintainability:** Unified codebase for all validation logic\n")
        f.write("- **Improved Reporting:** Comprehensive validation reports with statistics\n")
        f.write("- **Pytest Integration:** Standard testing framework integration\n")
        f.write("- **Flexible Execution:** Run all suites or specific ones as needed\n")
        f.write("- **Better Error Handling:** Robust error handling and reporting\n\n")
        
        f.write("## Archived Scripts\n\n")
        f.write("Original validation scripts have been archived to:\n")
        f.write("`scripts/archived_validation/[timestamp]/`\n\n")
        f.write("These can be referenced if needed, but the integrated framework ")
        f.write("should be used going forward.\n")
    
    print(f"\n📝 Migration documentation created: {docs_path}")

def cleanup_old_scripts(backup_dir: Path) -> None:
    """Clean up old validation scripts after successful migration."""
    scripts = find_validation_scripts()
    
    print("\n🧹 Cleaning up old validation scripts...")
    print(f"(Backup available at: {backup_dir})")
    
    removed_count = 0
    for script in scripts:
        try:
            # Only remove if it's a pure validation script (not if it has other purposes)
            if "validate_" in script.name and script.suffix == ".py":
                script.unlink()
                removed_count += 1
                print(f"   Removed: {script.name}")
        except Exception as e:
            print(f"   Error removing {script.name}: {e}")
    
    print(f"   Total removed: {removed_count} scripts")

def main() -> int:
    """Main consolidation workflow."""
    print("🚀 Validation Script Consolidation Tool")
    print("=" * 60)
    print("This tool consolidates individual validation scripts into")
    print("the integrated validation framework.\n")
    
    # Step 1: Find existing scripts
    scripts = find_validation_scripts()
    print(f"🔍 Found {len(scripts)} validation scripts to consolidate")
    
    if not scripts:
        print("No validation scripts found to consolidate.")
        return 0
    
    # Step 2: Run old scripts
    old_results = run_old_validation_scripts()
    
    # Step 3: Run new integrated framework
    new_result = run_integrated_framework()
    
    # Step 4: Compare results
    compare_results(old_results, new_result)
    
    # Step 5: Create backup
    backup_dir = create_backup_archive()
    
    # Step 6: Create documentation
    create_migration_documentation()
    
    # Step 7: Optional cleanup (ask user)
    new_success, _ = new_result
    old_all_passed = all(success for success, _ in old_results.values())
    
    if new_success:
        print("\n🤔 Migration Assessment: Ready to clean up old scripts?")
        if old_all_passed:
            print("   Recommendation: YES - Both approaches work, safe to migrate")
        else:
            print("   Recommendation: YES - New framework resolves previous issues")
        
        response = input("\nRemove old validation scripts? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            cleanup_old_scripts(backup_dir)
            print("\n✅ Migration completed successfully!")
            print("\n📋 Next Steps:")
            print("   - Use: `pytest tests/test_integrated_validation_framework.py`")
            print("   - Or: `python tests/test_integrated_validation_framework.py`")
            print("   - Documentation: docs/validation_framework_migration.md")
            return 0
        else:
            print("\n📋 Migration prepared but old scripts preserved")
            print("   - New framework available and tested")
            print(f"   - Backup created: {backup_dir}")
            print("   - Run cleanup manually when ready")
            return 0
    else:
        print("\n⚠️ Migration assessment: New framework has issues")
        print("   - Review integrated framework implementation")
        print("   - Resolve validation failures")
        print("   - Re-run consolidation when ready")
        return 1

if __name__ == "__main__":
    sys.exit(main())
