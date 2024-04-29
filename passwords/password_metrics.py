import math


def calculate_entropy(password):
    """Calculate the entropy of a given password based on character variety and length."""
    charset_size = len(set(password))  # Simplified charset size estimate for demonstration
    entropy = len(password) * math.log2(charset_size)
    return entropy


def time_to_crack(entropy):
    """Estimate time to crack based on entropy, assuming average attack scenarios."""
    # Average guesses per second might be around 1 billion (1e9) for a high-end consumer GPU setup
    guesses_per_second = 1e9  # More realistic for consumer hardware
    seconds = (2 ** entropy) / guesses_per_second
    return seconds


def format_time(seconds):
    """Convert seconds to a more readable format, like days, hours, minutes."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{(seconds / 60):.2f} minutes"
    elif seconds < 86400:
        return f"{(seconds / 3600):.2f} hours"
    else:
        return f"{(seconds / 86400):.2f} days"


def calculate_strength_percentile(entropy, distribution):
    """Calculate the percentile of the password's strength based on entropy."""
    if not distribution:
        return 0  # Return 0 if distribution is empty to avoid division by zero
    sorted_distribution = sorted(distribution)
    # Finding the first index where entropy is less than the value in sorted_distribution
    position = next((i for i, e in enumerate(sorted_distribution) if entropy < e), len(sorted_distribution))
    percentile = (position / len(sorted_distribution)) * 100
    return percentile


def calculate_percentile(position, total_items):
    if total_items == 0:
        return 0  # Avoid division by zero if the distribution is unexpectedly empty
    percentile = (position / total_items) * 100
    return percentile
