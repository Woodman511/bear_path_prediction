# Testing Guide for Bear Path Prediction

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with coverage report
```bash
pytest --cov=./ --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_propagate.py
```

### Run specific test class or function
```bash
pytest tests/test_time_adjusted_grid.py::TestTimeDifference::test_exact_match
```

### Run tests matching a pattern
```bash
pytest -k "propagate"
```

### Run with verbose output
```bash
pytest -vv
```

### Run with print statements visible
```bash
pytest -s
```

## Test Structure

The test suite is organized into several test modules:

- **test_time_adjusted_grid.py**: Tests for time-based weight calculations
- **test_propagate.py**: Tests for probability propagation algorithm
- **test_freqency_grid.py**: Tests for grid creation and coordinate conversion
- **test_path_find.py**: Tests for pathfinding algorithm
- **test_graph_prob.py**: Tests for visualization functions
- **test_integration.py**: End-to-end integration tests

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `sample_data_csv`: Temporary CSV file with sample bear tracking data
- `sample_grid`: Simple probability grid for testing
- `sample_land_mask`: Land/water mask for grid cells
- `sample_grid_with_water`: Grid combined with a realistic land mask

## Test Categories

Tests are marked with pytest markers for organization:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.visualization`: Visualization tests

Run only specific categories:
```bash
pytest -m unit
pytest -m "not slow"
```

## Coverage

To generate an HTML coverage report:

```bash
pytest --cov=./ --cov-report=html
```

Open `htmlcov/index.html` in a browser to view the report.

## Adding New Tests

1. Create test functions starting with `test_`
2. Group related tests in test classes starting with `Test`
3. Use descriptive names for test functions
4. Add docstrings explaining what is being tested
5. Use fixtures from `conftest.py` for common test data

Example:

```python
def test_new_feature(sample_grid):
    """Test description."""
    result = some_function(sample_grid)
    assert result is not None
```

## Continuous Integration

Tests can be run automatically before commits using git hooks.
To set up a pre-commit hook:

```bash
echo '#!/bin/sh\npytest' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
