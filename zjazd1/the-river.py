# Braian Kreft s16723
# https://www.codingame.com/ide/puzzle/the-river-i-
# The River I
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r_1 = int(input())
r_2 = int(input())

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
def nextRiverNumber(r):
    nextR = r
    while r > 0:
        nextR += r % 10
        r -= r % 10
        r //= 10
    
    return nextR

while r_1 != r_2:
    if r_1 < r_2:
        r_1 = nextRiverNumber(r_1)        
    else:
        r_2 = nextRiverNumber(r_2)
print(r_1)
