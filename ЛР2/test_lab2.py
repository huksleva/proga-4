"""
test_lab2.py

Набор тестов для проверки реализации паттерна Декоратор.
Покрывает базовый функционал и оба декоратора (YAML, CSV).
Соблюдает принцип DAST (Tests).
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import json
import csv

from main import CBRProvider, YamlDecorator, CsvDecorator


class TestCBRProvider(unittest.TestCase):
    """Тесты для базового компонента (CBRProvider)."""

    @patch("main.requests.get")
    def test_get_data_returns_dict(self, mock_get):
        """Тест 1: Проверка, что get_data возвращает словарь."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"Valute": {"USD": {"Value": 90.0}}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        provider = CBRProvider()

        # Act
        result = provider.get_data()

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("Valute", result)
        mock_get.assert_called_once()

    @patch("main.requests.get")
    def test_save_to_file_creates_json(self, mock_get):
        """Тест 2: Проверка сохранения файла в формате JSON."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"test_key": "test_value"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        provider = CBRProvider()
        filename = "test_rates.json"

        # Act
        provider.save_to_file(filename)

        # Assert
        self.assertTrue(os.path.exists(filename))
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["test_key"], "test_value")

        # Cleanup
        os.remove(filename)


class TestYamlDecorator(unittest.TestCase):
    """Тесты для декоратора YAML."""

    def test_get_data_returns_yaml_string(self):
        """Тест 3: Проверка, что декоратор возвращает строку YAML."""
        # Arrange
        mock_provider = MagicMock()
        mock_provider.get_data.return_value = {"currency": "USD", "value": 100}

        decorator = YamlDecorator(mock_provider)

        # Act
        result = decorator.get_data()

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn("currency: USD", result)
        self.assertIn("value: 100", result)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_to_file_writes_yaml(self, mock_file):
        """Тест 4: Проверка метода сохранения в YAML."""
        # Arrange
        mock_provider = MagicMock()
        mock_provider.get_data.return_value = {"key": "value"}

        decorator = YamlDecorator(mock_provider)
        filename = "test_output"

        # Act
        decorator.save_to_file(filename)

        # Assert
        # Проверяем, что open был вызван с именем файла + расширение
        # В реализации добавляется .yaml, если нет
        mock_file.assert_called_once_with("test_output.yaml", "w", encoding="utf-8")
        # Проверяем, что записанные данные содержат YAML формат
        handle = mock_file()
        handle.write.assert_called()
        written_content = handle.write.call_args[0][0]
        self.assertIn("key: value", written_content)


class TestCsvDecorator(unittest.TestCase):
    """Тесты для декоратора CSV."""

    def test_get_data_returns_csv_string(self):
        """Тест 5: Проверка, что декоратор возвращает строку CSV."""
        # Arrange
        mock_provider = MagicMock()
        # Имитация структуры JSON от ЦБ
        mock_provider.get_data.return_value = {
            "Valute": {
                "USD": {"CharCode": "USD", "Name": "Доллар", "Value": 90.0, "Nominal": 1},
                "EUR": {"CharCode": "EUR", "Name": "Евро", "Value": 98.0, "Nominal": 1}
            }
        }

        decorator = CsvDecorator(mock_provider)

        # Act
        result = decorator.get_data()

        # Assert
        self.assertIsInstance(result, str)
        self.assertIn("CharCode,Name,Value,Nominal", result)
        self.assertIn("USD,Доллар,90.0,1", result)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_to_file_writes_csv(self, mock_file):
        """Тест 6: Проверка метода сохранения в CSV."""
        # Arrange
        mock_provider = MagicMock()
        mock_provider.get_data.return_value = {
            "Valute": {
                "RUB": {"CharCode": "RUB", "Name": "Рубль", "Value": 1.0, "Nominal": 1}
            }
        }

        decorator = CsvDecorator(mock_provider)
        filename = "test_rates"

        # Act
        decorator.save_to_file(filename)

        # Assert
        mock_file.assert_called_once_with("test_rates.csv", "w", encoding="utf-8", newline="")
        handle = mock_file()
        handle.write.assert_called()
        written_content = handle.write.call_args[0][0]
        # Проверка валидности CSV через чтение строки
        lines = written_content.strip().split("\n")
        self.assertEqual(len(lines), 2)  # Заголовок + 1 строка данных
        reader = csv.DictReader(lines)
        rows = list(reader)
        self.assertEqual(rows[0]["CharCode"], "RUB")


if __name__ == "__main__":
    unittest.main()