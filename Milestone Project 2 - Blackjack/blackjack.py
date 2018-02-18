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

    def get_size(self):
        return len(self.cards)

    def get_values(self):
        return map(lambda card: card.get_value(), self.cards)

    def shuffle(self):
        shuffle(self.cards)

class Game:
    def __init__(self, deck):
        self.deck = deck
        self.dealer_hand = Hand()
        self.player_hand = Hand()

    @staticmethod
    def get_minimum_required_deck_size():
        # TODO: add explanation.
        return 16

    def play(self):
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        print self.dealer_hand, self.player_hand

class Hand:
    def __init__(self):
        self.cards = []

    def __repr__(self):
        string = reduce(lambda card_a, card_b: str(card_a) + ',' + str(card_b), self.cards)
        return string + ' ' + str(self.get_value())

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        return reduce(lambda card_a, card_b: card_a.get_value() + card_b.get_value(), self.cards)

class Player:
    def __init__(self):
        self.name = 'Player'
        self.bankroll = 20

    def __repr__(self):
        return str(self.name)

    def credit_bankroll(self, credit):
        self.bankroll += credit

    def get_bankroll(self):
        return self.bankroll;

class Set:
    minimum_required_deck_size = Game.get_minimum_required_deck_size()

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):
        while self.deck.get_size() >= Set.minimum_required_deck_size:
            game = Game(self.deck)
            game.play()

def main():
    set = Set()
    set.play()

if __name__ == '__main__':
    main()
