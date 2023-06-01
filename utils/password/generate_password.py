import string
from random import SystemRandom as st


def create_password() -> str:
    alphanum: str = string.ascii_letters + string.punctuation + string.digits
    password: str = "".join(st().choices(
        alphanum, k=20))
    return password.replace('"', '&').replace("'", '@')
