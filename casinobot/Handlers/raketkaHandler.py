from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.handlers import MessageHandler
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization
from aiogram.fsm.state import State, StatesGroup

from casinobot.Filters.filters import RacketkaTextFilter, RepeatRaketkaFilter, BackFilter
from casinobot.config_reader import Settings
from casinobot.keyboards import get_games_keyboard, get_return_raketka_menu
from casinobot.Generate_coefficient import generate_multiplier

flags = {"throttling_key": "default"}
router = Router()

old_game_state = None

class InputState(StatesGroup):
    waiting_for_input = State()

@router.message(RepeatRaketkaFilter(), flags=flags)
async def repeat_raketka(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    await raketka(message, state, l10n, config)

@router.message(BackFilter(), flags=flags)
async def back_card(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("choice-game-text"), reply_markup=get_games_keyboard(l10n))


@router.message(Command("raketka"), flags=flags)
@router.message(RacketkaTextFilter(), flags=flags)
async def raketka(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
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

    global old_game_state
    old_game_state = await state.get_state()

    await message.answer(l10n.format_value("raketka-grow-up-info-text"), reply_markup=ReplyKeyboardRemove())
    await message.answer(l10n.format_value("raketka-text-input-text"))

    await state.set_state(InputState.waiting_for_input)

@router.message(InputState.waiting_for_input)
async def waiting_for_input(message: Message, state: FSMContext, l10n: FluentLocalization):
    flag: bool = False

    response = message.text
    try:
        if 1 < float(response) < 50:
            flag = True
            await message.answer(l10n.format_value("raketka-succesfull-input-text"))
        else:
            await message.answer(l10n.format_value("raketka-not-succesfull-input-text"),
                                 reply_markup=get_games_keyboard(l10n))

    except ValueError:
        await message.answer(l10n.format_value("raketka-not-succesfull-input-text"), reply_markup=get_games_keyboard(l10n))

    await state.set_state(old_game_state)
    if flag:
        await state.update_data(coefficient=float(response))
        await equals_coefficient(message, state, l10n)
        return

async def equals_coefficient(message: Message, state: FSMContext, l10n: FluentLocalization):
    raketka_coefficient = generate_multiplier()
    user_data = await state.get_data()
    user_coefficient = user_data["coefficient"]
    user_bet = user_data["bet"]
    user_score = user_data["score"]

    if raketka_coefficient > user_coefficient:
        bet = float(user_bet) * user_coefficient
        score = user_score + bet
        await state.update_data(score=score)
        result_text = l10n.format_value("player-raketka-win-text")
    else:
        score = user_score - float(user_bet)
        await state.update_data(score=score)
        result_text = l10n.format_value("player-raketka-lose-text")
    await message.answer(l10n.format_value(
        "raketka-coefficient-text",
        {
            "coefficient": raketka_coefficient
        }
    ))
    await message.answer(l10n.format_value(result_text), reply_markup=get_return_raketka_menu(l10n))
    await message.answer(l10n.format_value(
        "card-game-score-text",
        {
            "score": score
        }
    ))


