import string
import random


class Krypto:

    @staticmethod
    def base_str():
        return string.ascii_letters + string.digits

    @staticmethod
    def generate(length=6):
        return "".join([random.choice(Krypto.base_str()) for _ in range(length)])
