import scandir
import os
import argparse
import re

'''
	Use the scandir library (faster implementation than os.walk) to retrieve a list of files in a particular directory
	scandir.walk() returns (root dir, folders, files)
'''
def get_all_files(path):
	for entry in scandir.walk(path):
		for item in entry[2]:
			files.append(os.path.join(entry[0], item))

'''
	Converts matching rules to regex format
	e.g.
		MyFolder/*  -> ^MyFolder/.*$
		This regex rule will match all subdirectories of 'MyFolder', effectively excluding the directory 'MyFolder'
		*SomeString* -> ^.*SomeString.*$
		This regex rule will match all files with path that contains the string 'SomeString'
'''
def process_ignore_config(ignore_config):
	rules = []
	for config in ignore_config:
		config = config.replace('.', '\.') # To escape for . in the regex syntax
		config = config.replace('*', '.*')
		#config = config.replace('*', '')
		config = '^' + config + '$'
		rules.append(config)
	return rules


'''
	Remove all files matching any of the ignore rules from the list of all files
'''
def ignore(files, ignore_config):
	new_files = []
	for file in files:
		match_rule = False
		for rule in ignore_config:
			if re.match(rule, file):
				match_rule = True
				break
		if not match_rule:
			new_files.append(file)
	return new_files

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Crawling directories with the option to ignore certain filetypes and folders')
	parser.add_argument('--crawl', action='store_true')
	parser.add_argument('--ignore', action='store')
	parser.add_argument('--input', action='store')
	args = parser.parse_args()
	files = []
	if args.crawl:
		get_all_files('/Volumes/pn-opus/Seedlings')
		with open('files.txt', 'w') as f:
			for file in files:
				f.write(file + '\n')
	elif args.input:
		with open(args.input) as f:
			files = [x.strip() for x in f.readlines()]
	if args.ignore:
		with open(args.ignore) as f:
			ignore_config = [x.strip() for x in f.readlines()]
		ignore_config = process_ignore_config(ignore_config)
		files = ignore(files, ignore_config)
		with open('files-with-ignore.txt', 'w') as f:
			for file in files:
				f.write(file + '\n')
