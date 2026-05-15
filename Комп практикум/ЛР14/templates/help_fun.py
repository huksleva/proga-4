def find_email(str_list: list[str]) -> str:
    """
    Получает на вход массив строк, находит среди них email и возвращает его

    Args:
        str_list: Массив строк, где есть email

    Returns:
        Найденный email адрес. Если не найден, то возвращает пустую строку
    """

    for string in str_list:
        if string.find('@') != -1:
            return string

    return ""


def find_phone_number(str_list: list[str]) -> str:
    """
    Получает на вход массив строк, находит среди них телефонный номер и возвращает его

    Args:
        str_list: Массив строк, где есть телефонный номер

    Returns:
        Найденный телефонный номер. Если не найден, то возвращает пустую строку
    """

    for string in str_list:
        if string.find('+') != -1:
            return string

    return ""

def check_status_code(status_code: int) -> bool:
    """
    Обрабатывает статус коды

    Args:
        status_code (int): статус код (ответ от сервера)

    Returns:
        bool: True - если ок, False - если ошибка
    """

    if status_code == 200:
        print("OK")
        return True
    else:
        print("ERROR")
        print(status_code)
        return False


