from re import findall
from subprocess import Popen, PIPE
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from app_list import disabled
from colorama import init, Fore


init(autoreset=True)

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()
import app_list
from app_list import installed_packages
from rm_list_pkgs import check_list_packages
from rm_list_nms import check_list_names

"""
сравниваем списки установленных пакетов с черным списком
"""
differences = list(filter(lambda it: it in installed_packages, check_list_packages))

print(f"-------------------------")
print(Fore.RED + f"Application's for removing...")
print(f"-------------------------")
index = 0
for iter in differences:
    out = f"{index + 1}) Name: {Fore.YELLOW + compare_position(differences)[index]} {Fore.RESET}Package: {Fore.GREEN + differences[index]}"
    index = index + 1
    if iter in disabled:
        out += Fore.RED + " Disabled"
    print(out)

while True:
    try:
        if len(differences) == 0:
            exit(
                Fore.GREEN + f"Your phone is in optimal condition\nNo apps to remove..."
            )
        print(f"-------------------------")
        input_nums = findall(
            "[\da]+",
            input(
                f"Enter the app numbers you want to remove separate by space\n"
                f'or type "a" to select all apps...\n'
                f"Warning !!!\n"
                f"If you have selected all apps or select keyboard to remove\n"
                f"make sure you have an additional keyboard installed\n"
                f">>> "
            ),
        )
        print(f"-------------------------")
        print(f"Your choice: ")
        pkgs_to_remove = list()
        nms_to_remove = list()
        for iter in input_nums:
            if input_nums[0] == "a" and len(input_nums) == 1:
                print(f"Selected: " + Fore.RED + "All Apps!!!")
                pkgs_to_remove = differences
                break
            pkgs_to_remove.append(differences[int(iter) - 1])
            print(
                f">> {Fore.YELLOW + compare_position(differences)[int(iter) - 1]}{Fore.RESET} - {Fore.GREEN + differences[int(iter) - 1]}"
            )
        break

    except (ValueError, IndexError):
        print("incorrect input, try again...")

input("Press Enter to confirm...")
print(f"-------------------------")

for iter in pkgs_to_remove:
    cmd_un = f"{work_directory} -d shell pm uninstall --user 0 {iter}"
    cmd_dsbl = f"{work_directory} -d shell pm disable-user --user 0 {iter}"
    uninstall = split(cmd_un)
    disable = split(cmd_dsbl)

    proc = Popen(uninstall, stdout=PIPE)
    output = proc.stdout.read()

    """
    запись в файл ЕСЛИ получен ответ "Success"
    отключение приложения если оно не может быть удалено
    """
    if output == b"Failure [-1000]\r\n":
        Popen(disable)

    elif output == b"Success\r\n":
        with open("removed_apps.ini", mode="a", encoding="UTF-8") as rm_ini_file:
            rm_ini_file.write(f"{iter}\n")

    print(f"{iter} - {output.decode()}")
    proc.terminate()
