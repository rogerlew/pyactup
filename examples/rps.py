# Rock, paper, scissors example using pyactup
import sys

sys.path.insert(0, '../')

import pyactup
import random

import numpy as np


DEFAULT_ROUNDS = 100
MOVES = ["paper", "rock", "scissors"]
N_MOVES = len(MOVES)

m = pyactup.Memory(noise=0.1, optimized_learning=False, stress=None)
m2 = pyactup.Memory(noise=0.1, optimized_learning=False, stress=0.1)


def defeat_expectation(m, **kwargs):
    # Generate expectation matching supplied conditions and play the move that defeats.
    # If no expectation can be generate, chooses a move randomly.
    expectation = (m.retrieve(**kwargs) or {}).get("move")
    if expectation:
        return MOVES[(MOVES.index(expectation) - 1) % N_MOVES]
    else:
        return random.choice(MOVES)


def safe_element(list, i):
    try:
        return list[i]
    except IndexError:
        return None


def main(sets=100, rounds=1000):
    # Plays multiple rounds of r/p/s of a lag 1 player (player1) versus a
    # lag 2 player (player2).
    scores = []
    for s in range(sets):
        plays1 = []
        plays2 = []
        score = 0
        for r in range(rounds):
            move1 = defeat_expectation(m, player="player2",
                                       ultimate=safe_element(plays2, -1))
            move2 = defeat_expectation(m2, player="player1",
                                       ultimate=safe_element(plays1, -1),
                                       penultimate=safe_element(plays1, -2))
            winner = (MOVES.index(move2) - MOVES.index(move1) + N_MOVES) % N_MOVES
            score += -1 if winner == 2 else winner
#            print("Round {:3d}\tPlayer 1: {:8s}\tPlayer 2: {:8s}\tWinner: {}\tScore: {:4d}".format(
#                r, move1, move2, winner, score))
            m.learn(player="player1",
                    ultimate=safe_element(plays1, -1),
                    penultimate=safe_element(plays1, -2),
                    move=move1)
            m2.learn(player="player2", ultimate=safe_element(plays2, -1), move=move2)
            plays1.append(move1)
            plays2.append(move2)
#            if r % 100 == 0:
#                print(m)
            m.advance()
            m2.advance()

        scores.append(score)

        print(np.mean(scores), np.std(scores))
    print(scores)

if __name__ == '__main__':
    from time import time
    t0 = time()
    main()
    print(time() - t0)

# np Chunk._references 3.382678270339966 s

# m=None, m2=None
# -3.45 26.067364653911604
# [-20, 7, -17, -12, -10, 2, 46, 54, 4, 29, -7, -14, -37, -18, 42, -20, -9, -16, -50, 12, 4, 9, 1, -48, -36, -2, -11, -68, 19, 34, 37, -18, -29, 20, 11, 22, 7, -40, -22, -24, 1, 16, -1, -25, -50, 3, 32, -48, -30, 30, -33, -36, 34, -36, 24, 35, 2, 10, -14, -40, -15, -38, 42, 24, 4, 30, 59, 2, -24, 1, -17, -12, 5, 11, -15, 1, 52, 13, -11, 14, 3, 17, -27, -4, -2, -9, -40, -10, 10, -14, 8, -26, -2, -31, -34, 6, 34, -31, 3, -28]

# m=None, m2=5 100,000 rounds score 173

