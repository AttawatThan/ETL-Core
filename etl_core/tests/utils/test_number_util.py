import pytest
from etl_core.utils.number_util import round_half_up, round_half_down

class TestNumberUtil:
    """TestSuite for the Number Utility functions."""

    # ==========================================
    # Tests for round_half_up
    # ==========================================
    def test_round_half_up_to_integer(self):
        """Tests standard round half up to 0 decimal places (integer)."""
        assert round_half_up(2.4) == 2
        assert round_half_up(2.5) == 3
        assert round_half_up(2.6) == 3
        
    def test_round_half_up_with_decimals(self):
        """Tests round half up with specific decimal places."""
        assert round_half_up(2.54, 1) == 2.5
        assert round_half_up(2.55, 1) == 2.6
        assert round_half_up(2.555, 2) == 2.56 

    def test_round_half_up_negative_numbers(self):
        """Tests round half up with negative numbers (away from zero)."""
        assert round_half_up(-2.4) == -2
        assert round_half_up(-2.5) == -3
        assert round_half_up(-2.6) == -3

    def test_round_half_up_string_input(self):
        """Tests that passing string values works correctly and prevents float imprecision."""
        assert round_half_up("2.5") == 3
        assert round_half_up("2.555", 2) == 2.56

    def test_round_half_up_integer_input(self):
        """Tests that passing an integer works correctly."""
        assert round_half_up(2) == 2
        assert round_half_up(2, 2) == 2.0

    def test_round_half_up_zero(self):
        """Tests that zero is handled correctly."""
        assert round_half_up(0) == 0
        assert round_half_up(0.0, 2) == 0.0

    def test_round_half_up_invalid_decimal_places(self):
        """Tests that negative decimal_places raises ValueError."""
        with pytest.raises(ValueError):
            round_half_up(2.5, -1)

    def test_round_half_up_invalid_string_input(self):
        """Tests that a non-numeric string raises an exception."""
        from decimal import InvalidOperation
        with pytest.raises(InvalidOperation):
            round_half_up("abc")

    # ==========================================
    # Tests for round_half_down
    # ==========================================
    def test_round_half_down_to_integer(self):
        """Tests standard round half down to 0 decimal places (integer)."""
        assert round_half_down(2.4) == 2
        assert round_half_down(2.5) == 2
        assert round_half_down(2.6) == 3
        
    def test_round_half_down_with_decimals(self):
        """Tests round half down with specific decimal places."""
        assert round_half_down(2.54, 1) == 2.5
        assert round_half_down(2.55, 1) == 2.5
        assert round_half_down(2.555, 2) == 2.55

    def test_round_half_down_negative_numbers(self):
        """Tests round half down with negative numbers (towards zero)."""
        assert round_half_down(-2.4) == -2
        assert round_half_down(-2.5) == -2
        assert round_half_down(-2.6) == -3

    def test_round_half_down_string_input(self):
        """Tests that passing string values works correctly for round half down."""
        assert round_half_down("2.5") == 2
        assert round_half_down("2.555", 2) == 2.55

    def test_round_half_down_integer_input(self):
        """Tests that passing an integer works correctly."""
        assert round_half_down(2) == 2
        assert round_half_down(2, 2) == 2.0

    def test_round_half_down_zero(self):
        """Tests that zero is handled correctly."""
        assert round_half_down(0) == 0
        assert round_half_down(0.0, 2) == 0.0

    def test_round_half_down_invalid_decimal_places(self):
        """Tests that negative decimal_places raises ValueError."""
        with pytest.raises(ValueError):
            round_half_down(2.5, -1)

    def test_round_half_down_invalid_string_input(self):
        """Tests that a non-numeric string raises an exception."""
        from decimal import InvalidOperation
        with pytest.raises(InvalidOperation):
            round_half_down("abc")

    # ==========================================
    # Tests for Return Types
    # ==========================================
    def test_return_types(self):
        """Tests that decimal_places=0 returns int, and >0 returns float."""
        # 0 decimals should return int
        assert isinstance(round_half_up(2.5, 0), int)
        assert isinstance(round_half_down(2.5, 0), int)
        
        # >0 decimals should return float
        assert isinstance(round_half_up(2.5, 1), float)
        assert isinstance(round_half_down(2.5, 1), float)
