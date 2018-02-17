from collections import OrderedDict
from random import shuffle

card_values = OrderedDict()
card_values['2'] = 2
card_values['3'] = 3
card_values['4'] = 4
card_values['5'] = 5
card_values['6'] = 6
card_values['7'] = 7
card_values['8'] = 8
card_values['9'] = 9
card_values['T'] = 10
card_values['J'] = 10
card_values['Q'] = 10
card_values['K'] = 10
card_values['A'] = 11

card_suits = [
    'C',
    'D',
    'H',
    'S',
]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return self.value + self.suit

    def get_value(self):
        return card_values[self.value]

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in card_values.keys() for suit in card_suits]

    def __repr__(self):
        return str(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def get_card_count(self):
        return len(self.cards)

    def get_values(self):
        return map(lambda card: card.get_value(), self.cards)

    def shuffle(self):
        shuffle(self.cards)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.player_hand = Hand()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        return reduce(lambda card_a, card_b: card_a.get_value() + card_b.get_value(), self.cards)

def main():
    deck = Deck()
    print deck
    print deck.get_values()
    deck.shuffle()
    print deck
    print deck.get_values()
    while (deck.get_card_count()):
        card = deck.deal_card()
        print card, card.get_value()

if __name__ == '__main__':
    main()
