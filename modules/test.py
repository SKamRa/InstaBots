from random import randint
import random
from config import BASE_DIR

chrlists = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T','U', 'V', 'W', 'X', 'Y',
    'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'é', 'è', 'à', 'ù','È', 'À', 
    'Ù', 'ê', 'â', 'û', 'Ê', 'Â', 'Û', 'ë', 'ä', 'ü', 'Ë','Ä', 'Ü' '€', '$', '!', '@', 
    '?', ':', ',', ';', '§', 'µ', '£','^','%', '°','*', '#', '&', '~']
password = ""
for i in range(16):
    password = password + random.choices(chrlists)[0]
print(password)