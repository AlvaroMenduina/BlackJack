import numpy as np
import random
import matplotlib.pyplot as plt

class MoneyPot(object):
    def __init__(self, starting_amount, min_bet):
        self.current_pot = starting_amount
        self.min_bet = min_bet
        self.end_game = False

    def check_if_broke(self):
        if self.min_bet > self.current_pot:
            print("You can no longer bet. The Game is LOST")
            self.end_game = True

    def place_bet(self, amount):
        if amount < self.min_bet:
            print ("%d not allowed. Minimum bet: %d" %(amount, self.min_bet))
            self.current_pot -= self.min_bet
        else:
            self.current_pot -= amount


class Hand(object):
    """
    Python object which simulates a single round of Blackjack
    It receives as inputs the current deck of cards, the strategy object and the bet

    When called, it returns the outcome of the round "Win", "Lose" or "Push"
    """
    def __init__(self, cards, strategy, bet_placed):
        self.cards = cards
        self.strategy = strategy
        self.bet_placed = bet_placed
        self.hand_outcome = "Lose"

    def deal_first_hand(self):
        your_1st_card = self.cards.draw_a_card()
        dealers_1st_card = self.cards.draw_a_card()
        your_2nd_card = self.cards.draw_a_card()
        dealers_2nd_card = self.cards.draw_a_card()
        your_hand = [your_1st_card, your_2nd_card]
        dealers_hand = [dealers_1st_card, dealers_2nd_card]
        print ("Dealing first hand")
        print ("Your hand", your_hand)
        print ("Dealer shows a:", dealers_1st_card)
        return your_hand, dealers_hand

    def check_your_first_two_cards(self, your_cards, dealers_cards):
        # See what you have
        card1, card2 = your_cards[0], your_cards[1]
        d_card1 = dealers_cards[0]
        your_hand = "None"
        dealers_hand = "None"

        if (card1 == card2):  # A pair of cards
            if (card1.isdigit()) and (2 <= int(card1) <= 10): # A pair of number cards
                your_hand = "D" + card1
            if (card1 == "J" or card1 == "Q" or card1 == "K"): # A pair of figures
                your_hand = "D10"
            if (card1 == "A"):
                your_hand = "DA"
        if (card1 != card2) & (card1.isdigit()) & (card2.isdigit()): # Two number cards
            your_hand = str(int(card1) + int(card2))
        if (card1 != card2) & (card1.isalpha()) & (card2.isdigit()): # First card is a figure
            if card1 == "A":
                if (int(card2) != 10):
                    your_hand = "A" + card2
                if (int(card2) == 10):
                    your_hand = "Blackjack"
            if (card1 == "J" or card1 == "Q" or card1 == "K"):
                your_hand = str(10 + int(card2))
        if (card1 != card2) & (card1.isdigit()) & (card2.isalpha()): # Second card is a figure
            if card2 == "A":
                if (int(card1) != 10):
                    your_hand = "A" + card1
                if (int(card1) == 10):
                    your_hand = "Blackjack"
            if (card2 == "J" or card2 == "Q" or card2 == "K"):
                your_hand = str(10 + int(card1))
        if (card1 != card2) & (card1.isalpha()) & (card2.isalpha()): # Both cards are figures
            if (card1 != "A") & (card2 != "A"):
                your_hand = str(20)
            else:
                your_hand = "Blackjack"

        if (d_card1 == "J" or d_card1 == "Q" or d_card1 == "K"):
            dealers_hand = str(10)
        else:
            dealers_hand = d_card1

        if (your_hand == "None"):
            raise ValueError ("Your hand is incorrect")
        if (dealers_hand == "None"):
            raise ValueError ("Dealer's hand is incorrect")

        return your_hand, dealers_hand

    def get_value(self, your_cards):
        """
        Receives a list of cards defining your hand and return the numerical value
        For instan
        :param your_cards:
        :return:
        """
        your_value = 0
        N_ace = 0
        for card in your_cards:
            if (card.isalpha()) & (card != "A"):
                your_value += 10
            if (card.isdigit()):
                your_value += int(card)
            if (card == "A"):
                your_value += 11
                N_ace += 1

        # If you are over 21, check if you have Aces
        # and downgrade them from 11 to 1 until you are under 21
        # or until all have been downgraded
        if (your_value > 21):
            for card in your_cards:
                if card == "A":
                    your_value -= 10
                    N_ace -= 1
                if your_value <= 21:
                    break

        if your_value == 0:
            raise Exception ("Failure to update value of your hand")

        return your_value

    def __call__(self, *args, **kwargs):
        # First round of cards
        your_cards, dealers_cards = self.deal_first_hand()
        # Check your hand
        your_hand, dealers_hand = self.check_your_first_two_cards(your_cards, dealers_cards)
        if your_hand == "Blackjack":
            # Directly check whether Dealer has Blackjack
            dealer, useless = self.check_your_first_two_cards(dealers_cards, dealers_cards)
            if dealer != "Blackjack":
                self.hand_outcome = "Win"
                print ("Player Wins by Blackjack")
                return self.hand_outcome
            if dealer == "Blackjack":
                print ("Dealer shows his hand", dealers_cards)
                print ("Both Player and Dealer have Blackjack")
                self.hand_outcome = "Push"
        else:
            first_decision = self.strategy(your_hand, dealers_hand)

        # Second round
        if first_decision == "Surrender":
            pass
            # FIX ME. Future implementation of Surrender

        if first_decision == "Split":
            pass
            # FIX ME. Future implementation of Split

        if first_decision == "Double":
            self.bet_placed *= 2
            print("Players draws a card")
            your_cards.append(self.cards.draw_a_card())
            print("Player's hand", your_cards)
            your_new_value = self.get_value(your_cards)
            if your_new_value <= 21:
                final_decision = "Stand"
            else:
                self.hand_outcome = "Lose"
                print("Player Loses. Over 21")
                return self.hand_outcome

        if first_decision == "Hit":
            final_decision = "Hit"
            while final_decision == "Hit":
                print ("Players draws a card")
                your_cards.append(self.cards.draw_a_card())
                print ("Player's hand", your_cards)
                your_new_value = self.get_value(your_cards)
                if your_new_value >= 21:
                    self.hand_outcome = "Lose"
                    print("Player Loses. Over 21")
                    return self.hand_outcome
                else:
                    final_decision = self.strategy(str(your_new_value), dealers_cards[0])

        if first_decision == "Stand":
            your_new_value = self.get_value(your_cards)
            final_decision = "Stand"

        # You stand. Dealer's turn to play
        if final_decision == "Stand":
            # Check if the dealer has Blackjack
            dealer, useless = self.check_your_first_two_cards(dealers_cards, dealers_cards)
            print ("Dealer shows his hand", dealers_cards)
            if dealer == "Blackjack":
                print("Player Loses. Dealer has Blackjack")
                self.hand_outcome = "Lose"
                return self.hand_outcome
            else: # Dealer hasn't got Blackjack, decides to play
                initial_value = self.get_value(dealers_cards)
                value = initial_value
                while value <= 17: # Dealer must play up to 17
                    dealers_cards.append(self.cards.draw_a_card())
                    print ("Dealer draws a card")
                    print ("Dealers hand", dealers_cards)
                    value = self.get_value(dealers_cards)
                    if (value > 21): # Dealer busted
                        print("Player Wins. Dealer busted")
                        self.hand_outcome = "Win"
                        return self.hand_outcome
                    if (17 <= value <= 21):
                        break
                if (17 <= value <= 21): # Dealer can decide whether to Stand
                    if (your_new_value == value):
                    # Dealer prefers to stand
                        print("Player and Dealer have the same hand. Push")
                        self.hand_outcome = "Push"
                        return self.hand_outcome
                    if (your_new_value < value <= 21):
                    # Dealer has better hand, decides to Stand
                        print("Player Loses. Dealer has better hand")
                        self.hand_outcome = "Lose"
                        return self.hand_outcome
                    while your_new_value >= value:
                        # Dealer keeps playing
                        print("Dealer draws a card")
                        dealers_cards.append(self.cards.draw_a_card())
                        print("Dealers hand", dealers_cards)
                        value = self.get_value(dealers_cards)
                        if (value > 21): # Dealer busted
                            print("Player Wins. Dealer busted")
                            self.hand_outcome = "Win"
                            return self.hand_outcome
                        if (your_new_value < value <= 21):
                            # Dealer has a better hand, decides to Stand
                            print("Player Loses. Dealer has better hand")
                            self.hand_outcome = "Lose"
                            return self.hand_outcome

        # Check for loopholes
        if self.hand_outcome == None:
            raise Exception ("Failure to decide Hand")

        return self.hand_outcome

