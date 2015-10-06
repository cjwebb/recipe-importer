import json
import uuid
import codecs

file = "nice.json"

count = 0

def create_ingredient(name):
    uid = str(uuid.uuid4());
    cypher = 'MERGE (f:Food{ name:"' + name + '"}) ON CREATE SET f.id = "' + uid +'";'
    return uid, cypher

def create_ingredient_rel(fid, iname):
    return 'MATCH (r:Recipe {id: "' + fid + '"}),(f:Food{name:"'+iname+'"}) CREATE (r)-[:CONTAINS]->(f);'

def create_food(f):
    name = f.get('name')
    url = f.get('url')
    image = f.get('image')
    description = f.get('description')
    id = f.get('id')

    attrs = 'id: "' + id + '"'
    if name is not None:
        attrs = attrs + ', name: "' + name + '"' 
    if url is not None:
        attrs = attrs + ', source_url: "' + url + '", source_name: "BBC Food"'
    if image is not None:
        attrs = attrs + ', image_url: "' + image + '"'
    if description is not None:
        attrs = attrs + ', description: "' + description + '"'

    with codecs.open('cypher.out', 'a', encoding='utf-8') as out:
        out.write("MERGE (f:Food:Recipe {" + attrs + "});"+'\n')

        for x in f.get('parsed_ingredients'):
            iid, cypher = create_ingredient(x)
            out.write(cypher + '\n')
            out.write(create_ingredient_rel(id, x) + '\n')

for line in codecs.open(file, encoding='utf-8'):
    j = json.loads(line)
    create_food(j)
    count = count + 1

print count
