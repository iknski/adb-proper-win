from subprocess import call
from main import phone_check, adb_terminate
from colorama import init, Fore


"""
узнаем что хочет сделать пользователь
"""
init(autoreset=True)


with open("work_directory.ini", mode="r", encoding="UTF-8") as wd_ini_file:
    work_directory = wd_ini_file.readline().strip()
    work_directory = work_directory.replace("\\", "/")

while True:
    try:
        print(
            f"-------------------------\n"
            f"1) To execute commands manually\n"
            f"2) To uninstall apps manually\n"
            f"3) To uninstall apps via list_to_remove.txt\n"
            f"4) To reinstall deleted apps\n"
            f"5) To enable disabled apps\n"
            f"6) To close and exit"
        )
        choice = int(input(f"Choose your option\n" f"Enter a number: >>> "))
        match choice:
            case 1:
                print(f"To finish enter: " + Fore.RED + "exit")
                print(f"-------------------------")
                phone_check()
                call([work_directory, "shell"])
            case 2:
                import uninstall
            case 3:
                import list_remover
            case 4:
                import reinstall
            case 5:
                import disabled
            case 6:
                print(Fore.RED + f"Script is closed!")
                adb_terminate()
        break

    except (ValueError, IndexError):
        print(f"-------------------------")
        print(Fore.RED + f"incorrect input, try again...")
    except FileNotFoundError:
        print(f"-------------------------")
        print(Fore.RED + f"No such file or file is empty")
