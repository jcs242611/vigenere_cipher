from collections import defaultdict
import re
from math import gcd
from functools import reduce

def find_repeated_sequences(ct, min_length=3):
    sequences = defaultdict(list)
    for i in range(len(ct) - min_length + 1):
        seq = ct[i:i + min_length]
        sequences[seq].append(i)
    
    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for i in range(1, len(positions)):
                distances.append(positions[i] - positions[i - 1])
    
    return distances

def find_key_lengths(distances):
    def find_gcd(numbers):
        return reduce(gcd, numbers)

    possible_lengths = set()
    if distances:
        length_gcd = find_gcd(distances)
        for i in range(1, length_gcd + 1):
            if length_gcd % i == 0:
                possible_lengths.add(i)
    return possible_lengths

ct = "Pspqmtorccw gc wgwtji jpoigxk mevqoptow dbsk geldmlq xm zylswf."
ct = ct.replace(" ", "")
distances = find_repeated_sequences(ct)
key_lengths = find_key_lengths(distances)
key_lengths.discard(1)
print("Possible Key Lengths:", key_lengths)
