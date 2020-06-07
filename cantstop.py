# Compute the odds for the Can't stop game

import numpy

open = [True for _ in range(13)]
goin = [False for _ in range(13)]

# Probabilities of being able to progress in a lane, or any of two lanes, or any of three lanes
prob1 = [0 for _ in range(13)]
prob2 = [[0 for _ in range(13)] for _ in range(13)]
prob3 = [[[0 for _ in range(13)] for _ in range(13)] for _ in range(13)]

dice = range(1, 7)
cols = range(2, 13)

rolls = 0

# Generate possible rolls
for d1 in dice:
    for d2 in dice:
        for d3 in dice:
            for d4 in dice:
                rolls += 1
                # Possible bins:
                targets = [d1 + d2, d1 + d3, d1 + d4, d2 + d3, d2 + d4, d3 + d4]
                # Possible combos
                for i in set(targets):
                    prob1[i] += 1

                # Combos of 2
                for i in cols:
                    for j in range(i + 1, 13):
                        if i in targets or j in targets:
                            prob2[i][j] += 1
                            prob2[j][i] += 1

                # Combos of 3
                for i in cols:
                    for j in range(i + 1, 13):
                        for k in range (j + 1, 13):
                            if i in targets or j in targets or k in targets:
                                prob3[i][j][k] += 1
                                prob3[i][k][j] += 1
                                prob3[j][i][k] += 1
                                prob3[j][k][i] += 1
                                prob3[k][i][j] += 1
                                prob3[k][j][i] += 1

# Compute probabilities
for i in range(13):
    prob1[i] /= rolls
    print("{:2}: {:5.2%}".format(i, prob1[i]))

for i in range(2, 13):
    for j in range(2, 13):
        prob2[i][j] /= rolls
        if i < j:
            print("{:2} {:2}: {:5.2%}".format(i, j, prob2[i][j]))

for i in range(2, 13):
    for j in range(2, 13):
        for k in range(2, 13):
            prob3[i][j][k] /= rolls
            if i < j < k:
                print("{:2} {:2} {:2}: {:5.2%}".format(i, j, k, prob3[i][j][k]))

def prob_of_going(status, i):
    lanes = sum(status)
    if lanes in [0, 1]:
        return prob1[i]
    elif lanes == 2:
        j = [x for x in cols if x != i and status[x]][0]
        return prob2[i][j]
    elif lanes == 3:
        others = [x for x in cols if x != i and status[x]]
        j = others[0]
        k = others[1]
        return prob3[i][j][k]
    else:
        return 0

def prob2_of_going(status, i):
    for j in cols:
        if j != i and status[j]:
            return prob2[i][j]
    return 0


def read_col(text):
    if text in "abc":
        return int(text, 16)
    else:
        return int(text)


while True:
    # Print status
    # Columns
    print("\nBoard state:\n" + " ".join(["{:^6}".format(i) if open[i] else 'XXXXXX' for i in cols]))
    # Selection
    print(" ".join(["[====]" if goin[i] else "------" for i in cols]))
    # Prob of individual column (if not going) or of any of going
    for in_a_row in range(1, 13):
        if any(goin):
            stakes = prob_of_going(goin, [x for x in cols if goin[x]][0])
            print(" ".join("{:6.2%}".format(1 - stakes ** in_a_row if not goin[i] else stakes ** in_a_row) for i in cols))
        else:
            print(" ".join("{:6.2%}".format(prob1[i] ** in_a_row) for i in cols))

    action = input("\nX exits, X[num] toggles column open, [num] toggles advance>> ").lower()

    # Process command
    if action == "":
        continue
    elif action == "x":
        break
    elif action[0] == 'x':
        col = read_col(action[1:])
        open[col] ^= True
    elif action[-1] == 'x':
        col = read_col(action[:-1])
        open[col] ^= True
    else:
        goin[read_col(action)] ^= True
