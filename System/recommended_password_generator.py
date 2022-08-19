'''
Random password generation according to the user preference
'''

import string, random

def generate_password(alphabets, digits, special_characters, total_characters):
    # Enter password length
    password_len = int(input("Enter password length : "))

    # Enter the length of each character type
    alphabets_cnt = int(input("Enter the number of alphabets in password : "))
    digits_cnt = int(input("Enter the number of digits in password : "))
    special_characters_cnt = int(input("Enter the number of special characters in password : "))

    total_char_cnt = alphabets_cnt + digits_cnt + special_characters_cnt

    # Password validation by comparing password length and character length
    if total_char_cnt > password_len:
        print("Total characters count is greater than the password length")
        return
    else:
        # Initialize password
        recommended_password = []

        # picking random alphabets
        for i in range(alphabets_cnt):
            recommended_password.append(random.choice(alphabets))

        # picking random digits
        for i in range(digits_cnt):
            recommended_password.append(random.choice(digits))

        # picking random special characters
        for i in range(special_characters_cnt):
            recommended_password.append(random.choice(special_characters))

        if total_char_cnt < password_len:
            random.shuffle(total_characters)
            for i in range(password_len - total_char_cnt):
                recommended_password.append(random.choice(total_characters))

        # shuffling to make the final password
        random.shuffle(recommended_password)

        # Converting the list type to string type and print the final password
        completed_password = "".join(recommended_password)
        return completed_password

def main(): 
    # Type of characters to use for password generation
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%^&*()")
    total_characters = alphabets + digits + special_characters

    # Executing random password generator and print the password
    result_password = generate_password(alphabets, digits, special_characters, total_characters)
    print("Recommended Password :", result_password)

if __name__ == "__main__":
    main()
