from rm_list_pkgs import check_list_packages
from rm_list_nms import check_list_names

position = None
if position is None:
    position = []

names = None
if names is None:
    names = []


def compare_position(comparison_list: list) -> list:

    """
    находим номера позиций списка "comparison_list" в списке "check_list_packages"
    """
    for iter in comparison_list or check_list_packages:
        if not iter in check_list_packages:
            continue
        elif iter:
            position.append(check_list_packages.index(iter))

    """
    находим имена пакетов из списка "comparison_list" - будут нужны для вывода
    """
    for iter in position:
        name = check_list_names[iter]
        names.append(name)
    return names
