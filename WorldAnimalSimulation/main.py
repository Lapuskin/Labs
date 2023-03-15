from animals import Lion
from plain import Plain
import fire


plain = Plain()

def start():
    plain.start()

def step():
    plain.step()


def add(essence, x, y):
    print(x, y)
    plain.add(essence, x, y)


def remove(x, y):
    plain.remove(x, y)


if __name__ == '__main__':
    fire.Fire()
