from collections import OrderedDict
from random import shuffle as random_shuffle
from sys import argv as sys_argv
from time import sleep as time_sleep
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
    dealer_stand_value = 17

    # TODO: add explanation.
    minimum_required_deck_size = 16

    def __init__(self, deck):
        self.deck = deck
        self.dealer_hand = Hand()
        self.game_over = False
        self.player_hand = Hand()
        self.player_standing = False

    def deal(self):
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())

    def dealer_hit(self):
        self.dealer_hand.add_card(self.deck.deal_card())

    def end(self):
        self.game_over = True

    def does_dealer_bust(self):
        return self.dealer_hand.get_value() > 21

    def does_dealer_have_blackjack(self):
        return (len(self.dealer_hand) == 2) and (self.dealer_hand.get_value() == 21)

    def does_dealer_win(self):
        if self.game_over:
            dealer_value = self.dealer_hand.get_value()
            player_value = self.player_hand.get_value()
            return (dealer_value <= 21) and ((player_value > 21) or (dealer_value > player_value))
        else:
            return False

    def does_player_have_blackjack(self):
        return (len(self.player_hand) == 2) and (self.player_hand.get_value() == 21)

    def does_player_win(self):
        if self.game_over:
            dealer_value = self.dealer_hand.get_value()
            player_value = self.player_hand.get_value()
            return (player_value <= 21) and ((dealer_value > 21) or (player_value > dealer_value))
        else:
            return False

    def get_dealer_display(self):
        cards = ' '.join(map(lambda card: str(card), self.dealer_hand.get_cards()))
        if self.game_over or self.player_standing:
            value = '[{0:02}]'.format(self.dealer_hand.get_value())
        else:
            cards = '??' + cards[2:]
            value = '[??]'
        return value + ' ' + cards

    def get_player_display(self):
        cards = ' '.join(map(lambda card: str(card), self.player_hand.get_cards()))
        value = '[{0:02}]'.format(self.player_hand.get_value())
        return value + ' ' + cards

    def is_game_over(self):
        return self.game_over

    def player_hit(self):
        self.player_hand.add_card(self.deck.deal_card())
        if self.player_hand.get_value() > 21:
            self.game_over = True

    def player_stand(self):
        self.player_standing = True

    def should_dealer_hit(self):
        return self.dealer_hand.get_value() < Game.dealer_stand_value

class Hand:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

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
        return Hand.get_value_considering_aces(values)

class HandTestCase(TestCase):
    def test_get_value_considering_aces(self):
        self.assertEqual(1 + 1, 2)
        self.assertEqual(Hand.get_value_considering_aces([]), 0)
        self.assertEqual(Hand.get_value_considering_aces([2, 3]), 5)
        self.assertEqual(Hand.get_value_considering_aces([2, 9]), 11)
        self.assertEqual(Hand.get_value_considering_aces([2, 9, 2, 9]), 22)
        self.assertEqual(Hand.get_value_considering_aces([10]), 10)
        self.assertEqual(Hand.get_value_considering_aces([10, 10]), 20)
        self.assertEqual(Hand.get_value_considering_aces([10, 11]), 21)
        self.assertEqual(Hand.get_value_considering_aces([10, 10, 10]), 30)
        self.assertEqual(Hand.get_value_considering_aces([10, 10, 11]), 21)
        self.assertEqual(Hand.get_value_considering_aces([10, 11, 11]), 12)
        self.assertEqual(Hand.get_value_considering_aces([10, 11, 11, 11, 11, 11, 11]), 16)
        self.assertEqual(Hand.get_value_considering_aces([11] * 1), 11)
        self.assertEqual(Hand.get_value_considering_aces([11] * 2), 12)
        self.assertEqual(Hand.get_value_considering_aces([11] * 3), 13)
        self.assertEqual(Hand.get_value_considering_aces([11] * 4), 14)
        self.assertEqual(Hand.get_value_considering_aces([11] * 5), 15)
        self.assertEqual(Hand.get_value_considering_aces([11] * 6), 16)
        self.assertEqual(Hand.get_value_considering_aces([11] * 10), 20)
        self.assertEqual(Hand.get_value_considering_aces([11] * 11), 21)
        self.assertEqual(Hand.get_value_considering_aces([11] * 12), 12)

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
            if self.deck.get_size() < Game.minimum_required_deck_size:
                print 'Shuffling deck.'
                self.deck = Deck()
            game = Game(self.deck)
            game.deal()
            self.print_state(game)
            if game.does_dealer_have_blackjack():
                if game.does_player_have_blackjack():
                    print 'Both dealer and player have blackjack.'
                else:
                    print 'Dealer has blackjack.'
                game.end()
            elif game.does_player_have_blackjack():
                print 'Player has blackjack.'
                game.end()
            if game.is_game_over():
                self.print_state(game)
            else:
                while self.query_hit(name):
                    player_value = game.player_hit()
                    self.print_state(game)
                    if game.is_game_over():
                        print '{0} busts.'.format(name)
                        break
                if not game.is_game_over():
                    game.player_stand()
                    self.print_state(game)
                    while game.should_dealer_hit():
                        print 'Dealer hitting...'
                        time_sleep(1)
                        game.dealer_hit()
                        self.print_state(game)
                    game.end()
                    if game.does_dealer_bust():
                        print 'Dealer busts.'
                    else:
                        print 'Dealer stands.'
            if game.does_dealer_win():
                print 'Dealer wins.'
            elif game.does_player_win():
                print 'Player wins.'
            else:
                print 'Push, dealer and player tie.'
        print 'Thank you for playing {0}.'.format(name)
        print 'Your final bankroll is ${0}.'.format(self.player.get_bankroll())

def play():
    session = Session()
    session.play()

def main():
    if len(sys_argv) == 1:
        play()
    elif sys_argv[1] == '--unittest':
        unittest_main(argv=[sys_argv[0]])
    else:
        print 'Usage: python {0} [--unittest]'.format(sys_argv[0])

if __name__ == '__main__':
    main()
