import requests
from bs4 import BeautifulSoup
from templates.help_fun import check_status_code, find_email, find_phone_number

# Добавляем User-Agent
# Некоторые сайты блокируют запросы без заголовков.
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Начинаем
for page in range(1, 55):
    url = "https://atlas.herzen.spb.ru/teachers?page=" + str(page)
    print(f"Обрабатывается страница {url}")

    # 1. Получаем HTML
    response = requests.get(url, headers=headers)
    check_status_code(response.status_code)

    # 2. Создаём объект BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. Ищем данные
    table = soup.find("table")

    # Получаем заголовки таблицы
    head = table.find("thead").find("tr")

    # Получаем все строки таблицы без заголовка
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        # Получаем ячейки из строки
        cells = row.find_all("td")

        # Получаем данные из каждой ячейки
        FIO = cells[0].text.strip()
        profile_link = cells[0].find("a")["href"]
        print(f"Обрабатывается страница {profile_link}")
        post = cells[1].text.strip()
        faculty = cells[2].text.strip()
        department = cells[3].text.strip()
        academic_degree = cells[4].text.strip()


        # Со страницы профиля получаем: почту и телефон (при наличии)
        profile_response = requests.get(str(profile_link), headers=headers)
        check_status_code(profile_response.status_code)
        profile_soup = BeautifulSoup(profile_response.text, "html.parser")

        # Получаем список всех h1
        h1_list = [
            h1.get_text(strip=True)
            for h1 in profile_soup.find_all("h1", class_="text-m")
        ]

        # Ищем email
        email = find_email(h1_list)

        # Ищем телефонный номер
        phone_number = find_phone_number(h1_list)

        print(email, phone_number, sep="===", end="|||\n")
    
