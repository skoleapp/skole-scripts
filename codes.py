import random

LETTERS = "ABCDEFGHJKLMNPQRSTUVWXY3456789"
LEN = 8
AMOUNT = 250

   
def main():    
    codes = set()
    while len(codes) < AMOUNT:
        code = "".join(random.sample(LETTERS, LEN))
        codes.add(f"{code}\n")
    
    with open("codes.txt", "w") as f:
        f.writelines(codes)
        
        
if __name__ == "__main__":
    main()
