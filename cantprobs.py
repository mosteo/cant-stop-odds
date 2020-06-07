# Generate probabilities by brute force, to compare against computed ones

from random import randint

prob1 = [0 for _ in range(13)]
prob2 = [[0 for _ in range(13)] for _ in range(13)]
rolls = 1000000

for _ in range(rolls):
    d1 = randint(1, 6)
    d2 = randint(1, 6)
    d3 = randint(1, 6)
    d4 = randint(1, 6)

    combos = {d1 + d2, d1 + d3, d1 + d4, d2 + d3, d2 + d4, d3 + d4}

    for i in combos:
        prob1[i] += 1
        for j in range(2, 13):
            prob2[i][j] += 1
            prob2[j][i] += 1

for i in range(13):
    prob1[i] /= rolls
    print("{:2}: {:5.2%}".format(i, prob1[i]))

for i in range(2, 13):
    for j in range(2, 13):
        prob2[i][j] /= rolls
        if i < j:
            print("{:2} {:2}: {:5.2%}".format(i, j, prob2[i][j]))
