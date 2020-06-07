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

rolls = 6 ** 4

# Generate possible rolls
for d1 in dice:
    for d2 in dice:
        for d3 in dice:
            for d4 in dice:
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
                        for k in range(j + 1, 13):
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


def pcompute(check_fun):
    # Test each target set with check_fun and return probability
    hits = 0
    for d1 in dice:
        for d2 in dice:
            for d3 in dice:
                for d4 in dice:
                    targets = {d1 + d2, d1 + d3, d1 + d4, d2 + d3, d2 + d4, d3 + d4}
                    if check_fun(targets):
                        hits += 1
    return hits / 6**4


def check_ok(targets):
    # Check if this combo is good
    return any([(open[t] and goin[t]) or (open[t] and sum(goin) < 3) for t in targets])


def read_col(text):
    if text in "abc":
        return int(text, 16)
    else:
        return int(text)

roll = 1

while True:
    # Print status

    # Prob of individual column (if not going) or of any of going
    closed = [not x for x in open]
    cell = "{:6.2%} "
    bad_idea = False
    E = 1 / (1 - min(pcompute(check_ok), 0.9999))  # expectancy of required rolls to land a miss

    # Columns
    print("\nBoard state:")
    print(" ".join(["{:^6}".format(i) if open[i] else 'XXXXXX' for i in cols]))
    # Selection
    print(" ".join(["[====]" if goin[i] else "------" for i in cols]))

    for streak in range(1, 14):
        line = ""
        p_good = min(pcompute(check_ok) ** streak, 0.9999) # for display of 100%
        p_fail = min(1 - p_good, 0.9999)

        if p_good < p_fail and not bad_idea:
            bad_idea = True
            print("------ " * 11 + " " + str(streak - 1))

        if streak == numpy.ceil(E):
            print("====== " * 11 + " " + "{:.2f}".format(E))

        for i in cols:
            if closed[i]:
                line += cell.format(p_fail)
            elif not goin[i] and sum(goin) >= 3:
                line += cell.format(p_fail)
            elif not goin[i] and sum(goin) + sum(closed) == 0: # Nothing played yet, show initial prob per lane
                line += cell.format(prob1[i] ** streak)
            elif not goin[i]: # but we still have lanes to choose
                line += cell.format(p_good)
            elif goin[i] and sum(goin) < 3:
                line += cell.format(p_good)
            else:  # goin[i] and sum(goin) >= 3, that is: we must hit one of those 3 in use
                line += cell.format(p_good)
        print(line + (" <--" if streak == roll else ""))

    action = input("\nX exits, X[num] toggles column open, [num] toggles advance, [ENTER] counts roll, OTHER resets"
                   "\n>> ").lower()

    # Process command
    if action == "":
        roll += 1
        continue
    elif action == "x":
        break
    elif action[0] == 'x':
        col = read_col(action[1:])
        open[col] ^= True
    elif action[-1] == 'x':
        col = read_col(action[:-1])
        open[col] ^= True
    elif action in "0123456789abc" or action in ["10", "11", "12"]:
        roll = 1
        goin[read_col(action)] ^= True
    else:
        goin = [False for _ in range(13)]
        roll = 1
