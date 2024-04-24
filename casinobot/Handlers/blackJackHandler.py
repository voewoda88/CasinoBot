from asyncio import sleep
from contextlib import suppress

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from Filters.filters import BlackJackTextFilter
from config_reader import Settings

flags = {"throttling_key": "game"}
router = Router()

@router.message(Command("black_jack"), flags=flags)
@router.message(BlackJackTextFilter(), flags=flags)
async def black_jack(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    i = 0