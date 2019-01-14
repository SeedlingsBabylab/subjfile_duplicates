import os
import sys
import json


hash_dict = {}
result_dir = "./"

def read_file(path):
    with open(path, 'rb') as f:
        for file in f.readlines():
            [file, hash] = file.replace("\n", "").rsplit(",", 1)
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

    other_dups = []
    trl_dups = []

    for key in hash_dict.keys():
        is_trl = 0
        if len(hash_dict[key]) > 1:
            entry = {}
            entry['num_duplicates'] = len(hash_dict[key])
            entry['duplicates'] = []
            for i in hash_dict[key]:
                entry['duplicates'].append(i)
                if ".trl" in i:
                    is_trl = 1
            if is_trl:
                trl_dups.append(entry)
            else:
                other_dups.append(entry)

    with open('dup_result_other.json', 'w') as f:
    	json.dump(other_dups, f, indent=4)

    with open('dup_result_trl.json', 'w') as f:
    	json.dump(trl_dups, f, indent=4)

# dup_list = [", ".join(hash_dict[key]) for key in hash_dict.keys() if len(hash_dict[key]) > 1]
# with open(os.path.join(result_dir, "dup_result_other.txt"), 'w+') as f:
#     with open(os.path.join(result_dir, "dup_result_trl.txt"), 'w+') as f_trl:
#         for dup in dup_list:
#             if ".trl" in dup:
#                 f_trl.write(dup + "\n")
#             elif "/Applications/" not in dup:
#                 f.write(dup + "\n")
