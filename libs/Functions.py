import random


class Functions:
    def __init__(self):
        pass

    @staticmethod
    def clamp(num, mini=0, maxi=1):
        tr = num

        if num < mini:
            tr = mini
        if num > maxi:
            tr = maxi

        return tr

    @staticmethod
    def noise(n, strength=10):
        return n + random.randint(-strength, strength)
