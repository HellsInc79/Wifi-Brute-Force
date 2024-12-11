import random
import string
import os

def select_choice():
    """Selects a random character, digit, or symbol for password generation."""
    choice_code = random.randint(1, 10)

    if choice_code in range(1, 7):
        return random.choice(string.ascii_lowercase)  # Letters
    elif choice_code in range(7, 9):
        return random.choice(string.digits)  # Digits
    elif choice_code == 9:
        return random.choice("-_")  # Symbols
    elif choice_code == 10:
        return None  # No addition for this round

def generate_passwords(limit_length, passwords_per_length):
    """Generates passwords of increasing lengths up to a specified limit."""
    passwords = []

    for length in range(8, limit_length + 1):
        for _ in range(passwords_per_length):
            password = ""

            for _ in range(length):
                char = select_choice()
                if char:
                    password += char

            passwords.append(password)

    return passwords

def main():
    print("[==================================================]")
    print("                Key Combinator 1.0.0")
    print("[==================================================]")
    print("                  Developed By HellsInc")
    print("[==================================================]")

    # Get user input for password length limit
    while True:
        try:
            limit_length = int(input("What is the limit length for creating passwords? (8-?): "))
            if limit_length < 8:
                raise ValueError("Length must be at least 8.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Get user input for number of passwords per length
    while True:
        try:
            passwords_per_length = int(input("How many passwords will be generated per length? "))
            if passwords_per_length <= 0:
                raise ValueError("Number must be greater than 0.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    print("\nGenerating Passwords...\n")

    passwords = generate_passwords(limit_length, passwords_per_length)

    output_file = "passlist_raw.txt"
    with open(output_file, "w") as file:
        for password in passwords:
            file.write(password + "\n")

    absolute_path = os.path.abspath(output_file)

    print("[==========================]")
    print("  Creating Of List Complete")
    print(f"  Passwords generated: {len(passwords)}")
    print(f"  Password list saved at: {absolute_path}")
    print("[==========================]")
    print("\nPress any key to exit...")

if __name__ == "__main__":
    main()
