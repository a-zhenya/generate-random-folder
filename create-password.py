from pathlib import Path
import random
import requests
from tqdm import tqdm 
import string
import zlib

random.seed(58930)
NODES = 1000
FILES = NODES * 20
OPTION = 2 # 1 - random text/password.txt
           # 2 - random data

if not Path('wordlist.10000').exists():
    url = "https://www.mit.edu/~ecprice/wordlist.10000"
    with requests.get(url) as response, open('wordlist.10000', 'w') as f:
        f.write(response.text)

with open('wordlist.10000') as f:
    words = f.readlines()
words = [w.strip() for w in words if len(w.strip()) >= 4]

JPEG_DATA = zlib.decompress(b''.join([x.to_bytes() for x in [
 120, 156, 251, 127, 227, 255, 3, 6, 1, 47,
 55, 79, 55, 6, 70, 70, 70, 6, 15, 32,
 100, 248, 255, 144, 97, 157, 107, 69, 102, 26,
 3, 131, 167, 167, 22, 3, 7, 3, 3, 3,
 59, 131, 16, 35, 51, 3, 35, 144, 5, 194,
 82, 140, 172, 96, 58, 9, 136, 165, 161, 236,
 44, 32, 214, 128, 170, 97, 2, 0, 255, 58,
 11, 180
]]))

A_OUT = [11, 1, 0, 0]
def get_random_data():
    option = random.randrange(4)
    if option == 0: # Random Data
        return b''.join(random.randrange(255).to_bytes() for _ in range(1000))
    elif option == 1: # Picture
        return JPEG_DATA
    elif option == 2: # a.out
        return b''.join(x.to_bytes() for x in A_OUT)
    return b'' # empty

def get_random_text():
    return "".join(random.choices(string.ascii_letters + string.digits, k=25))

def main():
    nodes = []
    for _ in range(NODES):
        parent = random.randrange(len(nodes)) if nodes else None
        nodes.append((parent, random.choice(words)))

    paths = {}
    for idx, (parent, name) in enumerate(nodes):
        path = Path(name) if parent is None else paths[parent] / name
        paths[idx] = path
        path.mkdir()

    files = []
    for _ in range(FILES):
        parent = random.randrange(len(nodes)) if nodes else None
        files.append((parent, random.choice(words)))
    
    password = False
    for i, (parent, name) in enumerate(files):
        filepath = paths[parent] / name
        content = get_random_text() if OPTION == 1 else get_random_data()
        if not password and random.random() < (i + 1)/FILES:
            password = True
            if OPTION == 1:
                filepath = paths[parent] / "password.txt"
            if OPTION == 2:
                content = get_random_text()
            print(content)
            with filepath.open("w") as f:
                print(content, file=f)
            continue
        if filepath.exists():
            continue
        with filepath.open("wb" if OPTION == 2 else "w") as f:
            f.write(content)
        


if __name__ == '__main__':
    main()
