import sys
import os
import hashlib
import pandas

def get_hash(file_name):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(file_name, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

if __name__ == "__main__":

    dir1 = sys.argv[1]
    dir2 = sys.argv[2]

    diff_version_list = []
    dir1_file = [file for file in os.listdir(dir1) if (os.path.isfile(os.path.join(dir1, file)) and not file.startswith("."))]

    for file in os.listdir(dir2):
        if file in dir1_file:
            path1 = os.path.join(dir1, file)
            path2 = os.path.join(dir2, file)
            dir1_hash = get_hash(path1)
            dir2_hash = get_hash(path2)
            if dir1_hash == dir2_hash:
                diff_version_list.append([path1, path2, "identical"])
            else:
                diff_version_list.append([path1, path2, "different"])


    df = pandas.DataFrame(diff_version_list, columns=['file_path_1', 'file_path_2', 'comparison'])
    df.to_csv("first_level_diff.csv", index=False)
