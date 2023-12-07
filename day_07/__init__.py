import os
from collections import Counter

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
If these cards are different, the hand with the stronger first card is considered stronger.
If the first card in each hand have the same label, however, then move on to considering the second card in each hand.
If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger.
Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger
(and both hands have the same first and second card).
"""

CARD_RANKS = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
CARD_RANKS_WITH_JOKERS = list(reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]))

def get_lines():
    with open(os.path.join(__location__, "input.txt")) as f:
        for line in f.readlines():
            yield line.strip()


def get_hands_and_bids():
    for line in get_lines():
        hand, bid = line.split(" ")
        yield hand, int(bid)


def categorize_hand(hand, with_jokers=False):
    """Returns a tuple of (hand_rank, card_rank_1, ... , card_rank_5) which can used as a sort key"""
    card_counter = Counter(hand)
    card_counts = card_counter.values()
    if "J" in hand and with_jokers:
        joker_count = card_counter.pop("J")
        if joker_count == 5:
            # Special case - put the jokers back
            card_counter["J"] = joker_count
        else:
            top_card = card_counter.most_common(1)[0][0]
            card_counter[top_card] += joker_count

    if 5 in card_counts:
        hand_rank = 6
    elif 4 in card_counts:
        hand_rank = 5
    elif 3 in card_counts and 2 in card_counts:
        hand_rank = 4
    elif 3 in card_counts:
        hand_rank = 3
    elif len(card_counts) == 3:
        hand_rank = 2
    elif len(card_counts) == 4:
        hand_rank = 1
    else:
        hand_rank = 0

    if with_jokers:
        card_ranks = [CARD_RANKS_WITH_JOKERS.index(card) for card in hand]
    else:
        card_ranks = [CARD_RANKS.index(card) for card in hand]
    return hand_rank, *card_ranks


def get_total_winnings(sorted_hands_and_bids):
    return sum((idx + 1) * bid for idx, (_, bid) in enumerate(sorted_hands_and_bids))
