from subprocess import Popen, PIPE
from comparing_positions import compare_position
from shlex import split
from main import phone_check
from app_list import disabled
from colorama import init, Fore
from pick import pick


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
сравниваем списки установленных пакетов c черным списком
"""
differences_pkg = list(filter(lambda it: it in installed_packages, check_list_packages))

"""
если есть отключенные пакеты удаляем их из подготаавливаемого списка
"""
for iter in differences_pkg:
    if iter in disabled:
        differences_pkg.remove(iter)

"""
формируем список имён пакетов - понадобится для лучшего понимания, что мы будем удалять
"""
differences_nm = compare_position(differences_pkg)

"""
если сравниваемый список пуст, это здорово
"""
if len(differences_pkg) == 0:
    exit(Fore.GREEN + f"Your phone is in optimal condition\nNo apps to remove...")

"""
добавляем имена к пакетам для удобства
"""
differences_full = list()
index = 0
for iter in differences_nm:
    differences_full.append(f"{differences_pkg[index]} ({differences_nm[index]})")
    index = index + 1

"""
формируем меню для выбора удаляемых приложений
"""
title = (
    "Application's for removing...\nTap Space key for chose\n-------------------------"
)
options = differences_full
selected = pick(
    options,
    title,
    indicator="> ",
    multiselect=True,
    min_selection_count=1,
)

print(f"Your choice: \n-------------------------")

"""
формируем список для удаления
отрезаем лишнее из элементов списка, иначе будет ошибка удаления
для ADB нам нужно лишь имя пакета
"""
pkgs_to_remove = list()
for iter in selected:
    if "(" in iter[0]:
        pkgs_to_remove.append(iter[0].split(" (")[0])

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
