import xxhash
from multiprocessing import Process, Pool
import os

hash_dict = {}
hashf = xxhash.xxh64
files = []
dir = "./"
hash_list = []

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


def multithread_checksum():
	p = Pool(20)
	counter = 0
	for i in range(0, len(files), 20):
		results = p.map_async(compute_hash, files[i:min(i+20, len(files))])
		results = results.get()
		for result in results:
            hash_list.append(result)
		counter += len(results)
		print('FINISHED {}/{}	ESTIMATED TIME REMAINING: {}'.format(counter, len(files), (time.time()-start_time)*(len(files)-counter)/counter))


if __name__ == '__main__':
    for txt in os.listdir(dir):
        if txt.startswith("path_hash_") and not txt.endswith("_finished.txt"):
            files.clear()
            hash_list.clear()
            with open(os.path.join(dir, txt), 'rb') as f:
                files.extend(f.readlines())
            multithread_checksum()
            with open(os.path.join(dir, txt.replace(".txt", "_finished.txt")), 'w+') as f:
                for hash in hash_list:
                    f.write(hash + "\n")
            os.remove(os.path.join(dir, txt))
