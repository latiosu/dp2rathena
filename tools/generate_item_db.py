import os
import urllib.request
import yaml

# rathena renewal item_db yaml files)
sources = [
    'https://raw.githubusercontent.com/rathena/rathena/master/db/re/item_db_usable.yml',
    'https://raw.githubusercontent.com/rathena/rathena/master/db/re/item_db_equip.yml',
    'https://raw.githubusercontent.com/rathena/rathena/master/db/re/item_db_etc.yml',
]
results = dict()

for url in sources:
    # 1. fetch and parse source file
    response = urllib.request.urlopen(url).read().decode('utf-8')
    db = yaml.load(response, Loader=yaml.FullLoader)

    # 2. ingest records
    for record in db['Body']:
        results[record['Id']] = record['AegisName']

# 3. output into db directory
filename = os.path.join(os.path.dirname(__file__), '../dp2rathena/db/item_db.yml')
with open(filename, 'w') as f:
    output = yaml.dump({'items': results}, sort_keys=True)
    f.write(output)
