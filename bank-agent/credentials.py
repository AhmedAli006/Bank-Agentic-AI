import random
import string

def generate_credentials(name):
    username = name.lower().replace(" ", "") + str(random.randint(100,999))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password