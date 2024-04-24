import argon2  # Argon2 password hashing module

def verify_password(file_path, password):
    with open(file_path, 'r') as file:
        hashed_password = file.read().strip()
        hasher = argon2.PasswordHasher()  # Create an Argon2 password hasher instance
        try:
            hasher.verify(hashed_password, password)  # Verify the provided password against the hashed password
            return True  # Return True if verification succeeds
        except argon2.exceptions.VerifyMismatchError:
            return False  # Return False if verification fails

def password():
    file_path = "password.txt"  # Path to the file containing the hashed password

    user_input_password = input("Mot de passe : ")  # Prompt user for password input
    if verify_password(file_path, user_input_password):
        print("Mot de passe correct.")  # Print message for correct password
        return True  # Return True if password is correct
    else:
        print("Mot de passe incorrect.")  # Print message for incorrect password
        return False  # Return False if password is incorrect
