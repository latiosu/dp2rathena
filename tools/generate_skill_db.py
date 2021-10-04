import os
import urllib.request
import yaml

# custom dumper to match rathena yaml formatting
class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

# rathena renewal item_db yaml files)
source = 'https://raw.githubusercontent.com/rathena/rathena/master/db/re/skill_db.yml'
results = dict()

# 1. fetch and parse source file
response = urllib.request.urlopen(source).read().decode('utf-8')
db = yaml.load(response, Loader=yaml.FullLoader)

# 2. ingest records
for record in db['Body']:
    results[record['Id']] = record
    del results[record['Id']]['Id'] # remove redundant id value

# 3. output into db directory
filename = os.path.join(os.path.dirname(__file__), '../dp2rathena/db/skill_db.yml')
with open(filename, 'w') as f:
    # skip sorting since already sorted in source
    output = yaml.dump(results, Dumper=MyDumper, sort_keys=False)
    f.write(output)
