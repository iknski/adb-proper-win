from re import findall
from subprocess import Popen, PIPE
from rm_list_pkgs import check_list_packages
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from colorama import init, Fore


init(autoreset=True)

disabled_packages = None
if disabled_packages is None:
    disabled_packages = []

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()

proc = Popen(work_directory + " shell pm list packages -d", shell=False, stdout=PIPE)

with proc.stdout:
    for line in iter(proc.stdout.readline, b""):
        disabled_packages.append(line.decode().strip()[8:])
proc.terminate()

print(f"-------------------------")
print(f"Disabled apps: ")
print(f"-------------------------")
index = 0
for iter in disabled_packages:
    if iter not in check_list_packages:
        print(f"{index + 1}) Package: {Fore.GREEN + iter}")
    elif iter in check_list_packages:
        print(
            f"{index + 1}) Name: {Fore.YELLOW + compare_position(disabled_packages)[index - 1]} {Fore.RESET}Package: {Fore.GREEN + iter}"
        )
    index = index + 1

while True:
    try:
        if len(disabled_packages) == 0:
            exit(Fore.GREEN + f"All apps enabled...")
        print(f"-------------------------")
        input_nums = findall(
            "[\da]+",
            input(
                f"Enter the app numbers you want to enable separate by space\n"
                f"-------------------------\n"
                f"Or type 'a' to select all apps: "
            ),
        )
        print(f"-------------------------")
        print(f"Your choice: ")
        pkgs_to_enable = list()
        nms_to_enable = list()
        for iter in input_nums:
            if input_nums[0] == "a":
                print(f"Selected: " + Fore.RED + "All Apps!!!")
                pkgs_to_enable = disabled_packages
                break
            pkgs_to_enable.append(disabled_packages[int(iter) - 1])

        for list_iter in pkgs_to_enable:
            if list_iter not in check_list_packages:
                print(f">> Package: {Fore.GREEN + list_iter}")
            elif list_iter in check_list_packages:
                print(
                    f">> {Fore.YELLOW + compare_position(disabled_packages)[index - 1]}{Fore.RESET} - {Fore.GREEN + list_iter}"
                )
            index = index + 1
        break

    except (ValueError, IndexError):
        print("incorrect input, try again...")

input("Press Enter to confirm...")
print(f"-------------------------")

print(pkgs_to_enable)
for iter in pkgs_to_enable:
    cmd_enbl = f"{work_directory} -d shell pm enable --user 0 {iter}"
    enable = split(cmd_enbl)
    proc = Popen(enable, stdout=PIPE)
    output = proc.stdout.read()

    print(f"{iter} - {output.decode()}")
    proc.terminate()
