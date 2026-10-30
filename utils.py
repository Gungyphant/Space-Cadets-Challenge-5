import math
from numbers import Number
from typing import SupportsIndex, Generator
from decimal import Decimal


def frange(start: Number, stop: Number, step: Number, inclusive: bool = False) -> Generator[Number]:
    value = start
    while value < stop:
        yield value
        value += step
    if inclusive:
        yield stop

def lcm(*integers: SupportsIndex) -> int:
    # Discard 0s:
    integers = [n for n in integers if n != 0]
    return math.lcm(*integers)

PreciseNumber = int | Decimal
Number = PreciseNumber | float

def sin(val: Number) -> Number:
    if isinstance(val, Decimal):
        return Decimal(math.sin(float(val)))
    else:
        return math.sin(val)

def cos(val: Number) -> Number:
    if isinstance(val, Decimal):
        return Decimal(math.cos(float(val)))
    else:
        return math.cos(val)

pi = Decimal(math.pi)
