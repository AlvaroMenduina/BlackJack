import numpy as np
import matplotlib.pyplot as plt
import blackjack as bj


if __name__ == "__main__":

    st = bj.Strategy()
    mp = bj.MoneyPot(starting_amount=1000, min_bet=10)
    cd = bj.Cards(N_decks=5)

    # hand0 = bj.Hand(cards=cd, strategy=st, money_pot=mp, bet_placed=10)
    # hand0()

    N_games = 10000
    games = np.arange(N_games)
    lengths = np.zeros(N_games)
    plt.figure()
    for k in range(N_games):
        game = bj.Game(N_decks=5, initial_money=1000, min_bet=10, pay_ratio=3./2.)
        result, won, lost, pushed = game()
        lengths[k] = len(result)
        plt.plot(result, label="Game %d" %(k+1))

    plt.xlabel("Number of Hands played")
    plt.ylabel("Money Pot")
    if N_games <= 10:
        plt.legend()

    plt.figure()
    plt.scatter(games, lengths)
    plt.xlabel('Game #')
    plt.ylabel('Hands played')


    plt.figure()
    plt.hist(lengths, bins='auto')
    plt.show()


