from subprocess import Popen, PIPE


"""
получение списка установленных приложений
"""
installed_packages = None
if installed_packages is None:
    installed_packages = []

disabled_packages = None
if disabled_packages is None:
    disabled_packages = []

with open("work_directory.ini", mode="r", encoding="UTF-8") as ini_file:
    work_directory = ini_file.readline().strip()

proc = Popen(work_directory + " shell pm list packages", shell=False, stdout=PIPE)

with proc.stdout:
    for line in iter(proc.stdout.readline, b""):
        installed_packages.append(line.decode().strip()[8:])
proc.terminate()

proc = Popen(work_directory + " shell pm list packages -d", shell=False, stdout=PIPE)

with proc.stdout:
    for line in iter(proc.stdout.readline, b""):
        disabled_packages.append(line.decode().strip()[8:])
proc.terminate()

disabled = list(filter(lambda it: it in installed_packages, disabled_packages))
