import json
import uuid
import codecs

file = "/Users/colin/Downloads/recipeitems-latest.json"
source = 'bbcfood'
required_attrs = ['image']
unwanted = ['_id', 'recipeYield', 'prepTime', 'ts']

def remove_unwanted_keys(dictionary):
    for u in unwanted:
        if u in dictionary:
            del dictionary[u]
    return dictionary

def valid(line):
    has_required = all(map(lambda x: line.get(x) is not None, required_attrs))
    is_source = line['source'] == source
    return has_required and is_source

with open(file) as f, codecs.open('preprocessed.json', 'w', encoding='utf-8') as b:
    for line in f:
        j = json.loads(line)
        if valid(j):
            j['id'] = str(uuid.uuid4())
            j['ingredients'] = j['ingredients'].split('\n')
            out = json.dumps(remove_unwanted_keys(j), ensure_ascii=False)
            print out
            b.write(out + '\n')

