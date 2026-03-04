from decimal import Decimal, localcontext, ROUND_HALF_UP, ROUND_HALF_DOWN
from typing import Union

def round_half_up(number: Union[float, int, str], decimal_places: int = 0) -> Union[int, float]:
    """Rounds a number using the "round half up" strategy.

    This strategy rounds to the nearest value, and when the value is exactly
    halfway between two numbers, it rounds away from zero (e.g., 2.5 becomes 3).

    Args:
        number: The number to be rounded. Can be a float, int, or string.
            It is recommended to pass as string if high precision is required.
        decimal_places: The number of decimal places to round to.
            Defaults to 0 for rounding to the nearest integer.

    Raises:
        ValueError: If decimal_places is negative.

    Returns:
        int: If decimal_places is 0, returns the rounded number as an integer.
        float: If decimal_places is > 0, returns the rounded number as a float.
    """
    if decimal_places < 0:
        raise ValueError(f"decimal_places must be non-negative, got {decimal_places}")

    quantizer = Decimal('1e-' + str(decimal_places))

    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_UP
        rounded_decimal = Decimal(str(number)).quantize(quantizer)

    if decimal_places == 0:
        return int(rounded_decimal)
    return float(rounded_decimal)

def round_half_down(number: Union[float, int, str], decimal_places: int = 0) -> Union[int, float]:
    """Rounds a number using the "round half down" strategy.
    
    This strategy rounds to the nearest value, and when the value is exactly 
    halfway between two numbers, it rounds towards zero (e.g., 2.5 becomes 2).

    Args:
        number: The number to be rounded. Can be a float, int, or string.
            It is recommended to pass as string if high precision is required.
        decimal_places: The number of decimal places to round to.
            Defaults to 0 for rounding to the nearest integer.

    Raises:
        ValueError: If decimal_places is negative.

    Returns:
        int: If decimal_places is 0, returns the rounded number as an integer.
        float: If decimal_places is > 0, returns the rounded number as a float.
    """
    if decimal_places < 0:
        raise ValueError(f"decimal_places must be non-negative, got {decimal_places}")

    quantizer = Decimal('1e-' + str(decimal_places))

    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_DOWN
        rounded_decimal = Decimal(str(number)).quantize(quantizer)

    if decimal_places == 0:
        return int(rounded_decimal)
    return float(rounded_decimal)
