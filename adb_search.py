from colorama import init, Fore
from os import path, walk
from win32api import GetLogicalDriveStrings
from time import time


"""
Ищем файл "adb.exe" на локальных дисках и формируем список, если найдены несколько копий программы
"""
init(autoreset=True)


def _searching(the_file: str, the_path: str) -> list:
    result = None
    if result is None:
        result = []
    for root, dirs, files in walk(the_path):
        if root.startswith(path.join(the_path, "$Recycle")):  # пропуск корзины
            continue
        if the_file in files:
            result.append(path.join(root, the_file))
    return result


win_drives = GetLogicalDriveStrings().split("\x00")[:-1]

found = None
if found is None:
    found = []

index = 0
quantity_drives = len(win_drives)
timer = time()

while index <= len(win_drives) - 1:
    drive = win_drives.pop(index)
    found.append(_searching("adb.exe", drive))
    index = index

adb_found = None
if adb_found is None:
    adb_found = []

for next_list in found:
    adb_found += next_list

print(f"-------------------------\n"
    f"{Fore.GREEN}found in %.3f seconds\n"
    f"{quantity_drives} drives scanned" % (time() - timer)
)
