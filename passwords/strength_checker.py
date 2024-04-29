import re

def check_password_strength(password):
    """Check the strength of a password."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search("[a-z]", password):
        return False, "Password must include at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return False, "Password must include at least one uppercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must include at least one number."
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must include at least one special character."
    return True, "Password is strong."

def load_common_passwords(file_path='common_passwords.txt'):
    """Load a set of common passwords from a file."""
    try:
        with open(file_path, 'r') as file:
            common_passwords = set(line.strip() for line in file)
        return common_passwords
    except FileNotFoundError:
        print(f"Warning: Could not find the file {file_path}. Common password check will not be performed.")
        return set()

def check_common_passwords(password, common_passwords):
    """Check if the password is too common."""
    if password in common_passwords:
        return False, "Password is too common."
    return True, "Password is not common."

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python strength_checker.py <password>")
        sys.exit(1)

    input_password = sys.argv[1]
    common_passwords = load_common_passwords()  # Load common passwords list

    # Check password strength
    strength_ok, strength_message = check_password_strength(input_password)
    common_ok, common_message = check_common_passwords(input_password, common_passwords)

    print(strength_message)
    if not strength_ok:
        print("Improve your password based on the feedback above.")
    else:
        print(common_message)
