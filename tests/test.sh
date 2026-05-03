#!/bin/bash
# Unix/Linux/Mac script for running tests

case "$1" in
    all)
        python -m pytest tests/ -v
        ;;
    coverage)
        python -m pytest tests/ --cov=./ --cov-report=html
        echo "Coverage report generated in htmlcov/index.html"
        ;;
    quick)
        python -m pytest tests/ -q
        ;;
    unit)
        python -m pytest tests/ -v -m unit
        ;;
    watch)
        python -m pytest tests/ -v --looponfail
        ;;
    help|--help|-h)
        echo "Usage: ./test.sh [command]"
        echo ""
        echo "Commands:"
        echo "  all       Run all tests with verbose output"
        echo "  coverage  Run tests and generate coverage report"
        echo "  quick     Run tests with minimal output"
        echo "  unit      Run only unit tests"
        echo "  watch     Run tests in watch mode (requires pytest-watch)"
        echo "  help      Show this help message"
        echo ""
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run './test.sh help' for usage information"
        exit 1
        ;;
esac
