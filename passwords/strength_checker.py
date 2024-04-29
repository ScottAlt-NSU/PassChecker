import re
import os


def check_password_strength(password):
    """Provide feedback on password weaknesses but allow any password."""
    messages = []
    if len(password) < 8:
        messages.append("Password should be at least 8 characters long.")
    if not re.search("[a-z]", password):
        messages.append("Password should include at least one lowercase letter.")
    if not re.search("[A-Z]", password):
        messages.append("Password should include at least one uppercase letter.")
    if not re.search("[0-9]", password):
        messages.append("Password should include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}\[\]|<>\\]", password):
        messages.append("Password should include at least one special character.")

    if messages:
        return False, "Consider improving your password: " + "  ".join(messages)
    return True, "Password is strong."


def load_common_passwords(file_path=None):
    if file_path is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'common_passwords.txt')
    try:
        with open(file_path, 'r') as file:
            common_passwords = set(line.strip() for line in file)
        return common_passwords
    except FileNotFoundError:
        print(f"Warning: Could not find the file {file_path}. Common password check will not be performed.")
        return set()


def check_common_passwords(password, common_passwords):
    """Warn if the password is common but still allow testing it."""
    if password in common_passwords:
        return False, "Warning: Password is commonly used and may be easily guessed."
    return True, "Password is not common."


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python strength_checker.py <password>")
        sys.exit(1)

    input_password = sys.argv[1]
    common_passwords = load_common_passwords()

    strength_ok, strength_message = check_password_strength(input_password)
    common_ok, common_message = check_common_passwords(input_password, common_passwords)

    if not common_ok:
        print(common_message)  # Prioritize common password warning if applicable
    elif not strength_ok:
        print(strength_message)  # Show strength improvements needed if not a common password
    else:
        print("Your password is strong and not common.")  # Show positive message if all checks are passed
