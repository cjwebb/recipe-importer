import codecs
import json

# read ingredients file, and put into memory
ingredients = set()
with codecs.open('/Users/colin/ingredients.txt', encoding='utf-8') as f:
    for line in f:
        ingredients.add(line.strip())

def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def only_longest(arr):
    return [max(arr, key=len)]

def ingredients_in_text(text):
    split_text = text.split(' ')
    split_in = []
    string_in = []
    substrings = [] 

    # todo - need to consider bigrams!

    for i in ingredients:
        if i in text:
            substrings.append(i)
        # contains token
        if i in text.lower():
            string_in.append(i)
        # equals token
        for s in split_text:
            if i == s:
                split_in.append(i)

    # get the longest ingredients, as this is often more specific
    # e.g. 'icecubes' would also match 'ice'
    if len(substrings) > 0:
        return only_longest(substrings)
    elif len(split_in) > 0:
        return only_longest(split_in)
    else:
        if len(string_in) > 0:
            return only_longest(string_in)

    # we didn't find anything
    return []

with codecs.open('preprocessed.json', encoding='utf-8') as f:
    with codecs.open('nice.json', 'w', encoding='utf-8') as f2:
        for line in f:
            j = json.loads(line)
            i = j['ingredients']

            parsed = []
            for x in i:
                parsed = parsed + ingredients_in_text(x)

            j['parsed_ingredients'] = unique_list(parsed)
            f2.write(json.dumps(j, ensure_ascii=False) + '\n')

