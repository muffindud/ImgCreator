import sys
import os
import subprocess


def main(file, option):
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

    if option == '-y':
        try:
            subprocess.run(["vboxmanage", "storageattach", "SlayMachine", "--storagectl", "\"Floppy\"", "--port", "0", "--device", "0", "--type", "fdd", "--medium", os.getcwd() + img_file])
            subprocess.run(["vboxmanage", "startvm", "SlayMachine"])
        except:
            print("Error: Could not attach image to virtual machine.")
            print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
            sys.exit(1)
    elif option == '-a':
        try:
            subprocess.run(["vboxmanage", "storageattach", "SlayMachine", "--storagectl", "\"Floppy\"", "--port", "0", "--device", "0", "--type", "fdd", "--medium", os.getcwd() + img_file])
        except:
            print("Error: Could not attach image to virtual machine.")
            print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
            sys.exit(1)


if __name__ == "__main__":
    if sys.argv[1] == "-h":
        print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
        print("Usage: python3 main.py <file.asm> [option]")
        print("Options: -h: Help, -y: Attach image to virtual machine and run., -a: Attach image to virtual machine.")
        sys.exit(0)
    else:
        main(sys.argv[1], sys.argv[2])
