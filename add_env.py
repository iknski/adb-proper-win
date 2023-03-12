import winreg
from time import sleep


HKCR = winreg.HKEY_CLASSES_ROOT
HKCC = winreg.HKEY_CURRENT_CONFIG
HKCU = winreg.HKEY_CURRENT_USER
HKLM = winreg.HKEY_LOCAL_MACHINE
HKU = winreg.HKEY_USERS


class RegistryKey:
    def __init__(self, root, path: str, access=winreg.KEY_ALL_ACCESS):
        self._root_key = winreg.ConnectRegistry(None, root)
        self._key = winreg.OpenKey(self._root_key, path, 0, access)

    def __enter__(self):
        return self

    def close(self):
        if hasattr(self, "_key") and self._key:
            winreg.CloseKey(self._key)
            self._key = None

        if hasattr(self, "_root_key") and self._root_key:
            winreg.CloseKey(self._root_key)
            self._root_key = None

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def __iter__(self):
        for i in range(1024):
            try:
                n, v, _ = winreg.EnumValue(self._key, i)
            except (OSError, EnvironmentError):
                break

            yield n, v

    def __getitem__(self, name: str):
        return winreg.QueryValueEx(self._key, name)[0]

    def __setitem__(self, name: str, value):
        value_type = winreg.QueryValueEx(self._key, name)[1]
        winreg.SetValueEx(self._key, name, 0, value_type, value)


def add_sys_env(env):
    with RegistryKey(HKCU, "Environment") as key:
        key["path"] = key["path"].rstrip(";") + ";" + env
        sleep(1)


if __name__ == "__main__":
    add_sys_env()
