import numpy as np
import blackjack as bj


if __name__ == "__main__":

    st = bj.Strategy()
    mp = bj.MoneyPot(starting_amount=1000, min_bet=10)
    cd = bj.Cards(N_decks=5)

    hand0 = bj.Hand(cards=cd, strategy=st, bet_placed=10)
    hand0()

