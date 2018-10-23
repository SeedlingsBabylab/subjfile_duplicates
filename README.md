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

### dup_match_by_checksum.py
This script computes the xxhash of each file and stores the hashes in a dictionary for later write-out to serialized json format.  
To obtain the dictionary of checksums, run
```
python dup_match_by_checksum.py files.txt
```
where files.txt is a list of files to compute xxhash for. files.txt is an optional argument, which if not given, will trigger the script to crawl the storage file system.  
The output of the script is checksums.txt

### check_dup_from_checksum_file.py
This script outputs groups of duplicate files based on checksums.txt.  
```
python check_dup_from_checksum_file.py
```

### first_level.py
This script outputs a csv specifying files in the first level of two directories with same name but different contents.
```
python first_level.py path/to/first/directory path/to/second/directory
```

### dup_match_all.py
This script outputs a csv specifying files in the first level of two directories with same name but different contents.
```
python dup_match_all.py path/to/first/directory path/to/second/directory
```
