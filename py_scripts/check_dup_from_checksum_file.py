import json

with open('checksums.txt') as f:
	res = json.load(f)

dups = []

for key in res:
	if len(res[key])>=2:
		entry = {}
		entry['num_duplicates'] = len(res[key])
		entry['duplicates'] = []
		for i in res[key]:
			entry['duplicates'].append(i)
		dups.append(entry)

with open('duplicates.json', 'w') as f:
	json.dump(dups, f)