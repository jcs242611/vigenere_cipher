from collections import defaultdict
import re

def index_of_coincidence(text):
    text = re.sub(r'[^A-Z]', '', text.upper())
    freq = defaultdict(int)
    length = len(text)
    
    for char in text:
        freq[char] += 1
    
    ic = sum(count * (count - 1) for count in freq.values()) / (length * (length - 1))
    return ic

def segment_text(ct, key_length):
    segments = ['' for _ in range(key_length)]
    for i, char in enumerate(ct):
        segments[i % key_length] += char
    return segments

def calculate_ic_for_lengths(ct, key_lengths):
    ic_values = {}
    for key_length in key_lengths:
        segments = segment_text(ct, key_length)
        ic_sum = sum(index_of_coincidence(segment) for segment in segments)
        avg_ic = ic_sum / key_length
        ic_values[key_length] = avg_ic
    return ic_values

ct = "Pspqmtorccw gc wgwtji jpoigxk mevqoptow dbsk geldmlq xm zylswf."
key_lengths = {3}  # replace with actual from Kasiski
ic_values = calculate_ic_for_lengths(ct, key_lengths)
print("Index of Coincidence Values:", ic_values)
