# This repository hosts code for checking duplicate files on the cloud storage

## For robustness, duplicate file checking are broken down into several stages, each done using a script

### list_files.py
This script has two functionalities: 1. crawling the cloud storage file system for a complete list of files that are present 2. process the list of files to generate a new list that excludes certain files according to the given ignore rules.  
To crawl the file system, run
```
python list_files.py --crawl
```
A text file 'files.txt' that contains a list of files on the storage will be generated.  
To exclude ignore files, run
```
python list_files.py --ignore ignore.txt --input files.txt
```
where ignore.txt contains the ignore rules and files.txt is the list of all files.