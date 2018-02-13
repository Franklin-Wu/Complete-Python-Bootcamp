from collections import OrderedDict

card_ranks_unsorted = {
    '2' : 2,
    '3' : 3,
    'A' : 11,
}

card_ranks = OrderedDict()
card_ranks['2'] = 2
card_ranks['3'] = 3
card_ranks['K'] = 10
card_ranks['A'] = 11

card_suits = [
    'C',
    'D',
    'H',
    'S',
]

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

def main():
    print card_ranks
    print card_suits
    print card_ranks['A']

if __name__ == '__main__':
    main()
