from flask import Flask, render_template, request

from passwords import strength_checker
from passwords.strength_checker import check_password_strength, load_common_passwords, check_common_passwords
from passwords import password_metrics

app = Flask(__name__)

# Load the entropy distribution at the start
entropy_distribution = []


def load_entropy_distribution():
    try:
        with open('/Users/scott/Documents/Development/Github/PassChecker/passwords/entropy_distribution.txt', 'r') as file:
            global entropy_distribution
            entropy_distribution = [float(line.strip()) for line in file]
    except FileNotFoundError:
        print("Entropy distribution file not found. Please generate it first.")


load_entropy_distribution()  # Call this function on startup


def calculate_strength_percentile(entropy, distribution):
    sorted_distribution = sorted(distribution)
    position = next((i for i, e in enumerate(sorted_distribution) if e > entropy), len(sorted_distribution))
    return position


def calculate_percentile(position, total_items):
    if total_items == 0:
        return 0.0  # Avoid division by zero and ensure return type is float
    return (position / total_items) * 100


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    time_estimate = ''
    percentile = 0.0  # Initialize percentile as a float
    if request.method == 'POST':
        password = request.form['password']
        common_passwords = strength_checker.load_common_passwords()
        strength_ok, strength_message = strength_checker.check_password_strength(password)
        common_ok, common_message = strength_checker.check_common_passwords(password, common_passwords)

        entropy = password_metrics.calculate_entropy(password)
        seconds = password_metrics.time_to_crack(entropy)
        time_estimate = password_metrics.format_time(seconds)

        # Use the loaded entropy distribution
        if entropy_distribution:
            position = calculate_strength_percentile(entropy, entropy_distribution)
            percentile = calculate_percentile(position, len(entropy_distribution))
        else:
            message = "Entropy distribution not available."

        if not strength_ok or not common_ok:
            message = strength_message if not strength_ok else common_message
        else:
            message += f" Your password is strong and uncommon. It would take approximately {time_estimate} to crack. It is stronger than {percentile:.2f}% of common passwords."

    return render_template('index.html', message=message, time_estimate=time_estimate, percentile=f"{percentile:.2f}%")


if __name__ == '__main__':
    app.run(debug=True)
