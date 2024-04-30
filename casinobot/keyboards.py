from functools import cache

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fluent.runtime import FluentLocalization

@cache
def get_games_keyboard(l10n: FluentLocalization):
    first_row = [
        KeyboardButton(text=l10n.format_value("spin-button-text")),
        KeyboardButton(text=l10n.format_value("black-jack-text")),
        KeyboardButton(text=l10n.format_value("raketka-button-text"))
    ]

    second_row = [
        KeyboardButton(text=l10n.format_value("change-bet-text"))
    ]

    third_row = [
        KeyboardButton(text=l10n.format_value("balance-info-button"))
    ]

    return ReplyKeyboardMarkup(keyboard=[first_row, second_row, third_row], resize_keyboard=True)

@cache
def get_main_menu(l10n: FluentLocalization):
    keyboard = [
        [KeyboardButton(text=l10n.format_value("start-game-text"))]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_return_menu(l10n: FluentLocalization):
    first_row = [
        KeyboardButton(text=l10n.format_value("repeat-game-button-text"))
    ]

    second_row = [
        KeyboardButton(text=l10n.format_value("back-button-text"))
    ]

    return ReplyKeyboardMarkup(keyboard=[first_row, second_row], resize_keyboard=True)

def get_return_card_menu(l10n: FluentLocalization):
    first_row = [
        KeyboardButton(text=l10n.format_value("repeat-card-game-button-text"))
    ]

    second_row = [
        KeyboardButton(text=l10n.format_value("back-button-text"))
    ]

    return ReplyKeyboardMarkup(keyboard=[first_row, second_row], resize_keyboard=True)

@cache
def get_options_menu(l10n: FluentLocalization):
    first_row = [
        KeyboardButton(text=l10n.format_value("get-another-card-text"))
    ]

    second_row = [
        KeyboardButton(text=l10n.format_value("enough-card-text"))
    ]
    return ReplyKeyboardMarkup(keyboard=[first_row, second_row], resize_keyboard=True)

@cache
def get_return_raketka_menu(l10n: FluentLocalization):
    first_row = [
        KeyboardButton(text=l10n.format_value("repeat-raketka-game-button-text"))
    ]

    second_row = [
        KeyboardButton(text=l10n.format_value("back-button-text"))
    ]

    return ReplyKeyboardMarkup(keyboard=[first_row, second_row], resize_keyboard=True)