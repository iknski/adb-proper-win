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
        index = 1
        print(
            f"-------------------------\n"
            f"{index}) To execute commands manually\n"
            f"{index + 1}) To uninstall apps\n"
            f"{index + 2}) To reinstall deleted apps\n"
            f"{index + 3}) To enable disabled apps\n"
            f"{index + 4}) To close and exit"
        )
        choice = int(input(f"Choose your option\n" f"Enter a number: >>> "))
        if choice == index:
            print(f"To finish enter: " + Fore.RED + "exit")
            print(f"-------------------------")
            phone_check()
            call([work_directory, "shell"])
        elif choice == index + 1:
            import uninstall
        elif choice == index + 2:
            import reinstall
        elif choice == index + 3:
            import disabled
        elif choice == index + 4:
            print(Fore.RED + f"Script is closed!")
            adb_terminate()
        break
    except (ValueError, IndexError):
        print(f"-------------------------")
        print(Fore.RED + f"incorrect input, try again...")
    except FileNotFoundError:
        print(f"-------------------------")
        print(Fore.RED + f"No such file: removed_apps.ini or file is empty")
