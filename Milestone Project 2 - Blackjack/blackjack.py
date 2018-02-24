from collections import OrderedDict
from random import shuffle as random_shuffle
from sys import argv as sys_argv
from unittest import (
    main as unittest_main,
    TestCase,
)

class Card:
    suits = [
        'C',
        'D',
        'H',
        'S',
    ]

    values = OrderedDict()
    values['2'] = 2
    values['3'] = 3
    values['4'] = 4
    values['5'] = 5
    values['6'] = 6
    values['7'] = 7
    values['8'] = 8
    values['9'] = 9
    values['T'] = 10
    values['J'] = 10
    values['Q'] = 10
    values['K'] = 10
    values['A'] = 11 # can also be 1, which is handled in Hand.get_value()

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return self.value + self.suit

    def get_value(self):
        return Card.values[self.value]

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in Card.values.keys() for suit in Card.suits]
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
        random_shuffle(self.cards)

class Game:
    def __init__(self, deck):
        self.deck = deck
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.player_standing = False
        self.game_result = None

    @staticmethod
    def get_minimum_required_deck_size():
        # TODO: add explanation.
        return 16

    def deal(self):
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())

    def get_dealer_display(self):
        cards = ' '.join(map(lambda card: str(card), self.dealer_hand.get_cards()))
        if self.player_standing:
            value = '[' + str(self.dealer_hand.get_value()) + ']'
        else:
            cards = '??' + cards[2:]
            value = '[??]'
        return value + ' ' + cards

    def get_player_display(self):
        cards = ' '.join(map(lambda card: str(card), self.player_hand.get_cards()))
        value = '[{0:02}]'.format(self.player_hand.get_value())
        return value + ' ' + cards

    def hit(self):
        self.player_hand.add_card(self.deck.deal_card())
        return self.player_hand.get_value()

    def lose(self):
        self.game_result = 0

    def stand(self):
        self.player_standing = True
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        return self.dealer_hand.get_value()

class Hand:
    def __init__(self):
        self.cards = []

    def __repr__(self):
        string = reduce(lambda card_a, card_b: str(card_a) + ',' + str(card_b), self.cards)
        return string + ' ' + str(self.get_value())

    @staticmethod
    def get_value_considering_aces(values):
        # An Ace may have a value 11 or 1. Calculate the optimal value by subtracting 10 for each
        # Ace, whose dafault value is 11, until the value is less than 22.
        value = sum(values)
        ace_count = values.count(11)
        while ace_count:
            if value < 22:
                break
            value -= 10
            ace_count -= 1
        return value

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def get_value(self):
        values = map(lambda card: card.get_value(), self.cards)
        return get_value_considering_aces(values)

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

    def print_state(self, game):
        print 'Dealer: {0}'.format(game.get_dealer_display())
        print '{0}: {1}'.format(self.player.get_name(), game.get_player_display())

    def query_hit(self, name):
        prompt = '{0}, would you like a card (y/n)? '.format(name)
        while True:
            string = raw_input(prompt)
            if string == 'y':
                return True
            elif string == 'n':
                return False
            else:
                print 'Invalid input.'

    def query_wager(self, name):
        bankroll = self.player.get_bankroll()
        print
        prompt = '{0}, what is your wager (0 to quit, 1 - {1} to play)? $'.format(name, bankroll)
        while True:
            string = raw_input(prompt)
            if string.isdigit():
                wager = int(string)
                if wager in xrange(0, bankroll + 1):
                    return wager
            print 'Invalid input.'

    def play(self):
        name = self.player.get_name()
        print
        print 'Welcome to Blackjack, {0}.'.format(name)
        print 'Dealer stands on 17 (including soft 17).'
        print 'Your initial bankroll is ${0}.'.format(self.player.get_bankroll())
        while True:
            wager = self.query_wager(name)
            if not wager:
                break;
            if self.deck.get_size() < Game.get_minimum_required_deck_size():
                print 'Shuffling new deck.'
                self.deck = Deck()
            game = Game(self.deck)
            game.deal()
            self.print_state(game)
            while self.query_hit(name):
                player_value = game.hit()
                self.print_state(game)
                if player_value > 21:
                    game.lose()
                    break
            game.stand()
            self.print_state(game)
        print
        print 'Thank you for playing {0}.'.format(name)
        print 'Your final bankroll is ${0}.'.format(self.player.get_bankroll())

class TestSample(TestCase):
    def test_sample_bad(self):
        self.assertEqual(1 + 1, 3)

    def test_sample_good(self):
        self.assertEqual(1 + 1, 2)

def play():
    '''
    session = Session()
    session.play()
    '''
    print Hand.get_value_considering_aces([10, 11])
    print Hand.get_value_considering_aces([11, 11])
    print Hand.get_value_considering_aces([11, 11, 11])
    print Hand.get_value_considering_aces([10, 10, 10])

def main():
    if len(sys_argv) == 1:
        play()
    elif sys_argv[1] == '--unittest':
        unittest_main(argv=[sys_argv[0]])
    else:
        print 'Usage: python {0} [--unittest]'.format(sys_argv[0])

if __name__ == '__main__':
    main()
