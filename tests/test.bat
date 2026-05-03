@echo off
REM Windows batch file for running tests

if "%1"=="" goto help

if /i "%1"=="all" (
    python -m pytest tests/ -v
    goto end
)

if /i "%1"=="coverage" (
    python -m pytest tests/ --cov=./ --cov-report=html
    echo Coverage report generated in htmlcov/index.html
    goto end
)

if /i "%1"=="quick" (
    python -m pytest tests/ -q
    goto end
)

if /i "%1"=="unit" (
    python -m pytest tests/ -v -m unit
    goto end
)

if /i "%1"=="watch" (
    python -m pytest tests/ -v --looponfail
    goto end
)

if /i "%1"=="help" (
    goto help
)

goto end

:help
echo Usage: test.bat [command]
echo.
echo Commands:
echo   all       Run all tests with verbose output
echo   coverage  Run tests and generate coverage report
echo   quick     Run tests with minimal output
echo   unit      Run only unit tests
echo   watch     Run tests in watch mode (requires pytest-watch)
echo   help      Show this help message
echo.

:end
