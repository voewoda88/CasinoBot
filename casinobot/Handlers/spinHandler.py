from asyncio import sleep
from contextlib import suppress

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from Filters.filters import SpinTextFilter, RepeatFilter, BackFilter
from config_reader import Settings
from keyboards import get_games_keyboard, get_return_menu
from dice_check import get_score_change, get_combo_text

flags = {"throttling_key": "game"}
router = Router()

@router.message(RepeatFilter(), flags=flags)
async def repeat_spin(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    await spin(message, state, l10n, config)

@router.message(BackFilter(), flags=flags)
async def back_spin(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("choice-game-text"), reply_markup=get_games_keyboard(l10n))

@router.message(Command("spin"), flags=flags)
@router.message(SpinTextFilter(), flags=flags)
async def spin(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    user_data = await state.get_data()
    user_score = user_data.get("score")
    bet_value = user_data.get("bet")

    if user_score == 0:
        if config.send_gameover_sticker:
            with suppress(TelegramBadRequest):
                await message.answer_sticker(l10n.format_value("zero-balance-sticker"))
        await message.answer(l10n.format_value("zero-balance"))
        return


    if user_score < bet_value:
        await message.answer(l10n.format_value("bet-is-greater-than-balance"))
        return

    msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE, reply_markup=ReplyKeyboardRemove())

    score_change = get_score_change(msg.dice.value, bet_value)

    if score_change < 0:
        win_or_lose_text = l10n.format_value("spin-fail")
    else:
        win_or_lose_text = l10n.format_value("spin-success", {"score_change": score_change})

    new_score = user_score + score_change
    await state.update_data(score=new_score)

    await sleep(2.0)
    await msg.reply(
        l10n.format_value(
            "after-spin",
            {
                "combo_text": get_combo_text(msg.dice.value, l10n),
                "dice_value": msg.dice.value,
                "result_text": win_or_lose_text,
                "new_score": new_score
            }
        ), reply_markup=get_return_menu(l10n)
    )
