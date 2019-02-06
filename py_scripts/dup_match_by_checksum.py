from multiprocessing import Process, Pool
import scandir
import os
import sys
import xxhash
import json
import time
import argparse

hashf = xxhash.xxh64

def compute_hash(file):
	def file_as_blockiter(file, blocksize=4096):
		with open(file, 'rb') as f:
			block = f.read(blocksize)
			while len(block)>0:
				yield block
				block = f.read(blocksize)
	hash = hashf()
	try:
		for block in file_as_blockiter(file):
			hash.update(block)
		return (hash.hexdigest(), file)
	except:
		return ("Error", file)

def file_filter(files, exclude_file_type):
	def get_extension(file):
		try:
			return file.split('.')[-1]
		except:
			return ""
	files = [x for x in files if not (get_extension(x) in exclude_file_type)]
	return files

def write_out(hash_dict):
	with open('output.txt', 'w') as f:
		json.dump(hash_dict, f)

def multithread_checksum(files):
	p = Pool(20)
	counter = 0
	hash_dict = {}
	for i in range(0, len(files), 20):
		results = p.map_async(compute_hash, files[i:min(i+20, len(files))])
		results = results.get()
		for result in results:
			if result[0] in hash_dict:
				hash_dict[result[0]].append(result[1])
			else:
				hash_dict[result[0]] = []
				hash_dict[result[0]].append(result[1])
		counter += len(results)
		print('FINISHED {}/{}	ESTIMATED TIME REMAINING: {}'.format(counter, len(files), (time.time()-start_time)*(len(files)-counter)/counter))
		if counter%100==0:
			write_out(hash_dict)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Computing xxhash of all files in a given list')
	parser.add_argument('--input', action='store', required=True, help='The file that contains paths to files whose checksum needs to be computed')
	parser.add_argument('--filter', action='store', default='wav,mp4', help='The file types to be excluded from duplicate check, separated by comma, by default, wav and mp4 files will be excluded')
	with open(sys.argv[1]) as f:
		files = f.readlines()
	files = [x.rstrip() for x in files]
	files = file_filter(files, args.filter.split(','))
	global start_time
	start_time = time.time()
	multithread_checksum(files)
