import argon2

def verify_password(file_path, password):
    with open(file_path, 'r') as file:
        hashed_password = file.read().strip()
        hasher = argon2.PasswordHasher()
        try:
            hasher.verify(hashed_password, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

def password():

    file_path = "password.txt"

    user_input_password = input("Mot de passe : ")
    if verify_password(file_path, user_input_password):
        print("Mot de passe correct.")
        return True
    else:
        print("Mot de passe incorrect.")
        return False
