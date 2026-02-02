def fibonacchi_gen():
    """Генератор чисел Фибоначи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res

g = fibonacchi_gen()

while True:
    h = next(g)
    if h > 10:
        break
    print(h)





class Fibonacchilst():
    def f(self):
        print()


# pep8 и pep257 и pep484- документация
"""
подсказки при вызове функции
:param instance

Генератор - создаёт новое значение
Итератор - получает на вход значение и перебирает его
"""



if __name__ == '__main__':
    n = 10
    Fibonacci = list(range(n))






