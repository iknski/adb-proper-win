from os import stat, path
from subprocess import call, Popen, PIPE
from time import sleep
from colorama import init, Fore
from psutil import process_iter
from art import tprint


init(autoreset=True)

work_directory = None
if work_directory is None:
    work_directory = []

list_to_remove = None
if list_to_remove is None:
    list_to_remove = []


def _hello():
    hello = [
        "Welcome to the ADB_Proper!",
        "Created by @iknski from the 4PDA",
        "Searching for the ADB",
        "it will take some time",
        "please wait...",
    ]

    for x in hello:
        print(Fore.MAGENTA + x)
        sleep(1)


def _create():
    wd_ini_file = open("work_directory.ini", mode="a", encoding="UTF-8")
    wd_ini_file.close()
    rm_list_file = open("list_to_remove.txt", mode="a", encoding="UTF-8")
    rm_list_file.close()
    rm_ini_file = open("removed_apps.ini", mode="a", encoding="UTF-8")
    rm_ini_file.close()


def _version():
    with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
        work_directory = wd_ini_file.readline().strip()
    call([work_directory, "version"])


def _device_id():
    with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
        work_directory = wd_ini_file.readline().strip()
    output = Popen(
        [work_directory, "devices", "-l"], shell=False, stdout=PIPE, stderr=PIPE
    )

    with output.stdout:
        for line in iter(output.stdout.readline, b""):
            full_id = line.decode().strip()
            if "device:" in full_id:
                sn = list(filter(None, full_id.split(" ")))[0]
                device = list(filter(None, full_id.split(" ")))[4]
                model = list(filter(None, full_id.split(" ")))[3]
                print(
                    f"Device connected as:\n",
                    f"{Fore.YELLOW + device}\n",
                    f"{Fore.BLUE + model}\n",
                    Fore.GREEN + f"serial:{sn}",
                )
    output.terminate()


def phone_check():
    with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
        work_directory = wd_ini_file.readline().strip()

    proc = Popen([work_directory, "shell", "exit"], shell=False, stderr=PIPE)
    output = proc.stderr.read()
    if output == b"adb.exe: no devices/emulators found\r\n":
        print(f"Device is not connected!")
        proc.terminate()
        input("Press Enter to exit...")
        exit(Fore.RED + f"Script is closed!")


def adb_terminate():
    for proc in process_iter():
        name = proc.name()
        if name == "adb.exe":
            proc.terminate()


def main():
    if not path.isfile("work_directory.ini") or stat("work_directory.ini").st_size == 0:
        _create()
        _hello()

        import adb_search
        from adb_search import adb_found

        if not adb_found:
            import not_adb
        else:
            import adb_version

            print(f"-------------------------")
            _version()
            print(f"-------------------------")
            _device_id()
            import user_choice

    else:
        with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
            work_directory = wd_ini_file.readline().strip()
            work_directory = work_directory.replace("\\", "/")
        _version()
        print(f"-------------------------")
        _device_id()
        import user_choice


if __name__ == "__main__":
    tprint("ADB-Proper")
    print(Fore.BLUE + f"version 1.21 stable")
    print(
        Fore.BLUE
        + f">> added the ability to delete applications through the list_to_remove.txt ..."
    )
    print(Fore.BLUE + f">> added art - ADB-Proper title ...")
    print(f"-------------------------")
    main()
    adb_terminate()
    input("press Enter to exit")
