from day_07 import categorize_hand, get_hands_and_bids, get_total_winnings


if __name__ == "__main__":
    sorted_hands_and_bids = sorted(get_hands_and_bids(), key=lambda hb: categorize_hand(hb[0], with_jokers=True))
    print(get_total_winnings(sorted_hands_and_bids))
