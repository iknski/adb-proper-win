from subprocess import Popen, PIPE
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from colorama import init, Fore
from pick import pick


init(autoreset=True)

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()

"""
находим удалённые пакеты
"""
deleted_packages = None
if deleted_packages is None:
    deleted_packages = []

with open("removed_apps.ini", mode="r", encoding="UTF-8") as rm_ini_file:
    lines = rm_ini_file.readlines()
    for line in lines:
        deleted_packages.append(line.strip())

if len(deleted_packages) == 0:
    print(
        f"-------------------------\n"
        f"{Fore.GREEN}No deleted apps!\n"
        f"{Fore.RESET}-------------------------"
        )
else:
    """
    формируем список имён пакетов - понадобится для лучшего понимания, что мы будем удалять
    """
    deleted_names = compare_position(deleted_packages)
    
    """
    добавляем имена к пакетам для удобства
    """
    deleted_full = list()
    index = 0
    for iter in deleted_names:
        deleted_full.append(f"{deleted_packages[index]} ({deleted_names[index]})")
        index = index + 1
    
    """
    формируем меню для выбора приложений
    """
    title = (
        f"Deleted apps...\n"
        f"Tap Space key for chose\n"
        f"-------------------------"
        )
    options = deleted_full
    selected = pick(
        options,
        title,
        indicator="> ",
        multiselect=True,
        min_selection_count=1,
    )
    
    print(
        f"-------------------------\n"
        f"Your choice:\n"
        f"-------------------------"
        )
    
    """
    формируем список для включения
    отрезаем лишнее из элементов списка, иначе будет ошибка
    для ADB нам нужно лишь имя пакета
    """
    packages_to_reinstall = list()
    for iter in selected:
        if "(" in iter[0]:
            packages_to_reinstall.append(iter[0].split(" (")[0])
    
    """
    часть ниже нужна лишь для того чтобы увидеть что мы будем удалять перед подтверждением
    """
    _list = list()
    for list in selected:
        for iter in list:
            _list.append(iter)
            selected_packages = _list[0::2]
    
    index = 0
    for iter in selected_packages:
        out = f"{index + 1}) {iter}"
        index = index + 1
        print(out)
    input(
        f"-------------------------\n"
        f"Press Enter to confirm..."
        )
    
    for iter in packages_to_reinstall:
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
