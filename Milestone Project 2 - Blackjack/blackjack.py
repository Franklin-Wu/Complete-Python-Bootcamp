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
        self.shuffle()

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

    def deal(self):
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        print self.dealer_hand, self.player_hand

    def view_dealer(self):
        return ' '.join(['??', str(self.dealer_hand.get_cards()[1])])

    def view_player(self):
        return ' '.join(map(lambda card: str(card), self.player_hand.get_cards()))

class Hand:
    def __init__(self):
        self.cards = []

    def __repr__(self):
        string = reduce(lambda card_a, card_b: str(card_a) + ',' + str(card_b), self.cards)
        return string + ' ' + str(self.get_value())

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def get_value(self):
        return reduce(lambda card_a, card_b: card_a.get_value() + card_b.get_value(), self.cards)

class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll

    def __repr__(self):
        return str(self.name)

    def credit_bankroll(self, credit):
        self.bankroll += credit

    def get_bankroll(self):
        return self.bankroll

    def get_name(self):
        return self.name

class Session:
    def __init__(self):
        self.deck = Deck()
        self.player = Player('Player', 20)

    def play(self):
        name = self.player.get_name()
        print 'Welcome to Blackjack {0}.'.format(name)
        print 'Your initial bankroll is ${0}.'.format(self.player.get_bankroll())
        end_session = False
        while not end_session:
            bankroll = self.player.get_bankroll()
            prompt = '{0}, what is your bet (0 to quit, 1 - {1} to play)? $'.format(name, bankroll)
            while True:
                string = raw_input(prompt)
                if string.isdigit() and int(string) in xrange(0, self.player.get_bankroll() + 1):
                    if int(string) == 0:
                        end_session = True
                    break
                else:
                    print 'Invalid input.'
            if self.deck.get_size() < Game.get_minimum_required_deck_size():
                print 'Shuffling new deck.'
                self.deck = Deck()
            game = Game(self.deck)
            game.deal()
            print game.view_dealer()
            print game.view_player()
        print 'Thank you for playing {0}.'.format(name)
        print 'Your final bankroll is ${0}.'.format(self.player.get_bankroll())

def main():
    session = Session()
    session.play()

if __name__ == '__main__':
    main()
