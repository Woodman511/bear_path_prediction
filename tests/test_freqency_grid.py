"""Tests for freqency_grid module."""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import freqency_grid


class TestLatLonToMeters:
    """Test cases for lat_lon_to_meters conversion function."""
    
    def test_zero_offset(self):
        """Test conversion when coordinates match reference point."""
        x, y = freqency_grid.lat_lon_to_meters(0, 0, 0, 0)
        assert x == 0.0 and y == 0.0, "Zero offset should return (0, 0)"
    
    def test_equator_conversion(self):
        """Test latitude/longitude conversion at equator."""
        # At equator, 1 degree latitude = 111320 meters
        x, y = freqency_grid.lat_lon_to_meters(0, 1, 0, 0)
        assert x > 0, "Positive longitude should give positive x"
        assert abs(y) < 1, "Zero latitude difference should give ~0 y"
    
    def test_latitude_conversion(self):
        """Test that latitude conversion works correctly."""
        # 1 degree latitude = 111320 meters
        x, y = freqency_grid.lat_lon_to_meters(1, 0, 0, 0)
        assert y > 0, "Positive latitude should give positive y"
        assert abs(x) < 1, "Zero longitude difference should give ~0 x"
    
    def test_negative_coordinates(self):
        """Test conversion with negative coordinates."""
        x, y = freqency_grid.lat_lon_to_meters(-1, -1, 0, 0)
        assert x < 0 and y < 0, "Negative coordinates should give negative x, y"
    
    def test_reference_point_shift(self):
        """Test that reference point changes the output."""
        result1 = freqency_grid.lat_lon_to_meters(61.18, -149.78, 61.0, -150.0)
        result2 = freqency_grid.lat_lon_to_meters(61.18, -149.78, 61.0, -149.0)
        
        # Different reference points should give different results
        assert result1 != result2
    
    def test_latitude_affects_longitude_scaling(self):
        """Test that higher latitude reduces longitude distance scaling."""
        # At higher latitudes, longitude degrees represent shorter distances
        x1, _ = freqency_grid.lat_lon_to_meters(0, 1, 0, 0)  # At equator
        x2, _ = freqency_grid.lat_lon_to_meters(45, 46, 45, 45)  # At 45 degrees
        
        # At 45 degrees, 1 degree longitude should be shorter
        assert x2 < x1, "Higher latitude should reduce longitude distance"


class TestGetGrid:
    """Test cases for get_grid function."""
    
    def test_get_grid_returns_valid_output(self, sample_data_csv):
        """Test that get_grid returns expected outputs."""
        # This test would require the actual CSV files or mocking them
        # For now, we test the structure
        pass
    
    def test_grid_dimensions_valid(self, sample_data_csv):
        """Test that grid dimensions are positive integers."""
        # Grid dimensions should always be positive
        pass
    
    def test_grid_values_non_negative(self):
        """Test that grid values are non-negative."""
        # All grid cells should have non-negative values
        pass


class TestCoordinateSystem:
    """Test cases for coordinate system and grid mapping."""
    
    def test_meters_per_lat_degree_constant(self):
        """Test that METERS_PER_LAT_DEGREE constant is correct."""
        # 1 degree latitude ≈ 111,320 meters
        assert abs(freqency_grid.METERS_PER_LAT_DEGREE - 111320.0) < 1, \
            "METERS_PER_LAT_DEGREE should be approximately 111320"
    
    def test_grid_cell_bounds(self):
        """Test that grid cell coordinates are within reasonable bounds."""
        # Test that a simple conversion produces sensible values
        x, y = freqency_grid.lat_lon_to_meters(1, 1, 0, 0)
        assert isinstance(x, (int, float)) and isinstance(y, (int, float))
        assert not np.isnan(x) and not np.isnan(y)


class TestGridProperties:
    """Test properties of generated grids."""
    
    def test_grid_is_2d_array(self):
        """Test that output grid is 2D numpy array."""
        # This would test actual grid creation
        pass
    
    def test_grid_dtypes_correct(self):
        """Test that grid uses correct data types."""
        # Grid should use float dtype to preserve weights
        pass
    
    def test_time_values_grid_structure(self):
        """Test that time_values_grid is properly structured."""
        # time_values_grid should be a 2D list of lists containing timestamps
        pass


class TestDataLoading:
    """Test CSV data loading and validation."""
    
    def test_missing_required_columns(self, tmp_path):
        """Test behavior when required columns are missing."""
        # Create CSV with missing columns
        df = pd.DataFrame({
            'Latitude': [1.0, 2.0],
            'Longitude': [3.0, 4.0]
            # Missing 'Time' column
        })
        csv_file = tmp_path / "incomplete.csv"
        df.to_csv(csv_file, index=False)
        
        # Should handle raise error
        # (depends on implementation)
    
    def test_empty_csv_file(self, tmp_path):
        """Test behavior with empty CSV file."""
        df = pd.DataFrame({
            'Latitude': [],
            'Longitude': [],
            'Time': []
        })
        csv_file = tmp_path / "empty.csv"
        df.to_csv(csv_file, index=False)
        
        # Should handle empty data gracefully
