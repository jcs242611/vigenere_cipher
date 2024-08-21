from collections import Counter

def frequency_analysis(segment):
    freq = Counter(segment)
    total = sum(freq.values())
    return {char: count / total for char, count in freq.items()}

def find_best_shift(segment):
    english_freq = {'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.070, 'N': 0.067, 'S': 0.063, 'H': 0.061, 'R': 0.060, 'D': 0.043, 'L': 0.040, 'U': 0.028, 'M': 0.025, 'W': 0.024, 'F': 0.022, 'G': 0.020, 'Y': 0.020, 'P': 0.019, 'B': 0.014, 'V': 0.010, 'K': 0.008, 'X': 0.001, 'J': 0.001, 'Q': 0.001, 'Z': 0.001}
    segment_freq = frequency_analysis(segment)
    
    best_shift = 0
    min_diff = float('inf')
    
    for shift in range(26):
        shifted_freq = {chr((ord(char) - ord('A') - shift) % 26 + ord('A')): freq for char, freq in segment_freq.items()}
        diff = sum(abs(english_freq.get(char, 0) - shifted_freq.get(char, 0)) for char in set(english_freq) | set(shifted_freq))
        
        if diff < min_diff:
            min_diff = diff
            best_shift = shift
    
    return best_shift

def segment_text(ciphertext, key_length):
    # Normalize the text by removing non-alphabetic characters and converting to uppercase
    normalized_text = ''.join(filter(str.isalpha, ciphertext)).upper()
    
    # Split the normalized text into segments of the given key length
    segments = ['' for _ in range(key_length)]
    for i, char in enumerate(normalized_text):
        segments[i % key_length] += char
    
    return segments

def find_key(ciphertext, key_lengths):
    best_key = ""
    for key_length in key_lengths:
        segments = segment_text(ciphertext, key_length)
        key = ""
        for segment in segments:
            best_shift = find_best_shift(segment)
            key += chr(best_shift + ord('A'))
        best_key = key
        print(f"Key Length: {key_length}, Key: {best_key}")
    return best_key

ct = "Pspqmtorccw gc wgwtji jpoigxk mevqoptow dbsk geldmlq xm zylswf."
key_lengths = {3}  # Example key lengths; replace with actual from Step 2
key = find_key(ct, key_lengths)
print("Determined Key:", key)
