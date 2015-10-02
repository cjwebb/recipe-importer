# Recipe Importer

Hacky scripts to import some recipes into Neo4J. It currently depends on having a few hardcoded file-names though.

Run these 3 scripts to munge data

    python preprocess.py
    python process_ingredients.py
    python recipes.py

And do this to load into local neo4j

    neo4j-shell -host 127.0.0.1 -file out.cypher

Putting this data live currently involves

    cd /usr/local/Cellar/neo4j/2.2.1/libexec
    tar -cjf graph.tar.bz2 data/graph.db
