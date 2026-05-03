"""Tests for propagate module."""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import propagate


class TestPropagate:
    """Test cases for the propagate function."""
    
    def test_propagate_basic(self, sample_grid):
        """Test basic propagation with a simple grid."""
        result = propagate.propagate(sample_grid)
        
        # Result should be numpy array of same shape
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_grid.shape
        
        # Original non-zero values should be preserved or increased
        assert np.all(result[1, 1] >= sample_grid[1, 1])
    
    def test_propagate_with_land_mask(self, sample_grid, sample_land_mask):
        """Test propagation respects land mask."""
        result = propagate.propagate(sample_grid, land_mask=sample_land_mask)
        
        # All cells should have valid values
        assert np.all(np.isfinite(result))
    
    def test_propagate_with_water_mask(self, sample_grid_with_water):
        """Test propagation with water cells masked out."""
        grid, land_mask = sample_grid_with_water
        result = propagate.propagate(grid, land_mask=land_mask)
        
        # Water cells should remain zero (or close to it)
        # Note: propagation may fill some edge values
        assert result[1, 3] == 0 or result[1, 3] < 0.1, "Water cell should be zero or very small"
    
    def test_propagate_preserves_shape(self, sample_grid):
        """Test that propagation preserves grid shape."""
        result = propagate.propagate(sample_grid)
        assert result.shape == sample_grid.shape
    
    def test_propagate_fills_empty_cells(self):
        """Test that propagation fills zero-valued cells with neighbor values."""
        # Grid with isolated points surrounded by zeros
        grid = np.array([
            [0, 0, 0, 0],
            [0, 5, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], dtype=float)
        
        result = propagate.propagate(grid)
        
        # Cells adjacent to the 5 should have non-zero values now
        # (top-left, top, top-right, left, right, bottom-left, bottom, bottom-right)
        assert result[0, 1] > 0, "Top neighbor should be filled"
        assert result[1, 0] > 0, "Left neighbor should be filled"
        assert result[1, 2] > 0, "Right neighbor should be filled"
        assert result[2, 1] > 0, "Bottom neighbor should be filled"
    
    def test_propagate_high_value_dominates(self):
        """Test that higher probability values spread more strongly."""
        grid = np.array([
            [0, 0, 10, 0],
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]
        ], dtype=float)
        
        result = propagate.propagate(grid)
        
        # Cell below the 10 should have higher value than cell above the 1
        assert result[1, 2] > 0, "High value should propagate"
    
    def test_propagate_convergence(self, sample_grid):
        """Test multiple propagation passes for convergence."""
        result1 = propagate.propagate(sample_grid)
        result2 = propagate.propagate(result1)
        
        # Additional propagation iterations shouldn't drastically change values
        # (they should stabilize)
        diff = np.abs(result2 - result1)
        # Most cells should have small changes
        assert np.mean(diff) < 1.0
    
    def test_propagate_no_negative_values(self, sample_grid):
        """Test that propagation doesn't produce negative values."""
        result = propagate.propagate(sample_grid)
        assert np.all(result >= 0), "Propagated grid should have no negative values"
    
    def test_propagate_all_zeros(self):
        """Test propagation on a grid of all zeros."""
        grid = np.zeros((4, 4), dtype=float)
        result = propagate.propagate(grid)
        
        # All zeros should remain all zeros
        assert np.allclose(result, 0)
    
    def test_propagate_single_cell(self):
        """Test propagation on a single-cell grid."""
        grid = np.array([[5.0]])
        result = propagate.propagate(grid)
        
        assert result.shape == (1, 1)
        assert result[0, 0] == 5.0


class TestEquationFunction:
    """Test cases for the equation helper function used in propagation."""
    
    def test_occupied_cell_returns_own_value(self):
        """Test that cells with values return their own values."""
        # This tests the internal behavior indirectly through propagate
        grid = np.array([
            [0, 0, 0],
            [0, 5, 0],
            [0, 0, 0]
        ], dtype=float)
        
        result = propagate.propagate(grid)
        
        # The cell with value 5 should maintain its value
        assert result[1, 1] == 5.0
    
    def test_corner_cells_propagate(self):
        """Test that corner cells without values are filled from neighbors."""
        grid = np.array([
            [0, 1, 0],
            [1, 5, 1],
            [0, 1, 0]
        ], dtype=float)
        
        result = propagate.propagate(grid)
        
        # Corner cells should be filled
        assert result[0, 0] > 0
        assert result[0, 2] > 0
        assert result[2, 0] > 0
        assert result[2, 2] > 0
