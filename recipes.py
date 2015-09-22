import json
import uuid

file = "/Users/colin/Downloads/recipeitems-latest.json"

count = 0

def create_ingredient(name):
    uid = str(uuid.uuid4());
    print 'MERGE (f:Food{ name:"' + name + '"}) ON CREATE SET f.id = "' + uid +'";'
    return uid

def create_ingredient_rel(fid, iid):
    print 'MATCH (r:Recipe {id: "' + fid + '"}),(f:Food{id:"'+iid+'"}) CREATE (r)-[:CONTAINS]->(f);'

def ingredients_split(ingredients):
    return map(unicode.strip, ingredients.split("\n"))

def create_food(f):
    name = f.get('name')
    url = f.get('url')
    image = f.get('image')
    description = f.get('description')
    uid = str(uuid.uuid4())

    attrs = 'id: "' + uid + '"' 
    if name is not None:
        attrs = attrs + ', name: "' + name + '"' 
    if url is not None:
        attrs = attrs + ', source_url: "' + url + '", source_name: "BBC Food"'
    if image is not None:
        attrs = attrs + ', image_url: "' + image + '"'
    if description is not None:
        attrs = attrs + ', description: "' + description + '"'

    out = "MERGE (f:Food:Recipe {" + attrs + "});"
    print out.encode('ascii', 'ignore')

    i = ingredients_split(f.get('ingredients'))
    for x in i:
        x = x.encode('ascii','ignore')
        iid = create_ingredient(x)
        create_ingredient_rel(uid, iid)

for line in open(file, 'r'):
    j = json.loads(line)
    if j['source'] == 'bbcfood' and j.get('image') is not None:
        count = count + 1
        create_food(j)

