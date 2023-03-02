from plain import Plain

if __name__ == '__main__':
    plain = Plain()
    i = 0
    plain.start()
    while i != 5:
        i += 1
        plain.step()

