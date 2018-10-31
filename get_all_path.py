import scandir
import os.path
import sys

files = []
num_per_f = 100
dir = "./"

def get_all_files(path):
	for entry in scandir.walk(path):
		for item in entry[2]:
			files.append(os.path.join(entry[0], item))


if __name__ == '__main__':
    dir = sys.argv[1]

    get_all_files(dir)

    for i in range(0, len(files)/num_per_f+1):
        with open(os.path.join(dir, "path_hash_{}.txt".format(i)), 'w+') as f:
            for file in files[i*num_per_f : (i+1)*num_per_f-1]:
                f.write(file + "\n")
