import json
import uuid

ingredients_file = "/Users/colin/ingredients.txt"

count = 0
ingredients = set()
unprocessed = []

def load_ingredients():
    for line in open(ingredients_file, 'r'):
        ingredients.add(line.strip().lower())

load_ingredients()

ordered = sorted(ingredients)

with open(ingredients_file, 'w') as file:
    for i in ordered:
        file.write(i + '\n')

