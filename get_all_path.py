import scandir
import os.path
import sys

files = []
num_per_f = 100
result_dir = "/Users/bergelsonlab/Desktop/github/seedlings/subjfile_duplicates/output/bergelson"

def get_all_files(path):
	for entry in scandir.walk(path):
		for item in entry[2]:
			files.append(os.path.join(entry[0], item))


if __name__ == '__main__':
	dir = sys.argv[1]

	for folder in os.listdir(dir):
		files = []
		folder_path = os.path.join(dir, folder)
		if os.path.isdir(folder_path):
			get_all_files(folder_path)

			print("finish traversing path")

			for i in range(0, len(files)/num_per_f+1):
				with open(os.path.join(result_dir, folder, "path_hash_{}.txt".format(i)), 'w+') as f:
					for file in files[i*num_per_f : (i+1)*num_per_f]:
						f.write(file + "\n")
