
import random
import string

class Generator:
    def create_password(self, length, digits, letters, specialchars):
        if length < 8:
            raise ValueError("Password length must be at least 8")
        if not (digits or letters or specialchars):
            raise ValueError("At least one character type (digits, letters, specialchars) must be selected")

        choices = ""
        if digits:
            choices += string.digits
        if letters:
            choices += string.ascii_letters
        if specialchars:
            choices += string.punctuation
        
        password = []
        if digits:
            password.append(random.choice(string.digits))
        if letters:
            password.append(random.choice(string.ascii_letters))
        if specialchars:
            password.append(random.choice(string.punctuation))
        
        for i in range(length - len(password)):
            password.append(random.choice(choices))
        random.shuffle(password)
        return ''.join(password)