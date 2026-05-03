"""Tests for time_adjusted_grid module."""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import time_adjusted_grid as tim_adj


class TestTimeDifference:
    """Test cases for time_difference function."""
    
    def test_exact_match(self):
        """Test when user input exactly matches data time point."""
        result = tim_adj.time_difference("09:30", "9:30 AM", index_time=0)
        assert result == 1.0, "Exact match should return weight of 1.0"
    
    def test_exact_match_with_index(self):
        """Test exact match with index_time parameter."""
        result = tim_adj.time_difference("14:00", "2:00 PM", index_time=0)
        assert result == 1.0, "Exact match should return weight of 1.0 regardless of index_time"
    
    def test_am_pm_conversion(self):
        """Test correct handling of AM/PM conversion."""
        # 9:00 AM
        result1 = tim_adj.time_difference("09:00", "9:00 AM", index_time=0)
        assert result1 == 1.0, "AM time should be converted correctly"
        
        # 9:00 PM (21:00 in 24-hour format)
        result2 = tim_adj.time_difference("21:00", "9:00 PM", index_time=0)
        assert result2 == 1.0, "PM time should be converted correctly"
    
    def test_index_time_affects_weight(self):
        """Test that index_time parameter affects the calculated weight."""
        result_no_index = tim_adj.time_difference("09:00", "10:00 AM", index_time=0)
        result_with_index = tim_adj.time_difference("09:00", "10:00 AM", index_time=5)
        
        # With index_time, difference should be 60+5=65 instead of 60
        assert result_with_index != result_no_index, "index_time should affect the result"
        assert result_with_index < result_no_index, "Adding index_time should decrease weight"
    
    def test_large_time_difference(self):
        """Test weight calculation for large time differences."""
        # 12 hour difference
        result = tim_adj.time_difference("09:00", "9:00 PM", index_time=0)
        # Result should be very small for such a large difference
        assert result > 0, "Weight should be positive"
        assert result < 0.001, "Large time difference should result in small weight"
    
    def test_noon_times(self):
        """Test handling of noon times."""
        result = tim_adj.time_difference("12:00", "12:00 PM", index_time=0)
        assert result == 1.0, "12:00 PM should match 12:00"
    
    def test_return_type_is_float(self):
        """Test that time_difference returns a float value."""
        result = tim_adj.time_difference("12:00", "1:00 PM", index_time=0)
        assert isinstance(result, (float, int)), "Return value should be numeric"
    
    def test_small_time_difference_produces_weight(self):
        """Test that small time differences produce valid weights."""
        result = tim_adj.time_difference("12:00", "12:01 PM", index_time=0)
        assert result > 0, "Should produce positive weight"
        assert not np.isnan(result) and not np.isinf(result), "Result should be finite"
    
    def test_negative_difference_produces_valid_weight(self):
        """Test that function handles midnight wraparound gracefully."""
        # The function should handle negative differences
        result = tim_adj.time_difference("23:00", "1:00 AM", index_time=0)
        assert result > 0, "Result should be positive"
        assert not np.isnan(result) and not np.isinf(result), "Result should be finite"
