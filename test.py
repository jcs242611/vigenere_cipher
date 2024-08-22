from collections import defaultdict, Counter
import re
from math import gcd
from functools import reduce
from itertools import product

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

def find_key_lengths(distances, max_length=5):
    def find_gcd(numbers):
        return reduce(gcd, numbers)

    possible_lengths = set()
    if distances:
        length_gcd = find_gcd(distances)
        for i in range(1, length_gcd + 1):
            if length_gcd % i == 0 and i <= max_length:
                possible_lengths.add(i)
    return possible_lengths

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

def frequency_analysis(segment):
    freq = Counter(segment)
    total = sum(freq.values())
    return {char: count / total for char, count in freq.items()}

def find_best_shifts(segment):
    english_freq = {'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.070, 'N': 0.067, 'S': 0.063, 'H': 0.061, 'R': 0.060, 'D': 0.043, 'L': 0.040, 'U': 0.028, 'M': 0.025, 'W': 0.024, 'F': 0.022, 'G': 0.020, 'Y': 0.020, 'P': 0.019, 'B': 0.014, 'V': 0.010, 'K': 0.008, 'X': 0.001, 'J': 0.001, 'Q': 0.001, 'Z': 0.001}
    segment_freq = frequency_analysis(segment)
    
    best_shifts = []
    
    for shift in range(26):
        shifted_freq = {chr((ord(char) - ord('A') - shift) % 26 + ord('A')): freq for char, freq in segment_freq.items()}
        diff = sum(abs(english_freq.get(char, 0) - shifted_freq.get(char, 0)) for char in set(english_freq) | set(shifted_freq))
        
        best_shifts.append((shift, diff))
    
    best_shifts.sort(key=lambda x: x[1])
    return best_shifts

def decrypt_vigenere(ciphertext, key):
    plaintext = []
    key = key.upper()
    key_length = len(key)
    
    # Remove non-alphabetic characters for decryption
    ciphertext = re.sub(r'[^A-Z]', '', ciphertext.upper())
    
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_index = (key_index + 1) % key_length
        else:
            plaintext.append(char)
    
    return ''.join(plaintext)

def find_key(ciphertext, key_lengths):
    all_keys = {}
    
    for key_length in key_lengths:
        segments = segment_text(ciphertext, key_length)
        key_options = []
        
        for segment in segments:
            best_shifts = find_best_shifts(segment)
            best_key_shifts = [chr(shift + ord('A')) for shift, _ in best_shifts[:5]]  # Get top 5 shifts
            key_options.append(best_key_shifts)
        
        # Generate all possible keys from top shifts
        possible_keys = [''.join(key) for key in product(*key_options)]
        possible_keys = possible_keys[:5]  # Limit to top 5 keys
        
        all_keys[key_length] = possible_keys
        
    return all_keys

def decrypt_vigenere_cipher(ct):
    ct = re.sub(r'[^A-Z]', '', ct.upper())
    
    # Step 1: Find repeated sequences and distances
    distances = find_repeated_sequences(ct)
    
    # Step 2: Find possible key lengths with a maximum length constraint
    key_lengths = find_key_lengths(distances)
    key_lengths.discard(1)  # Remove 1 as it's not a valid key length
    
    if not key_lengths:
        key_lengths = set(range(2, 6))  # Default key lengths if no distances found
    
    print("Possible Key Lengths:", key_lengths)
    
    # Step 3: Calculate Index of Coincidence for possible key lengths
    ic_values = calculate_ic_for_lengths(ct, key_lengths)
    print("Index of Coincidence Values:")
    for length, ic in ic_values.items():
        print(f"Key Length: {length}, Average IC: {ic:.4f}")
    
    # Step 4: Find the top possible keys using frequency analysis
    all_keys = find_key(ct, key_lengths)
    
    # Step 5: Decrypt using possible keys and calculate IC for decrypted text
    results = []
    print("\nDecryption and IC Calculation:")
    for key_length, keys in all_keys.items():
        for key in keys:
            decrypted_text = decrypt_vigenere(ct, key)
            ic = index_of_coincidence(decrypted_text)
            results.append((key, decrypted_text, ic))
    
    # Sort results by IC value in descending order
    results.sort(key=lambda x: x[2], reverse=True)
    
    # Print the best result
    best_key, best_text, best_ic = results[0]
    print("\nMost Likely Key:")
    print(f"Key: {best_key}")
    print(f"Decrypted Text: {best_text}")
    print(f"IC of Decrypted Text: {best_ic:.4f}")
    
    # Print other top possibilities
    print("\nOther Top Possibilities:")
    for key, text, ic in results[1:]:
        print(f"Key: {key}")
        print(f"Decrypted Text: {text}")
        print(f"IC of Decrypted Text: {ic:.4f}")

# Example usage
ciphertext = "T omvwmz ifmdkxa rvhu figlurz bti hcfik eavel; rskouzxvqwl myikoqw yzaq mmzhbvs snz urgmd ahzxh."
# ciphertext = "Fvck me o msqbzy hpmwhlijh nzef kcdp ns yfgdmjlip jcs zuuhwvq qchlqf. nzme wm tiuba mwqr ng gdsuli eoghpq hykx oomww fc wzioy nzi hofahuhs gj fvy usps. nzi wss xsd hbaw iwfd fq aimwq.Hbaw ug u keydfw txocfxqln llmh qapx py wrofshxqr pae hwafids wattsl. llug ck fqwhy yesx ls ofysxq guetxs nwwf qukie hi ulqqe llq judmpwnq sr hbw gary. llq yyq jaf nzme kcdp ns ggyes."
# ciphertext = "Pspqmtorccw gc wgwtji jpoigxk mevqoptow dbsk geldmlq xm zylswf."
decrypt_vigenere_cipher(ciphertext)
