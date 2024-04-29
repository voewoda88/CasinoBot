from functools import lru_cache

def calculate_score(hand):
    score = 0
    ace_count = 0

    for card in hand:
        if card in ('Jack', 'Queen', 'King'):
            score += 10
        elif card == 'Ace':
            ace_count += 1
            score += 11
        else:
            score += int(card)

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score

def get_card_text(person_hand: list, show_second_card: bool = False) -> str:
    cards: list[str] = []
    for i in range(0, len(person_hand)):
        if i == 1 and show_second_card:
            cards.append("[❔]")
        else:
            cards.append(person_hand[i].__str__())
    return ", ".join(cards)
