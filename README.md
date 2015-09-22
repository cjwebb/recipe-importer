# Recipe Importer

Hacky scripts to import some recipes into Neo4J. It currently depends on having a hardcoded file-name in `recipes.py`

    python recipes.py > out.cypher
    neo4j-shell -host 127.0.0.1 -file out.cypher