class Game(object):
    def __init__(self, N_decks, initial_money, min_bet = 10, pay_ratio = 3./2.):
        self.N_decks = N_decks
        self.cards = Cards(N_decks)
        self.strategy = Strategy()
        self.money_pot = MoneyPot(starting_amount=initial_money, min_bet=min_bet)
        self.min_bet = min_bet
        self.pay_ratio = pay_ratio
        self.victory_counter = []
        self.money_counter = []



    def play_game(self):
        while self.min_bet >= self.money_pot.current_pot:
            bet = self.min_bet
            new_hand = Hand(self.cards, self.strategy, bet)
            if new_hand.hand_outcome == "Win":
                self.money_pot.current_pot += np.floor(self.pay_ratio * new_hand.bet_placed)
            if new_hand.hand_outcome == "Lose":
                pass
            if new_hand.hand_outcome == "Push":
                self.money_pot.current_pot += new_hand.bet_placed
            self.victory_counter.append(new_hand.hand_outcome)
            self.money_counter.append(self.money_pot.current_pot)

        print ("End of Game. Statistics:")
        self.get_statistics()
        plt.figure()
        plt.plot(self.money_counter)
        plt.xlabel("Hand #")
        plt.ylabel("Money Pot")
        plt.show()

    def get_statistics(self):
        won, lost, pushed = 0, 0, 0
        hands_played = len(self.victory_counter)
        print ("Total hands played: %d" %hands_played)
        for hand in self.victory_counter:
            if hand == "Win":
                won += 1
            if hand == "Lose":
                lost += 1
            else:
                pushed += 1
        print ("Won: %d" %won)
        print ("Lost: %d" %lost)
        print("Pushed: %d" %pushed)



