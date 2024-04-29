from asyncio import sleep
from contextlib import suppress

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from fluent.runtime import FluentLocalization
from casinobot.Cards_deck import Card, Deck
from casinobot.Calculate_cards import calculate_score, get_card_text
from casinobot.keyboards import get_options_menu, get_games_keyboard, get_return_card_menu


#from Cards_deck
from casinobot.Filters.filters import BlackJackTextFilter, BlackJackHitFilter, RepeatCardFilter, BackFilter, BlackJackStandFilter
from casinobot.config_reader import Settings

flags = {"throttling_key": "default"}
router = Router()

@router.message(RepeatCardFilter(), flags=flags)
async def repeat_card(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
    await black_jack(message, state, l10n, config)

@router.message(BackFilter(), flags=flags)
async def back_card(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("choice-game-text"), reply_markup=get_games_keyboard(l10n))

@router.message(Command("black_jack"), flags=flags)
@router.message(BlackJackTextFilter(), flags=flags)
async def black_jack(message: Message, state: FSMContext, l10n: FluentLocalization, config: Settings):
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

    deck = Deck()
    deck.shuffle()
    player_hand = []
    dealer_hand = []

    for _ in range(2):
        player_hand.append(deck.deal())
        dealer_hand.append(deck.deal())

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    await message.answer(l10n.format_value("start-card-game-text"))

    await message.answer(l10n.format_value(
                    "card-dialer-hidden-text",
                    {
                        "cards": get_card_text(dealer_hand, show_second_card=True)
                    }
    ))

    await message.answer(l10n.format_value(
                    "card-player-text",
                    {
                        "score": player_score,
                        "cards": get_card_text(player_hand)
                    }
    ), reply_markup=get_options_menu(l10n))

    await state.update_data(player_hand=player_hand, dealer_hand=dealer_hand, deck=deck, dealer_score=dealer_score)

@router.message(BlackJackHitFilter(), flags=flags)
async def hit(message: Message, state: FSMContext, l10n: FluentLocalization):
    user_data = await state.get_data()
    player_hand = user_data["player_hand"]
    deck = user_data["deck"]
    dealer_hand = user_data["dealer_hand"]
    dealer_score = user_data["dealer_score"]
    score = user_data["score"]
    bet = user_data["bet"]

    player_hand.append(deck.deal())
    player_score = calculate_score(player_hand)
    await message.answer(l10n.format_value(
        "card-player-text",
         {
              "score": player_score,
              "cards": get_card_text(player_hand)
               }
    ))
    if player_score > 21:
        score = score - bet
        await message.answer(l10n.format_value(
            "card-dialer-text",
            {
                "score": dealer_score,
                "cards": get_card_text(dealer_hand)
            }
        ))
        await message.answer(l10n.format_value(
            "card-game-score-text",
            {
                "score": score
            }
        ))
        await message.answer(l10n.format_value("busted-text"), reply_markup=get_return_card_menu(l10n))
    await state.update_data(player_hand=player_hand, score=score)

@router.message(BlackJackStandFilter(), flags=flags)
async def stand(message: Message, state:FSMContext, l10n:FluentLocalization):
    user_data = await state.get_data()
    dealer_hand = user_data["dealer_hand"]
    player_hand = user_data["player_hand"]
    deck = user_data["deck"]
    score = user_data["score"]
    bet = user_data["bet"]

    dealer_score = calculate_score(dealer_hand)
    while dealer_score < 17:
       dealer_hand.append(deck.deal())
       dealer_score = calculate_score(dealer_hand)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if dealer_score > 21:
        result_text = l10n.format_value("dealer-busted-text")
        bet = bet * 2
        score = score + bet
    elif player_score > dealer_score:
        result_text = l10n.format_value("player-win-text")
        bet = bet * 2
        score = score + bet
    elif player_score < dealer_score:
        result_text = l10n.format_value("dealer-win-text")
        score = score - bet
    else:
        result_text = l10n.format_value("draw-text")
    await state.update_data(score=score)
    await message.answer(l10n.format_value(
        "card-dialer-text",
        {
            "score": dealer_score,
            "cards": get_card_text(dealer_hand)
        }
    ))

    await message.answer(l10n.format_value(
        "card-player-text",
        {
            "score": player_score,
            "cards": get_card_text(player_hand)
        }
    ))

    await message.answer(l10n.format_value(result_text), reply_markup=get_return_card_menu(l10n))
    await message.answer(l10n.format_value(
        "card-game-score-text",
        {
            "score": score
        }
    ))


def calculate_score(hand):
    score = 0
    ace_count = 0

    for card in hand:
        if card.rank in ('Jack', 'Queen', 'King'):
            score += 10
        elif card.rank == 'Ace':
            ace_count += 1
            score += 11
        else:
            score += int(card.rank)

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score


