import sys
import os
import subprocess


def main(file):
    file_name = os.path.splitext(os.path.basename(file))[0]
    bin_file = file_name + ".bin"
    img_file = file_name + ".img"
    subprocess.run(["nasm", "-f", "bin", file, "-o", bin_file])
    size = os.path.getsize(bin_file)
    small = open(bin_file, "rb")
    big = open(img_file, "wb")
    big.write(small.read())
    trunc_size = b'\x00' * (1474560 - size)
    big.write(trunc_size)
    subprocess.run(["rm", bin_file])


if __name__ == "__main__":
    main(sys.argv[1])
