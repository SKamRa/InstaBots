import random

from modules.config import BASE_DIR


def createPassword():
    chrlists = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T','U', 'V', 'W', 'X', 'Y',
        'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'é', 'è', 'à', 'ù','È', 'À', 
        'Ù', 'ê', 'â', 'û', 'Ê', 'Â', 'Û', 'ë', 'ä', 'ü', 'Ë','Ä', 'Ü' '€', '$', '!', '@', 
        '?', ':', ',', ';', '§', 'µ', '£','^','%', '°','*', '#', '&', '~']
    password = ""
    for i in range(16):
        password = password + random.choices(chrlists)[0]
    return str(password)

def createFullname():
    with open(f"{BASE_DIR}/data/usernames/available_first_names.txt", 'r') as firstnameslist:
        lines = firstnameslist.read().splitlines()
        firstname = random.choice(lines)
    with open(f"{BASE_DIR}/data/usernames/available_last_names.txt", 'r') as lastnameslist:
        lines = lastnameslist.read().splitlines()
        lastname = random.choice(lines)
    fullname = f'{firstname} {lastname}'
    return fullname

def main():
    createFullname()
    createPassword()

if __name__ == "__main__":
    main()