from aiogram.dispatcher.router import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from config_reader import Settings
from keyboards import get_main_menu, get_games_keyboard
from Filters.filters import GamesFilter, BetFilter, CheckBalanceFilter

flags = {"throttling_key": "default"}
router = Router()
old_state = None

class BetState(StatesGroup):
    waiting_for_bet = State()

@router.message(Command("start"), flags=flags)
async def start(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    start_text = l10n.format_value("start-text", {
            "points": config.starting_points,
            "bet": config.starting_bet
        }
    )

    await state.update_data(score=config.starting_points, bet=config.starting_bet)
    await message.answer(start_text, reply_markup=get_main_menu(l10n))

@router.message(Command("stop"), flags=flags)
async def stop(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("stop-text"), reply_markup=ReplyKeyboardRemove())

@router.message(Command("help"), flags=flags)
async def help(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("help-text"), disable_web_page_preview=True)

@router.message(Command("games"), flags=flags)
@router.message(GamesFilter(), flags=flags)
async def games(message: Message, l10n: FluentLocalization):
    choice_text = l10n.format_value("choice-game-text")

    await message.answer(choice_text, reply_markup=get_games_keyboard(l10n))

@router.message(Command("change_bet"), flags=flags)
@router.message(BetFilter(), flags=flags)
async def change_bet(message: Message, l10n: FluentLocalization, state: FSMContext):
    global old_state
    old_state = await state.get_state()

    await message.answer(l10n.format_value("bet-text"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(BetState.waiting_for_bet)

@router.message(BetState.waiting_for_bet)
async def process_bet(message: Message, l10n: FluentLocalization, state: FSMContext):
    user_data = await state.get_data()
    user_score = user_data.get("score")

    flag: bool = False

    response = message.text
    if not response.isdigit():
        await message.reply(l10n.format_value("invalid-bet-text"), reply_markup=get_games_keyboard(l10n))
    elif user_score < int(response):
        await message.reply(l10n.format_value("bet-is-greater-than-balance-text"), reply_markup=get_games_keyboard(l10n))
    else:
        await message.answer(l10n.format_value("complete-bet-text"), reply_markup=get_games_keyboard(l10n))
        flag = True

    await state.set_state(old_state)
    if flag:
        await state.update_data(bet=int(response))

@router.message(Command("check_balance"), flags=flags)
@router.message(CheckBalanceFilter(), flags=flags)
async def check_balance(message: Message, l10n: FluentLocalization, state: FSMContext):
    user_data = await state.get_data()
    user_score = user_data.get("score")

    await message.answer(l10n.format_value("balance-info-text", {"points": user_score}), reply_markup=get_games_keyboard(l10n))