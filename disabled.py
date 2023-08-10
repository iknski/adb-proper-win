from subprocess import Popen, PIPE
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from colorama import init, Fore
from pick import pick


init(autoreset=True)

disabled_packages = None
if disabled_packages is None:
    disabled_packages = []

with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

phone_check()

"""
находим отключенные пакеты
"""
proc = Popen(work_directory + " shell pm list packages -d", shell=False, stdout=PIPE)

with proc.stdout:
    for line in iter(proc.stdout.readline, b""):
        disabled_packages.append(line.decode().strip()[8:])
proc.terminate()

"""
A если нет отключенных пакетов
"""
if len(disabled_packages) == 0:
    print(
        f"-------------------------\n"
        f"{Fore.GREEN}No disabled apps!\n"
        f"{Fore.RESET}-------------------------"
        )
else:
    """
    формируем список имён пакетов - понадобится для лучшего понимания, что мы будем удалять
    """
    disabled_names = compare_position(disabled_packages)

    """
    добавляем имена к пакетам для удобства
    """
    disabled_full = list()
    index = 0
    for iter in disabled_names:
        disabled_full.append(f"{disabled_packages[index]} ({disabled_names[index]})")
        index = index + 1

    """
    формируем меню для выбора приложений
    """
    title = (
        f"Disabled apps...\n"
        f"Tap Space key for chose\n"
        f"-------------------------"
        )
    options = disabled_full
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
    packages_to_enable = list()
    for iter in selected:
        if "(" in iter[0]:
            packages_to_enable.append(iter[0].split(" (")[0])

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

    """
    погнали...
    """
    for iter in packages_to_enable:
        cmd_enbl = f"{work_directory} -d shell pm enable --user 0 {iter}"
        enable = split(cmd_enbl)
        proc = Popen(enable, stdout=PIPE)
        output = proc.stdout.read()

        print(f"{iter} - {output.decode()}")
        proc.terminate()
