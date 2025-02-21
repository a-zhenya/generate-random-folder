import random

ROOT_NAMES = ["config", "options", "parameters", "settings", "data", "files"]

with open('wordlist.10000') as f:
    words = f.readlines()
words = [w.strip() for w in words if len(w.strip()) >= 4]

def main():
    res = {root: [] for root in ROOT_NAMES}
    for i in range(100_000):
        random.seed(i)
        root = random.choice(words)
        if root in ROOT_NAMES:
            res[root].append(i)

    for root in ROOT_NAMES:
        print(root, res[root])

if __name__ == '__main__':
    main()