class Cards(object):
    """
    Python object which takes care of the decks of cards
    It puts together a set of N decks and shuffles the set.
    Cards.draw_a_card() takes care of the dealing of cards
    """
    def __init__(self, N_decks):
        self.N_decks = N_decks
        self.decks = self.get_N_decks()
        self.shuffle_deck(self.decks)

    def one_deck(self):
        deck = []
        numbers = np.arange(2, 11)
        for digit in numbers:
            deck.append(str(digit))
        figures = ["J", "Q", "K", "A"]
        deck.extend(figures)
        one = np.array(deck)
        two = np.concatenate((one, one))
        four = np.concatenate((two, two))
        return four

    def get_N_decks(self):
        a_deck = self.one_deck()
        all_decks = np.tile(a_deck, self.N_decks)
        return all_decks

    def shuffle_deck(self, array):
        return random.shuffle(array)

    def draw_a_card(self):
        try:
            dummy_card = self.decks[0]
        except IndexError:  # You ran out of cards in the deck
            print("Replenishing the deck")
            self.decks = self.get_N_decks()
            self.shuffle_deck(self.decks)
            # FIX ME: when "CountingCards" allowed, update the number of decks remaining
        drawn_card = self.decks[0]
        self.decks = self.decks[1:]
        return drawn_card

class Strategy(object):
    """
    Python object which takes care of the Blackjack Strategy
    It contains a strategy chart which takes as input both the Player's and Dealer's hand
    and returns a decision like "Hit", "Stand", "Double", "Split"
    """
    def __init__(self, mode="Agressive"):
        self.mode = mode    #FIX ME. Adapt strategy for ambiguous cases depending on Agressiveness

    def strategy_chart(self, your_hand, dealers_hand):
        decision = "UNDECIDED"
        if (your_hand.isdigit()): # Standard Numbers
            decision = "Hit"
            if (dealers_hand.isalpha()):
                dealers_hand = str(10)
            if (int(your_hand) == 9) & (3 <= int(dealers_hand) <= 6):
                decision = "Double"
            if (int(your_hand) == 10) & (int(dealers_hand) <= 9):
                decision = "Double"
            if (int(your_hand) == 11):
                decision = "Double"
            if (int(your_hand) == 12) & (4 <= int(dealers_hand) <=6):
                decision = "Stand"
            if (13 <= int(your_hand) <= 16) & (int(dealers_hand) <= 6):
                decision = "Stand"
            if (17 <= int(your_hand) <= 20):
                decision = "Stand"

        if ((your_hand)[0] == "D"): # Pair of numbers
            decision = "Hit"
            if (your_hand == "D2" or your_hand == "D3") & (int(dealers_hand) <= 7):
                decision = "Split"
            if (your_hand == "D4") & (5 <= int(dealers_hand) <= 6):
                decision = "Split"
            if (your_hand == "D5") & (int(dealers_hand) <= 9):
                decision = "Double"
            if (your_hand == "D6") & (int(dealers_hand) <= 7):
                decision = "Split"
            if (your_hand == "D7") & (int(dealers_hand) <= 8):
                decision = "Split"
            if (your_hand == "D8"):
                decision = "Split"
            if (your_hand == "D9"):
                if (int(dealers_hand) <= 9) & (int(dealers_hand) != 7):
                    decision = "Split"
                else:
                    decision = "Stand"
            if (your_hand == "D10"):
                decision = "Stand"
            if (your_hand == "DA"):
                decision = "Split"

        if (your_hand[0] == "A"):  # Soft (Ace + Card)
            decision = "Hit"
            if (your_hand == "A2" or your_hand == "A3") & (5 <= int(dealers_hand) <= 6):
                decision = "Double"
            if (your_hand == "A4" or your_hand == "A5") & (4 <= int(dealers_hand) <= 6):
                decision = "Double"
            if (your_hand == "A6") & (3 <= int(dealers_hand) <= 6):
                decision = "Double"
            if (your_hand == "A7"):
                if (int(dealers_hand) == 2 or int(dealers_hand) == 7 or int(dealers_hand) == 8):
                    decision = "Stand"
                if (3 <= int(dealers_hand) <= 6):
                    decision = "Double"
            if (your_hand == "A8"):
                decision = "Stand"
            if (your_hand == "A9"):
                decision = "Stand"

        if (your_hand == "Blackjack"):
            decision = "Stay"

        return decision

    def __call__(self, your_hand, dealers_hand):
        hand_decision = self.strategy_chart(your_hand, dealers_hand)
        print ("Calling Strategy")
        print ("Dealers hand:", dealers_hand)
        print ("Players hand:", your_hand)
        print ("Players decides to:", hand_decision)
        return hand_decision

