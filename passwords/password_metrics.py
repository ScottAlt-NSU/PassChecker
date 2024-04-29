import math
import re

import math


def load_dictionary(file_path='/Users/scott/Documents/Development/Github/PassChecker/passwords/dictionary.txt'):
    """
    Load a dictionary file with one word per line.
    """
    try:
        with open(file_path, 'r') as file:
            return set(word.strip().lower() for word in file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return set()


import math
import re


def calculate_entropy(password, dictionary):
    """Calculate refined entropy considering dictionary words and character diversity, with debugging."""
    if not password:
        return 0

    charset_size = sum([
        26 if re.search(r'[a-z]', password) else 0,
        26 if re.search(r'[A-Z]', password) else 0,
        10 if re.search(r'[0-9]', password) else 0,
        32 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0
    ])

    basic_entropy = math.log2(max(1, charset_size)) * len(password)
    print(f"Initial Entropy: {basic_entropy}")  # Debugging initial entropy

    # To handle overlapping and multiple reductions, track all possible word contributions
    word_contributions = []
    for word in dictionary:
        if word in password.lower():
            word_len = len(word)
            coverage = word_len / len(password)
            reduction = coverage * basic_entropy * 0.5  # Proportional reduction
            word_contributions.append((word, reduction))
            print(f"Identified '{word}' in password, proposing reduction: {reduction}")  # Debugging word reduction

    # Apply the maximum reduction from identified words
    if word_contributions:
        max_reduction = max(word_contributions, key=lambda x: x[1])[1]
        print(f"Applying maximum reduction: {max_reduction}")  # Debugging max reduction
        basic_entropy -= max_reduction

    adjusted_entropy = max(1, basic_entropy)  # Ensure a minimal entropy
    print(f"Adjusted Entropy: {adjusted_entropy}")  # Debugging adjusted entropy
    return adjusted_entropy


def time_to_crack(entropy):
    guesses_per_second = 1e13
    seconds = max(1, (2 ** entropy) / guesses_per_second)
    print(f"Entropy: {entropy}, Seconds: {seconds}")  # Debugging
    return seconds


def format_time(seconds):
    """Convert seconds to a human-readable format."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{(seconds / 60):.2f} minutes"
    elif seconds < 86400:
        return f"{(seconds / 3600):.2f} hours"
    elif seconds < 31536000:  # Up to a year
        return f"{(seconds / 86400):.2f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"


def calculate_strength_percentile(entropy, distribution):
    if not distribution:
        print("Empty distribution")  # Debugging
        return 0
    sorted_distribution = sorted(distribution)
    position = next((i for i, e in enumerate(sorted_distribution) if e > entropy), len(sorted_distribution))
    percentile = (position / len(sorted_distribution)) * 100
    print(f"Entropy: {entropy}, Position: {position}, Percentile: {percentile}%")  # Debugging
    return percentile


def calculate_percentile(position, total_items):
    """Calculate percentile based on position in a sorted list."""
    if total_items == 0:
        return 0  # Avoid division by zero if the distribution is unexpectedly empty
    percentile = (position / total_items) * 100
    return percentile
