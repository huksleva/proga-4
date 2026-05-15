import scrapy


class TeachersSpider(scrapy.Spider):
    name = "teachers"

    allowed_domains = ["atlas.herzen.spb.ru"]

    start_urls = [
        f"https://atlas.herzen.spb.ru/teachers?page={page}"
        for page in range(1, 55)
    ]

    # ==========================================
    # Получаем список преподавателей
    # ==========================================

    def parse(self, response):

        table = response.css("table")

        rows = table.css("tbody tr")

        for row in rows:
            cells = row.css("td")

            fio = cells[0].css("a::text").get("").strip()

            profile_link = cells[0].css(
                "a::attr(href)"
            ).get()

            post = cells[1].css("::text").get("").strip()

            faculty = cells[2].css("::text").get("").strip()

            department = cells[3].css("::text").get("").strip()

            academic_degree = cells[4].css(
                "::text"
            ).get("").strip()

            yield response.follow(
                profile_link,
                callback=self.parse_profile,
                meta={
                    "fio": fio,
                    "profile_link": profile_link,
                    "post": post,
                    "faculty": faculty,
                    "department": department,
                    "academic_degree": academic_degree
                }
            )

    # ==========================================
    # Получаем профиль
    # ==========================================

    @staticmethod
    def parse_profile(response):

        h1_list = response.css(
            "h1.text-m::text"
        ).getall()

        email = ""
        phone_number = ""

        for string in h1_list:

            string = string.strip()

            if '@' in string:
                email = string

            if string.startswith(('+', '8')):
                phone_number = string

        yield {
            "ФИО": response.meta["fio"],
            "Ссылка_на_профиль": response.meta["profile_link"],
            "Должность": response.meta["post"],
            "Факультет/институт": response.meta["faculty"],
            "Кафедра": response.meta["department"],
            "Учёная_степень": response.meta["academic_degree"],
            "Почта": email,
            "Номер_телефона": phone_number
        }
