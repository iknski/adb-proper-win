from re import findall
from subprocess import Popen, PIPE
from rm_list_pkgs import check_list_packages
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
формируем список имён пакетов - понадобится для лучшего понимания, что мы будем удалять
"""
disabled_nm = compare_position(disabled_packages)

"""
добавляем имена к пакетам для удобства
"""
disabled_full = list()
index = 0
for iter in disabled_nm:
    disabled_full.append(f"{disabled_packages[index]} ({disabled_nm[index]})")
    index = index + 1

"""
формируем меню для выбора приложений
"""
title = "Disabled apps...\nTap Space key for chose\n-------------------------"
options = disabled_full
selected = pick(
    options,
    title,
    indicator="> ",
    multiselect=True,
    min_selection_count=1,
)

print(f"Your choice: \n-------------------------")

"""
формируем список для включения
отрезаем лишнее из элементов списка, иначе будет ошибка
для ADB нам нужно лишь имя пакета
"""
pkgs_to_enable = list()
for iter in selected:
    if "(" in iter[0]:
        pkgs_to_enable.append(iter[0].split(" (")[0])

"""
часть ниже нужна лишь для того чтобы увидеть что мы будем удалять перед подтверждением
"""
_list = list()
for list in selected:
    for iter in list:
        _list.append(iter)
        selected_pkgs = _list[0::2]

index = 0
for iter in selected_pkgs:
    out = f"{index + 1}) {iter}"
    index = index + 1
    print(out)
print(f"-------------------------")
input("Press Enter to confirm...")

"""
погнали...
"""
for iter in pkgs_to_enable:
    cmd_enbl = f"{work_directory} -d shell pm enable --user 0 {iter}"
    enable = split(cmd_enbl)
    proc = Popen(enable, stdout=PIPE)
    output = proc.stdout.read()

    print(f"{iter} - {output.decode()}")
    proc.terminate()
