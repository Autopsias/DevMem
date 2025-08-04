#!/bin/bash

#
# Environment Bridge Hook
# Provides environment detection and bridging functionality for CI/CD environments
#

set -euo pipefail

# Environment detection
detect_ci_environment() {
    if [[ "${CI:-false}" == "true" ]]; then
        echo "CI"
    elif [[ "${GITHUB_ACTIONS:-false}" == "true" ]]; then
        echo "GITHUB_ACTIONS"
    elif [[ "${DOCKER:-false}" == "true" ]]; then
        echo "DOCKER"
    else
        echo "LOCAL"
    fi
}

# Main execution
main() {
    local command="${1:-detect}"

    case "$command" in
        "detect")
            detect_ci_environment
            ;;
        "health")
            echo "OK"
            ;;
        *)
            echo "Usage: $0 [detect|health]"
            exit 1
            ;;
    esac
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
