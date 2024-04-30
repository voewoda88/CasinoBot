from functools import lru_cache
from typing import List
from fluent.runtime import FluentLocalization

@lru_cache(maxsize=64)
def get_score_change(dice_value: int, bet_value: int) -> int:
    if dice_value in (1, 22, 43):
        return bet_value * 7
    elif dice_value in (16, 32, 48):
        return bet_value * 5
    elif dice_value == 64:
        return bet_value * 10
    else:
        return -bet_value

def get_combo_parts(dice_value: int) -> List[str]:
    values = ["bar", "grapes", "lemon", "seven"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result


@lru_cache(maxsize=64)
def get_combo_text(dice_value: int, l10n: FluentLocalization) -> str:
    parts: list[str] = get_combo_parts(dice_value)
    for i in range(len(parts)):
        parts[i] = l10n.format_value(parts[i])
    return ", ".join(parts)