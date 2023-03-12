from subprocess import Popen, PIPE
from adb_search import adb_found
from add_env import add_sys_env
from colorama import init, Fore, Back


"""
Формируем вывод с найденными программами и их версией
"""
init(autoreset=True)

index = 0
get_version = None  # временный список версий
app_version = None  # словарь с полным путем к приложению и его версией
if get_version is None:
    get_version = []
if app_version is None:
    app_version = {}
for x in adb_found:
    output = Popen([x, "version"], shell=False, stdout=PIPE)
    with output.stdout:
        for line in iter(output.stdout.readline, b""):
            if "Version" in line.decode().strip():
                get_version.append(line.decode().strip())
                index = index + 1
                app_version[x] = get_version[0]
    output.terminate()

if len(adb_found) == 1:
    print(
        f"-------------------------\n"
        f"Directory selected for work: {Fore.GREEN + adb_found[0]}"
    )
    work_directory = adb_found[0]
    with open("work_directory.ini", mode="w", encoding="UTF-8") as wd_ini_file:
        wd_ini_file.write(work_directory)

elif len(adb_found) >= 2:
    print(Back.GREEN + f"Found copies of the ADB:")
    print(f"-------------------------")
    index = 0
    for x in adb_found:
        index = index + 1
        print(f"{str(index)}) {x}  -  {Fore.RED + get_version.pop()}")

    answer_3 = int(
        input(
            f"-------------------------\n"
            f"Choose which one you will work with\n"
            f"Enter a number: >>> "
        )
    )
    for iter in range(len(adb_found)):
        if answer_3 == iter + 1:
            print(
                f"-------------------------\n"
                f"Directory selected for work: {Fore.GREEN + adb_found[iter]}"
            )
            work_directory = adb_found[iter]
            with open("work_directory.ini", mode="w", encoding="UTF-8") as wd_ini_file:
                wd_ini_file.write(work_directory)

"""
вносим найденную программу в системные переменные
"""
print(f"...adding work directory to system environment...")
sys_env = work_directory.rstrip(r"\adb.exe")
add_sys_env(sys_env)
print(f"...system environment updated...")
