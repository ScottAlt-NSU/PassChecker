import os

from passwords import password_metrics


def load_passwords(filename='/Users/scott/Documents/Development/Github/PassChecker/passwords/common_passwords.txt'):
    """ Load passwords from a file. Each password should be on a new line. """
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def calculate_entropies(passwords):
    """ Calculate the entropy for each password. """
    return [password_metrics.calculate_entropy(p) for p in passwords]


def save_entropies(entropies, output_filename='entropy_distribution.txt'):
    """ Save calculated entropies to a file. """
    with open(output_filename, 'w') as file:
        for entropy in entropies:
            file.write(f"{entropy}\n")


def main():
    passwords = load_passwords()  # Load passwords from a file
    entropies = calculate_entropies(passwords)  # Calculate entropies
    save_entropies(entropies)  # Save entropies to a file


if __name__ == '__main__':
    main()
