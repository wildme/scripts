import sys
import time

class CharCircle:
    def __init__(self, chars):
        self.chars = chars
        self.value = self.chars[0]
        self.head = 0
        self.tail = len(self.chars) - 1

    def __iter__(self):
        return self

    def __next__(self):
        # item between head and tail
        self.value = self.head
        self.head = (self.head + 1) % self.tail # reset to 0 after tail
        return self.chars[self.value]

    def start(self):
        for _ in self:
            sys.stdout.write('\b')
            sys.stdout.write(_)
            sys.stdout.flush()
            time.sleep(0.3)

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def update(self, cnt):
        sys.stdout.write('\b' * len(str(eval('cnt - 1'))))
        sys.stdout.write(str(cnt))
        sys.stdout.flush()

class Dot:
    def __init__(self, length=3):
        self.length = length

    def start(self, count=0):
        if count < self.length:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
            self.start(count + 1)
        else:
            sys.stdout.write('\b \b' * self.length)
            self.start()
