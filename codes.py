import random

LETTERS = "ABCDEFGHJKMNPQRSTUVWXYZ123456789"
AMOUNT = 250

with open("codes.txt", "w") as f:
    for _ in range(AMOUNT):
        code = "".join(random.sample(LETTERS, 6))
        f.write(f"{code}\n")
