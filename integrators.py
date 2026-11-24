"""Модуль реалізації класів чисельного інтегрування."""


class BaseIntegrator:
    """Базовий клас для чисельного обчислення визначених інтегралів."""

    order = 1
    method_name = "Базовий метод"

    def __init__(self, func, a, b):
        """Ініціалізує підінтегральну функцію та межі інтегрування."""
        if not self.validate_bounds(a, b):
            raise ValueError(f"Нижня межа ({a}) має бути строго меншою за верхню ({b})")
        self.func=func
        self.a=float(a)
        self.b=float(b)

    @classmethod
    def from_dict(cls, func, params):
        """Альтернативний конструктор для створення інтегратора зі словника."""
        if "a" not in params or "b" not in params:
            raise KeyError("Словник параметрів не місти ключ 'a' чи 'b' ")
        return cls(func, params["a"], params["b"])

    @staticmethod
    def validate_bounds(a, b):
        """Перевіряє коректність меж інтегрування."""
        return a<b

    def integrate(self, n):
        """Обчислює наближене значення інтеграла для n розбиттів."""
        raise NotImplementedError

    def adaptive_integrate(self, eps=1e-4, initial_n=2):
        """Знаходить інтеграл із заданою точністю eps за правилом Рунге."""
        if eps<=0:
            raise ValueError("Точність (eps) має бути додатним числом")
        if initial_n<2 or initial_n%2!=0: 
            raise ValueError("Початкове розбиття (initial_n) має бути парним числом")
        n=initial_n
        i_prev=self.integrate(n)
        denominator=(2**self.order)-1
        while True:
            n*=2
            i_curr=self.integrate(n)
            error=abs(i_curr-i_prev)/denominator
            if error<eps:
                i_refined=i_curr+(i_curr-i_prev)/denominator
                return i_refined, n, error
            i_prev=i_curr
            

    def __str__(self):
        """Повертає рядкове представлення об'єкта інтегратора."""
        return(f"{self.method_name} на відрізку [{self.a}; {self.b}]" f"(порядок точності O(h^{self.order}))")


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h=(self.b-self.a)/n
        total=sum(self.func(self.a+(i+0.5)*h) for i in range(n))
        return h*total


class TrapezoidIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою трапецій."""

    order = 2
    method_name = "Формула трапецій"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h=(self.b-self.a)/n
        endpoints=0.5*(self.func(self.a)+self.func(self.b))
        middle=sum(self.func(self.a+i*h) for i in range(1,n))
        return h*(endpoints+middle)


class SimpsonIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою Сімпсона."""

    order = 4
    method_name = "Формула Сімпсона"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        h=(self.b-self.a)/n
        odd_sum=sum(self.func(self.a+i*h) for i in range(1,n,2)) 
        even_sum=sum(self.func(self.a+i*h) for i in range(2,n-1,2))
        return (h/3)*(self.func(self.a) + self.func(self.a)+4*odd_sum+2*even_sum)
