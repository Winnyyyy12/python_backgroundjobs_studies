import gzip
import multiprocessing
import os
import shutil


def compress_file(file_path):
    compressed_file = file_path+'.gz'
    with open(file_path, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"compressed{file_path} to {compressed_file}")


if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]
    processess = []
    for file in files:
        p = multiprocessing.Process(target=compress_file, args=(file,))
        processess.append(p)
        p.start()

    for p in processess:
        p.join()
    print("All files completed")


def decompress_file(file_path):
    if not file_path.endswith('.gz'):
        print(f"{file_path} is not a gzip file")
        return
    decompressed_file = file_path[-3]
    with gzip.open(file_path, 'rb') as f_in:
        with open(decompressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"decompressed{file_path} to {decompressed_file}")


if __name__ == "__main__":
    files = ["file1.txt.gz", "file2.txt.gz", "file3.txt.gz"]
    processes = []
    for file in files:
        p = multiprocessing.Process(target=decompress_file, args=(file,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print("All files decompressed")
