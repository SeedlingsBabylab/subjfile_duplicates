import sys
import xxhash
import time
import scandir
import os
from multiprocessing import Process, Pool
import json

files = []
hash_dict = {}
hashf = xxhash.xxh64
start_time = 0

def get_all_files(path):
	for entry in scandir.walk(path):
		for item in entry[2]:
			files.append(os.path.join(entry[0], item))

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

def file_filter():
	global files
	exclude_file_type = ['mp4', 'wav']
	def get_extension(file):
		try:
			return file.split('.')[-1]
		except:
			return ""
	files = [x for x in files if not (get_extension(x) in exclude_file_type)]

def write_out():
	with open('output.txt', 'w') as f:
		json.dump(hash_dict, f)

def multithread_checksum():
	p = Pool(20)
	counter = 0
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
			write_out()

if __name__ == '__main__':
    dir_1 = sys.argv[1]
    dir_2 = sys.argv[2]

    get_all_files(dir_1)

    get_all_files(dir_2)

    file_filter()
    global start_time
    start_time = time.time()
    multithread_checksum()
