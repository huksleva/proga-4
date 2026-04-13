import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

# URL API ЦБ РФ (возвращает курсы валют в формате XML)
CBR_XML_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


class CBRFService:
    """Сервис для получения курсов валют с сайта ЦБ РФ"""

    @staticmethod
    async def fetch_currencies_xml() -> Optional[str]:
        """Асинхронно скачивает XML с курсами валют"""
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(CBR_XML_URL)
                response.raise_for_status()  # Выбросит ошибку при 4xx/5xx
                return response.text
        except httpx.HTTPError as e:
            print(f"Ошибка HTTP при запросе к ЦБ: {e}")
            return None
        except Exception as e:
            print(f"Ошибка сети при запросе к ЦБ: {e}")
            return None

    @staticmethod
    def parse_currencies_xml(xml_content: str) -> list[dict]:
        """Парсит XML ЦБ РФ и возвращает список словарей с валютами"""

        try:
            root = ET.fromstring(xml_content)
            currencies = []

            # Каждая валюта находится в теге <Valute>
            for valute in root.findall('Valute'):
                # Извлекаем значение
                value_str = valute.findtext('Value', default='0').replace(',', '.')

                # Конвертируем в float сразу
                try:
                    value = float(value_str)
                except ValueError:
                    value = 0.0

                currency = {
                    'char_code': valute.findtext('CharCode', default=''),
                    'num_code': valute.findtext('NumCode', default=''),
                    'name': valute.findtext('Name', default=''),
                    'nominal': int(valute.findtext('Nominal', default='1')),
                    'value': value,  # Сразу float
                    'date': datetime.now().strftime("%d:%m:%Y %H:%M")
                }

                currencies.append(currency)

            return currencies

        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
            return []
        except Exception as e:
            print(f"Ошибка при обработке данных ЦБ: {e}")
            return []

    @staticmethod
    async def get_currencies() -> list[dict]:
        """Основной метод: скачивает и парсит курсы валют"""

        xml = await CBRFService.fetch_currencies_xml()
        if not xml:
            return []
        return CBRFService.parse_currencies_xml(xml)

