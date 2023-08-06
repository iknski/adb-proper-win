from subprocess import call
from main import phone_check, adb_terminate
from colorama import init, Fore
from pick import pick


"""
узнаем что хочет сделать пользователь
"""
init(autoreset=True)


with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

title = "Choose your option: \n-------------------------"
options = [
    "To execute commands manually",
    "To uninstall apps manually",
    "To uninstall apps via list_to_remove.txt",
    "To reinstall deleted apps",
    "To enable disabled apps",
    "To close and exit",
]
option, index = pick(options, title, indicator="> ")
match index:
    case 0:
        print(f"To finish enter: " + Fore.RED + "exit")
        print(f"-------------------------")
        phone_check()
        call([work_directory, "shell"])
    case 1:
        import uninstall
    case 2:
        import list_remover
    case 3:
        import reinstall
    case 4:
        import disabled
    case 5:
        print(Fore.RED + f"Script is closed!")
        adb_terminate()
