from colorama import init, Fore
from sys import exit
from webbrowser import open_new


"""
если файл "adb.exe" не найден
"""
init(autoreset=True)

print(f"ADB is not installed! Please download, install it and try again")

download_url = "https://developer.android.com/studio/releases/platform-tools"

answer_1 = input(f"Do you want to download?\n" f"Y/N: > ").upper()
if answer_1 == "Y":
    open_new(download_url)
    exit(Fore.RED + f"Script is closed!")
else:
    print("OK, I'll be waiting for you next time...")
    exit(Fore.RED + f"Script is closed!")
