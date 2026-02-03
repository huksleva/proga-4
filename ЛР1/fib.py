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
    """Класс-итератор чисел Фибоначи (упрощённая версия через __getitem__)"""

    def __init__(self):
        self.a = 0
        self.b = 1
        self.sequence = list()


    # Нужно, чтобы объект (класс) стал итератором, чтобы дальше мы смогли обращаться к нему как к итератору
    def __iter__(self):
        return self

    def __getitem__(self, index):
        while index >= len(self.sequence):
            self.sequence.append(self.a)
            self.b += self.a
            self.a = self.b - self.a
        return self.sequence[index]




def fibonacchi_gen():
    """Генератор чисел Фибоначи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res













# pep8 и pep257 и pep484- документация
"""
подсказки при вызове функции
:param instance
"""



if __name__ == '__main__':
    print("Числа фибоначи через итератор\n\nОбычный вариант:")
    x = fib_gen()
    for _ in range(10):
        print(next(x))

    print("\nУпрощённый вариант:")
    y = fib_gen_simplified()
    for i in range(10):
        print(y[i])









