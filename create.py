from pathlib import Path
import random
import requests
from tqdm import tqdm 

random.seed(9115)
TERM = "time"
NODES = 1000

if not Path('wordlist.10000').exists():
    url = "https://www.mit.edu/~ecprice/wordlist.10000"
    with requests.get(url) as response, open('wordlist.10000', 'w') as f:
            f.write(response.text)

with open('wordlist.10000') as f:
    words = f.readlines()
words = [w.strip() for w in words if len(w.strip()) >= 4]

def create_file(filename: Path):
    extension = random.choice(['txt', 'conf'])
    filename = filename.with_suffix(f".{extension}")
    how_many = random.randint(100, 1000)
    
    with filename.open("w") as f:
        for _ in range(how_many):
            if random.randrange(100) == 0:
                word = TERM
            else:
                word = random.choice(words)
            value = random.randint(100, 1000)
            print(f"{word}={value}", file=f)

def create_files(path: Path):
    how_many = random.randint(3, 15)
    if how_many > 7:
        how_many = random.randint(7, 100)
    for _ in range(how_many):
        create_file(path / random.choice(words))

def main():
    nodes = []
    for _ in range(NODES):
        parent = random.randrange(len(nodes)) if nodes else None
        nodes.append((parent, random.choice(words)))

    paths = {}
    for idx, _ in enumerate(tqdm(nodes)):
        parent, name = nodes[idx]
        path = Path(name) if parent is None else paths[parent] / name
        paths[idx] = path
        path.mkdir()
        create_files(path)

if __name__ == '__main__':
    main()
