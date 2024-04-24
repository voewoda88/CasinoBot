from aiogram.filters import BaseFilter
from aiogram.types import Message
from fluent.runtime import FluentLocalization

class SpinTextFilter(BaseFilter):
    async def __call__(self, message: Message, l10n: FluentLocalization) -> bool:
        return message.text == l10n.format_value("spin-button-text")

class GamesFilter(BaseFilter):
    async def __call__(self, message: Message, l10n: FluentLocalization) -> bool:
        return message.text == l10n.format_value("start-game-text")

class BetFilter(BaseFilter):
    async def __call__(self, message: Message, l10n: FluentLocalization) -> bool:
        return message.text == l10n.format_value("change-bet-text")