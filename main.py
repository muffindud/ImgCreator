import sys
import os
import subprocess


def main(files, option):
    file_name = os.path.splitext(os.path.basename(files[0]))[0]
    img_file_name = file_name + ".img"
    img_file_content = b""
    for file in files:
        f_name = os.path.splitext(os.path.basename(file))[0] + ".bin"
        subprocess.run(["nasm", "-f", "bin", file, "-o", f_name])
        img_file_content += open(f_name, "rb").read()
        subprocess.run(["rm", f_name])
    img_file_content += b'\x00' * (1474560 - len(img_file_content))
    img_file = open(img_file_name, "wb")
    img_file.write(img_file_content)
    img_file.close()

    if option == '-y':
        try:
            subprocess.run(["vboxmanage", "storageattach", "SlayMachine", "--storagectl", ''"Floppy"'', "--port", "0", "--device", "0", "--type", "fdd", "--medium", os.getcwd() + "/" + img_file_name])
            subprocess.run(["vboxmanage", "startvm", "SlayMachine"])
        except:
            print("Error: Could not attach image to virtual machine.")
            print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
            sys.exit(1)
    elif option == '-a':
        try:
            subprocess.run(["vboxmanage", "storageattach", "SlayMachine", "--storagectl", ''"Floppy"'', "--port", "0", "--device", "0", "--type", "fdd", "--medium", os.getcwd() + "/" + img_file_name])
        except:
            print("Error: Could not attach image to virtual machine.")
            print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
            sys.exit(1)


if __name__ == "__main__":
    if sys.argv[1] == "-h":
        print("Make sure the virtual machine is named SlayMachine and has a floppy controller.")
        print("Usage: python3 main.py <file1.asm> <file2.asm> ... <fileN.asm> [option]")
        print("Options: -h: Help, -y: Attach image to virtual machine and run., -a: Attach image to virtual machine.")
        sys.exit(0)
    else:
        main(sys.argv[1:-1], sys.argv[-1])
