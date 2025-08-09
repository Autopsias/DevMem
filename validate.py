#!/usr/bin/env python3
"""
Claude Code Agent System - Unified Validation CLI

This is the main entry point for running all validation checks.
It provides a simplified interface to the integrated validation framework.

Usage:
    python validate.py                    # Run all validations
    python validate.py --suite story      # Run specific suite
    python validate.py --list             # List available suites
    python validate.py --help             # Show help
"""

import sys
import argparse
from pathlib import Path

# Add tests to path for framework import
sys.path.insert(0, str(Path(__file__).parent / 'tests'))

def list_available_suites():
    """List all available validation suites."""
    suites = {
        "all": "Run all validation suites (default)",
        "story": "S6.1 Claude Code Performance Optimization story completion",
        "s63": "S6.3 Enhanced Testing Framework Implementation", 
        "agent-selection": "Enhanced agent selection system validation",
        "infrastructure": "Infrastructure learning improvements validation",
        "config": "Native configuration (.claude/settings.json) validation",
        "agents": "Claude Code agent framework structure (.claude/agents/) validation",
        "learning": "Claude Code agent learning comprehensive validation"
    }
    
    print("📋 Available Validation Suites:")
    print("" + "=" * 50)
    
    for suite_id, description in suites.items():
        print(f"  {suite_id:<15} - {description}")
    
    print("\n🚀 Usage Examples:")
    print("  python validate.py                    # Run all suites")
    print("  python validate.py --suite story      # Run story validation only")
    print("  python validate.py --suite learning   # Run learning validation only")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Claude Code Agent System - Unified Validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate.py                    # Run all validations
  python validate.py --suite story      # Run story completion validation
  python validate.py --suite learning   # Run agent learning validation
  python validate.py --list             # List available suites
  python validate.py --verbose          # Enable verbose output
        """
    )
    
    parser.add_argument(
        "--suite", 
        choices=["story", "s63", "agent-selection", "infrastructure", "config", "agents", "learning", "all"],
        default="all",
        help="Specific validation suite to run (default: all)"
    )
    
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List all available validation suites"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Handle --list option
    if args.list:
        list_available_suites()
        return 0
    
    # Import and run the integrated validation framework
    try:
        from test_integrated_validation_framework import IntegratedValidationFramework
        
        print("🚀 Claude Code Agent System - Unified Validation")
        print("=" * 60)
        
        if args.suite != "all":
            print(f"Running {args.suite} validation suite...")
        else:
            print("Running all validation suites...")
        
        print()
        
        # Create and run framework
        framework = IntegratedValidationFramework(args.project_root)
        
        if args.suite == "all":
            success = framework.run_all_validations()
        else:
            # Run specific suite
            suite_map = {
                "story": framework._validate_story_completion,
                "s63": framework._validate_s63_implementation, 
                "agent-selection": framework._validate_agent_selection,
                "infrastructure": framework._validate_infrastructure_learning,
                "config": framework._validate_native_config,
                "agents": framework._validate_agent_framework_structure,
                "learning": framework._validate_claude_code_agent_learning
            }
            
            validator = suite_map[args.suite]
            results = validator()
            success = all(r.passed for r in results)
            
            # Print results for single suite
            print(f"\n📋 {args.suite.title()} Validation Results:")
            print("-" * 40)
            
            for result in results:
                status = "✅" if result.passed else "❌"
                details = f" ({result.details})" if result.details else ""
                score = f" [{result.score:.1%}]" if result.score is not None else ""
                print(f"  {status} {result.name}{score}{details}")
            
            passed_count = sum(1 for r in results if r.passed)
            total_count = len(results)
            
            print(f"\n📈 Summary: {passed_count}/{total_count} validations passed")
            print(f"Overall: {'✅ PASSED' if success else '❌ FAILED'}")
        
        return 0 if success else 1
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running from the project root directory.")
        return 1
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
