import sys
import os





if __name__ == '__main__':
    top_dir = sys.argv[1]

    for folder in os.listdir(top_dir):
        if os.path.isdir(os.path.join(top_dir, folder)):
            dir = os.path.join(top_dir, folder)
            for txt in os.listdir(dir):
                if txt.startswith("path_hash_") and txt.endswith("_finished.txt"):
                    with open(os.path.join(dir, txt), 'rb') as f:
                        for line in f.readlines():
                            if ", Error" in line:
                                print os.path.join(dir, txt), line
                                break
