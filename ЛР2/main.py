"""
main.py

Реализация паттерна «Декоратор» для получения и конвертации курсов валют ЦБ РФ.
Базовый компонент получает данные в JSON, декораторы преобразуют их в YAML и CSV.
"""

import abc
import csv
import io
import json
from typing import Any, Dict, List, Optional

import requests
import yaml


class CurrencyProvider(abc.ABC):
    """
    Базовый интерфейс (ABC) для поставщиков данных о валюте.
    Определяет методы получения данных и сохранения в файл.
    """

    @abc.abstractmethod
    def get_data(self) -> Any:
        """
        Получает данные о курсах валют.

        Returns:
            Any: Данные в формате, определенном конкретной реализацией.
        """
        pass

    @abc.abstractmethod
    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет полученные данные в файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        pass


class CBRProvider(CurrencyProvider):
    """
    Конкретный компонент. Получает данные в формате JSON через API Центробанка.
    """

    URL = "https://www.cbr-xml-daily.ru/daily_json.js"

    def __init__(self) -> None:
        """Инициализация провайдера."""
        self._data: Optional[Dict[str, Any]] = None

    def get_data(self) -> Dict[str, Any]:
        """
        Загружает актуальные курсы валют с API ЦБ РФ.

        Returns:
            Dict[str, Any]: Словарь с данными в формате JSON.

        Raises:
            requests.RequestException: Если запрос к API не удался.
        """
        response = requests.get(self.URL)
        response.raise_for_status()
        self._data = response.json()
        return self._data

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в файл в формате JSON.

        Args:
            filename (str): Путь к файлу (например, 'rates.json').
        """
        data = self.get_data()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class CurrencyDecorator(CurrencyProvider):
    """
    Базовый класс декоратора. Хранит ссылку на объект CurrencyProvider.
    """

    _provider: CurrencyProvider

    def __init__(self, provider: CurrencyProvider) -> None:
        """
        Инициализация декоратора.

        Args:
            provider (CurrencyProvider): Обертываемый объект.
        """
        self._provider = provider

    def get_data(self) -> Any:
        """
        Делегирует получение данных обертываемому объекту.

        Returns:
            Any: Данные от провайдера.
        """
        return self._provider.get_data()

    def save_to_file(self, filename: str) -> None:
        """
        Делегирует сохранение данных обертываемому объекту.

        Args:
            filename (str): Имя файла.
        """
        self._provider.save_to_file(filename)


class YamlDecorator(CurrencyDecorator):
    """
    Конкретный декоратор. Преобразует данные в формат YAML.
    """

    def get_data(self) -> str:
        """
        Получает данные от провайдера и конвертирует их в YAML строку.

        Returns:
            str: Данные в формате YAML.
        """
        raw_data = self._provider.get_data()
        return yaml.dump(raw_data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в файл в формате YAML.
        Автоматически добавляет расширение .yaml, если его нет.

        Args:
            filename (str): Путь к файлу.
        """
        if not filename.endswith(".yaml") and not filename.endswith(".yml"):
            filename += ".yaml"

        yaml_data = self.get_data()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(yaml_data)


class CsvDecorator(CurrencyDecorator):
    """
    Конкретный декоратор. Преобразует данные в формат CSV.
    Извлекает только основную информацию о валютах (CharCode, Name, Value).
    """

    def _flatten_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Преобразует вложенную структуру JSON в плоский список для CSV.

        Args:
            data (Dict[str, Any]): Исходные данные JSON.

        Returns:
            List[Dict[str, Any]]: Список словарей для строк CSV.
        """
        rows = []
        valutes = data.get("Valute", {})
        for code, info in valutes.items():
            rows.append(
                {
                    "CharCode": info.get("CharCode", code),
                    "Name": info.get("Name", ""),
                    "Value": info.get("Value", 0),
                    "Nominal": info.get("Nominal", 1),
                }
            )
        return rows

    def get_data(self) -> str:
        """
        Получает данные и конвертирует их в CSV строку.

        Returns:
            str: Данные в формате CSV.
        """
        raw_data = self._provider.get_data()
        flat_data = self._flatten_data(raw_data)

        output = io.StringIO()
        if flat_data:
            fieldnames = flat_data[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_data)

        return output.getvalue()

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в файл в формате CSV.
        Автоматически добавляет расширение .csv, если его нет.

        Args:
            filename (str): Путь к файлу.
        """
        if not filename.endswith(".csv"):
            filename += ".csv"

        csv_data = self.get_data()
        with open(filename, "w", encoding="utf-8", newline="") as f:
            f.write(csv_data)


def client_code(provider: CurrencyProvider) -> None:
    """
    Клиентский код работает с объектами через интерфейс CurrencyProvider.

    Args:
        provider (CurrencyProvider): Объект поставщика данных.
    """
    print(f"Получение данных через {provider.__class__.__name__}...")
    data = provider.get_data()
    print(f"Тип данных: {type(data).__name__}")
    if isinstance(data, str):
        print(f"Предпросмотр (100 символов): {data[:100]}...")
    elif isinstance(data, dict):
        print(f"Ключи верхнего уровня: {list(data.keys())}")
    print("-" * 40)


if __name__ == "__main__":
    # 1. Базовый компонент (JSON)
    simple_provider = CBRProvider()
    client_code(simple_provider)
    simple_provider.save_to_file("rates.json")
    print("Файл rates.json сохранен.\n")

    # 2. Декоратор YAML
    yaml_provider = YamlDecorator(CBRProvider())
    client_code(yaml_provider)
    yaml_provider.save_to_file("rates.yaml")
    print("Файл rates.yaml сохранен.\n")

    # 3. Декоратор CSV
    csv_provider = CsvDecorator(CBRProvider())
    client_code(csv_provider)
    csv_provider.save_to_file("rates.csv")
    print("Файл rates.csv сохранен.\n")

    # 4. Цепочка декораторов (пример: можно получить JSON, но сохранить через CSV декоратор)
    # В данном контексте обычно декорируют источник, чтобы изменить формат вывода.
    chained_provider = YamlDecorator(CsvDecorator(CBRProvider()))
    # Примечание: порядок важен. Внутренний CSV превратит dict в строку CSV,
    # внешний YAML попытается дампить строку. Это демонстрирует гибкость,
    # но для бизнес-логики обычно используют один декоратор формата.