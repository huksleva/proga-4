import unittest
from fib import fib_gen, fib_gen_simplified, fibonacchi_gen, fibonacchi_korutina


class TestFibonacciImplementations(unittest.TestCase):
    """Тесты для всех реализаций чисел Фибоначчи."""

    def setUp(self):
        """Подготовка ожидаемой последовательности Фибоначчи."""
        self.expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
        self.test_length = len(self.expected)

    def test_fib_gen_class(self):
        """Тест класса-итератора fib_gen."""
        fib_iter = fib_gen()
        result = [next(fib_iter) for _ in range(self.test_length)]
        self.assertEqual(result, self.expected)

    def test_fib_gen_simplified_class(self):
        """Тест упрощённого класса fib_gen_simplified."""
        fib_obj = fib_gen_simplified()
        result_indexed = [fib_obj[i] for i in range(self.test_length)]
        self.assertEqual(result_indexed, self.expected)

    def test_fibonacchi_gen_function(self):
        """Тест генераторной функции fibonacchi_gen."""
        fib_gen_func = fibonacchi_gen()
        result = [next(fib_gen_func) for _ in range(self.test_length)]
        self.assertEqual(result, self.expected)

    def test_fibonacchi_korutina_function(self):
        """Тест сопрограммы fibonacchi_korutina."""
        for i in range(self.test_length):
            coro = fibonacchi_korutina()
            next(coro)
            result = coro.send(i)
            self.assertEqual(result, self.expected[i])

    def test_edge_cases(self):
        """Тест граничных случаев."""
        # Тест для индекса 0
        self.assertEqual(next(fib_gen()), 0)
        self.assertEqual(fib_gen_simplified()[0], 0)
        self.assertEqual(next(fibonacchi_gen()), 0)

        coro_0 = fibonacchi_korutina()
        next(coro_0)
        self.assertEqual(coro_0.send(0), 0)

        # Тест для индекса 1
        fib_iter = fib_gen()
        next(fib_iter)
        self.assertEqual(next(fib_iter), 1)

        self.assertEqual(fib_gen_simplified()[1], 1)

        fib_gen_func = fibonacchi_gen()
        next(fib_gen_func)
        self.assertEqual(next(fib_gen_func), 1)

        coro_1 = fibonacchi_korutina()
        next(coro_1)
        self.assertEqual(coro_1.send(1), 1)

    def test_consistency_across_implementations(self):
        """Тест согласованности всех реализаций между собой."""
        n = 15

        # Создаём ОДИН экземпляр каждого типа
        fib_iter = fib_gen()
        result1 = [next(fib_iter) for _ in range(n)]

        fib_simpl = fib_gen_simplified()
        result2 = [fib_simpl[i] for i in range(n)]

        fib_gen_func = fibonacchi_gen()
        result3 = [next(fib_gen_func) for _ in range(n)]

        result4 = []
        for i in range(n):
            coro = fibonacchi_korutina()
            next(coro)
            result4.append(coro.send(i))

        expected_n = self.expected[:n]
        self.assertEqual(result1, expected_n)
        self.assertEqual(result2, expected_n)
        self.assertEqual(result3, expected_n)
        self.assertEqual(result4, expected_n)


if __name__ == '__main__':
    unittest.main()