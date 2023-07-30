from os import stat
from subprocess import Popen, PIPE
from shlex import split
from main import phone_check, adb_terminate
from colorama import init, Fore


init(autoreset=True)

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()

if stat("list_to_remove.txt").st_size == 0:
    print(Fore.RED + f"list_to_remove.txt is empty, please fill it and try again...")
    adb_terminate()

with open("list_to_remove.txt", mode="r", encoding="UTF-8") as rm_list_file:
    rm_list = None
    if rm_list is None:
        rm_list = []
    _list = rm_list_file.readlines()
    for _ in _list:
        rm_list.append(_.strip())

    for iter in rm_list:
        cmd_un = f"{work_directory} -d shell pm uninstall --user 0 {iter}"
        cmd_dsbl = f"{work_directory} -d shell pm disable-user --user 0 {iter}"
        uninstall = split(cmd_un)
        disable = split(cmd_dsbl)

        proc = Popen(uninstall, stdout=PIPE)
        output = proc.stdout.read()

        if output == b"Failure [-1000]\r\n":
            Popen(disable)
        elif output == b"Failure [not installed for 0]\r\n":
            print(Fore.GREEN + f"Bloatware package ({iter}) not found!!!")

        elif output == b"Success\r\n":
            with open("removed_apps.ini", mode="a", encoding="UTF-8") as rm_ini_file:
                rm_ini_file.write(f"{iter}\n")

        print(f"{iter} - {output.decode()}")
        proc.terminate()
