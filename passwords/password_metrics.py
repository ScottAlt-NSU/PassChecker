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


def calculate_entropy(password, dictionary):
    """Calculate refined entropy considering dictionary words and character diversity, with debugging."""
    if not password:
        return 0

    # Calculate charset size based on character diversity in the password
    charset_size = sum([
        26 if re.search(r'[a-z]', password) else 0,
        26 if re.search(r'[A-Z]', password) else 0,
        10 if re.search(r'[0-9]', password) else 0,
        32 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0
    ])

    # Initial entropy calculation based on charset size and password length
    basic_entropy = math.log2(max(1, charset_size)) * len(password)
    print(f"Initial Entropy: {basic_entropy:.2f}")  # Debugging initial entropy

    # Track all valid reductions due to dictionary words
    word_contributions = []
    for word in dictionary:
        start_index = 0
        while True:
            start_index = password.lower().find(word, start_index)
            if start_index == -1:
                break  # No more occurrences of the word
            end_index = start_index + len(word)

            # Calculate the potential reduction based on the word's coverage
            coverage = len(word) / len(password)
            reduction = coverage * basic_entropy * 0.5  # Proportional reduction
            word_contributions.append((word, start_index, end_index, reduction))

            print(
                f"Identified '{word}' at positions {start_index}-{end_index}, proposing reduction: {reduction:.2f}")  # Debugging word reduction

            start_index += 1  # Move start index forward to continue searching

    # Apply the maximum reduction for non-overlapping words sorted by their impact
    if word_contributions:
        # Sort contributions by start position and length (prioritize longer and earlier found words)
        word_contributions.sort(key=lambda x: (x[1], -x[2] + x[1]))
        applied_reductions = []

        # Apply reductions making sure not to double-count overlapping regions
        last_end = -1
        for word, start, end, reduction in word_contributions:
            if start >= last_end:  # Ensure no overlap with previously applied reduction
                applied_reductions.append(reduction)
                last_end = end  # Update last applied word end position
                print(f"Applying reduction for '{word}': {reduction:.2f}")  # Debugging applied reductions

        total_reduction = sum(applied_reductions)
        print(f"Total reductions applied: {total_reduction:.2f}")  # Debugging total reductions
        basic_entropy -= total_reduction

    adjusted_entropy = max(1, basic_entropy)  # Ensure a minimal entropy
    print(f"Adjusted Entropy: {adjusted_entropy:.2f}")  # Debugging adjusted entropy
    return adjusted_entropy


def time_to_crack(entropy):
    guesses_per_second = 1e11
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


def categorize_password_entropy(entropy):
    """Categorize the password based on its entropy value into weak, medium, or strong."""
    if entropy < 30:
        return "weak", "Your password is weak and could be easily guessed by attackers."
    elif 30 <= entropy < 60:
        return "medium", "Your password is medium strength, suitable for general use."
    else:
        return "strong", "Your password is strong and well-suited for securing sensitive data."


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
