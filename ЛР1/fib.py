class fib_gen:
    """Класс-итератор чисел Фибоначи (обычная версия)"""
    def __init__(self):
        self.a = 0
        self.b = 1


    # Нужно, чтобы объект (класс) стал итератором, чтобы дальше мы смогли обращаться к нему как к итератору
    def __iter__(self):
        return self


    def __next__(self):
        a = self.a
        self.b += self.a
        self.a = self.b - self.a


        # 0 1 1 2 3 5
        """
        a b
        0 1
        1 1
        1 2
        2 3
        3 5
        """
        return a


class fib_gen_simplified:
    """Класс для доступа к числам Фибоначчи по индексу"""

    def __init__(self):
        self.sequence = [0, 1]  # Начальные значения

    def __getitem__(self, index):
        if index < 0:
            raise IndexError("Negative indices not supported")

        # Генерируем последовательность до нужного индекса
        while len(self.sequence) <= index:
            next_val = self.sequence[-1] + self.sequence[-2]
            self.sequence.append(next_val)

        return self.sequence[index]

    def __iter__(self):
        # Для поддержки итерации - используем генератор
        i = 0
        while True:
            yield self[i]
            i += 1

def fibonacchi_gen():
    """Генератор чисел Фибоначи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res

def fibonacchi_korutina():
    """Сопрограмма (корутина) чисел Фибоначи"""
    index = yield
    a = 0
    b = 1
    for _ in range(index):
        a, b = b, a + b
    yield a












# pep8 и pep257 и pep484- документация
"""
подсказки при вызове функции
:param instance
"""



if __name__ == '__main__':
    n = 10
    print("Числа фибоначи через итератор\n\nОбычный вариант:")
    x = fib_gen()
    for _ in range(n):
        print(next(x))

    print("\nУпрощённый вариант:")
    y = fib_gen_simplified()
    for i in range(n):
        print(y[i])

    print("\n\nЧисла фибоначи через генератор и сопрограмму:")
    print("\nГенератор:")
    g = fibonacchi_gen()
    for i in range(n):
        print(next(g))

    print("\nЧерез корутину:")

    for i in range(n):
        h = fibonacchi_korutina()
        next(h)
        print(h.send(i))




