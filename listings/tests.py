from string import ascii_letters
import random

generate_random_string = lambda taille:"".join([ascii_letters[random.randint(0, len(ascii_letters)-1) ] for i in range(taille)])

print(generate_random_string(25))