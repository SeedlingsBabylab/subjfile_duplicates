import xxhash
from multiprocessing import Process, Pool
import os
import time

hashf = xxhash.xxh64
files = []
dir = "./"

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
            hash_list.append("{}, {}\n".format(result[1], result[0]))
	p.close()
    #print('FINISHED {}/{}	ESTIMATED TIME REMAINING: {}'.format(counter, len(files), (time.time()-start_time)*(len(files)-counter)/counter))


if __name__ == '__main__':
    for txt in os.listdir(dir):
        start_time = time.time()
        if txt.startswith("path_hash_") and not txt.endswith("_finished.txt"):
            files = []
            hash_list = []
            with open(os.path.join(dir, txt), 'rb') as f:
                files.extend([line.replace("\n", "") for line in f.readlines()])
            multithread_checksum()
            print ("finished {}".format(txt))
            with open(os.path.join(dir, txt.replace(".txt", "_finished.txt")), 'w+') as f:
                for hash in hash_list:
                    f.write(hash)
            #os.remove(os.path.join(dir, txt))
