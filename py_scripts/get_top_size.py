import scandir
import os.path
import sys
import math

def get_size_sum(path):
    total_size = 0
    for entry in scandir.walk(path):
        for item in entry[2]:
            total_size += os.path.getsize(os.path.join(entry[0], item))
    return total_size

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

if __name__ == '__main__':
    dir = sys.argv[1]
    with open("folder_size.txt", 'w+') as f:
        for folder in os.listdir(dir):
            path = os.path.join(dir, folder)
            if os.path.isdir(path):
                size = convert_size(get_size_sum(path))
            else:
                size = convert_size(os.path.getsize(path))
            print("{}: {}\n".format(path, size))
            f.write([path, size] + "\n")
