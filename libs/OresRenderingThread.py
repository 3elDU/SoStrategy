from threading import *


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.ores = {}
