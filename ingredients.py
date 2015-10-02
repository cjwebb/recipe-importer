import json
import uuid

file = "/Users/colin/Downloads/recipeitems-latest.json"
ingredients_file = "/Users/colin/ingredients.txt"

count = 0
ingredients = set()
unprocessed = []

def ingredients_split(ingredients):
    return map(unicode.strip, ingredients.split("\n"))

def load_ingredients():
    for line in open(ingredients_file, 'r'):
        ingredients.add(line.strip())

def ingredients_in_line(line):
    collection = []
    for i in ingredients:
        if i.lower() in line.lower():
            collection.append(i)

    return collection

def process_food(f):
    i = ingredients_split(f.get('ingredients'))
    for x in i:
        x = x.encode('utf-8','ignore')
        ingredients = ingredients_in_line(x)

        if len(ingredients) == 0:
            unprocessed.append(x) 

load_ingredients()

for line in open(file, 'r'):
    j = json.loads(line)
    if j['source'] == 'bbcfood' and j.get('image') is not None:
        count = count + 1
        process_food(j)

for u in set(unprocessed):
    print u

print "-------------"
print len(set(unprocessed))
