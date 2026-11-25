"""Головний модуль запуску чисельного інтегрування."""

import math

from integrators import (
    RectangleIntegrator,
    SimpsonIntegrator,
    TrapezoidIntegrator,
)


def target_function(x):
    """Підінтегральна функція згідно з індивідуальним варіантом."""
    return math.exp(math.sin(x))


def main():
    """Точка входу програми."""
    bounds={"a":0, "b":1}
    integratorz=[RectangleIntegrator.from_dict(target_function, bounds),
                TrapezoidIntegrator.from_dict(target_function, bounds),
                 SimpsonIntegrator.from_dict(target_function, bounds)]
    for eps in (0.0002, 0.00002):
        print(f"Точність = {eps} \n")
        for integrator in integratorz:
            print(integrator)
            res, n_min, err=integrator.adaptive_integrate(eps=eps)
            print(f"Уточнений результат: {res:.7f} (n_min = {n_min}, похибка ≈ {err:.2e})\n")

if __name__ == "__main__":
    main()
