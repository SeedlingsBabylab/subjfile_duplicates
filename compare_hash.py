import os
import sys


hash_dict = {}
result_dir = "./"

def read_file(path):
    with open(path, 'rb') as f:
        for file in f.readlines():
            [file, hash] = file.replace("\n", "").split(",")
            if hash in hash_dict:
                hash_dict[hash].append(file)
            else:
                hash_dict[hash] = [file]

def process_dir(dir1):
    for folder in os.listdir(dir1):
        if os.path.isdir(os.path.join(dir1, folder)):
            dir = os.path.join(dir1, folder)
            for txt in os.listdir(dir):
                if txt.startswith("path_hash_") and txt.endswith("_finished.txt"):
                    read_file(os.path.join(dir, txt))

def get_dup():
    return


if __name__ == '__main__':
    dir1 = sys.argv[1]
    process_dir(dir1)

    if (len(sys.argv) > 2):
        dir2 = sys.argv[2]
        process_dir(dir2)

dup_list = [", ".join(hash_dict[key]) for key in hash_dict.keys() if len(hash_dict[key]) > 1]
with open(os.path.join(result_dir, "dup_result.txt"), 'w+') as f:
    for dup in dup_list:
        f.write(dup + "\n")
