import sys, random, time


def print(message, end='\n'):
    for c in message:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(random.randint(40, 100) / 1000)
    sys.stdout.write(end)


if __name__ == "__main__":
    s = ""
    for _ in range(1000):
        s = s + chr(random.randint(ord('a'), ord('z')))
    print(s)
