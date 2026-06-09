# Задание по SOLID

## Принцип единственной ответственности (SRP — Single Responsibility Principle)

### Нарушение принципа

Рассмотрим пример из предметной области интернет-магазина.

Есть класс `Order`, который:

- хранит данные заказа;
    
- рассчитывает стоимость;
    
- сохраняет заказ в файл;
    
- отправляет сообщение клиенту.
    

```
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["count"]
        return total

    def save_to_file(self):
        with open("orders.txt", "a", encoding="utf-8") as file:
            file.write(str(self.items) + "\n")

    def send_email(self):
        print("Письмо клиенту отправлено")
```

---

## Почему здесь нарушен SRP

Принцип SRP говорит о том, что класс должен иметь только одну причину для изменения.

В данном примере класс `Order` выполняет сразу несколько задач:

1. Работает с данными заказа.
    
2. Выполняет расчёты.
    
3. Сохраняет данные в файл.
    
4. Отправляет уведомления.
    

Если изменится способ хранения данных или способ отправки сообщений, придётся изменять класс `Order`, хотя логика заказа может остаться прежней.

Это делает код:

- менее гибким;
    
- сложным для поддержки;
    
- трудным для тестирования.
    

---

# Исправление нарушения

Разделим обязанности между разными классами.

```
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["count"]
        return total


class OrderStorage:
    def save_to_file(self, order):
        with open("orders.txt", "a", encoding="utf-8") as file:
            file.write(str(order.items) + "\n")


class EmailService:
    def send_email(self):
        print("Письмо клиенту отправлено")
```

---

# Комментарий к исправлению

После исправления:

- класс `Order` отвечает только за данные заказа и расчёт стоимости;
    
- класс `OrderStorage` отвечает только за сохранение;
    
- класс `EmailService` отвечает только за отправку уведомлений.
    

Теперь каждый класс выполняет одну задачу, что соответствует принципу SRP.

Преимущества такого подхода:

- код легче изменять;
    
- проще тестировать;
    
- удобнее расширять функциональность;
    
- уменьшается количество ошибок при изменениях.