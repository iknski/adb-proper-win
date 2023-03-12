from re import findall
from subprocess import Popen, PIPE
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from colorama import init, Fore


init(autoreset=True)

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()

deleted_apps = None
if deleted_apps is None:
    deleted_apps = []

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

with open("removed_apps.ini", mode="r", encoding="UTF-8") as rm_ini_file:
    lines = rm_ini_file.readlines()
    for line in lines:
        deleted_apps.append(line.strip())

print(f"-------------------------")
print(Fore.RED + f"Deleted apps:")
print(f"-------------------------")
index = 0
for iter in deleted_apps:
    print(
        f"{index + 1}) Name: {Fore.YELLOW + compare_position(deleted_apps)[index]} {Fore.RESET}Package: {Fore.GREEN + deleted_apps[index]}"
    )
    index = index + 1

while True:
    try:
        print(f"-------------------------")
        input_nums = findall(
            "[\da]+",
            input(
                f"Enter the app numbers you want to reinstall separate by space\n"
                f"-------------------------\n"
                f"Or type 'a' to select all apps: "
            ),
        )
        print(f"-------------------------")
        print(f"Your choice: ")
        pkgs_to_reinstall = list()
        nms_to_remove = list()
        for iter in input_nums:
            if input_nums[0] == "a" and len(input_nums) == 1:
                print(f"Selected: " + Fore.RED + "All Apps!!!")
                pkgs_to_reinstall = deleted_apps
                break
            pkgs_to_reinstall.append(deleted_apps[int(iter) - 1])
            print(
                f">> {Fore.YELLOW + compare_position(deleted_apps)[int(iter) - 1]}{Fore.RESET} - {Fore.GREEN + deleted_apps[int(iter) - 1]}"
            )
        break

    except (ValueError, IndexError):
        print("incorrect input, try again...")

input("Press Enter to confirm...")
print(f"-------------------------")

for iter in pkgs_to_reinstall:
    cmd_re = f"{work_directory} -d shell cmd package install-existing {iter}"
    reinstall = split(cmd_re)

    proc = Popen(reinstall, stdout=PIPE)

    output = proc.stdout.read()

    print(f"{output.decode()}")

    proc.terminate()

    with open("removed_apps.ini", mode="r", encoding="UTF-8") as rm_ini_file:
        lines = rm_ini_file.readlines()
    with open("removed_apps.ini", mode="w", encoding="UTF-8") as rm_ini_file:
        for line in lines:
            if line.strip("\n") != iter:
                rm_ini_file.write(line)
