import math

def golden(a, b, f, iterations):
    phi = (5 ** 0.5 - 1) / 2
    print(phi)
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    for _ in range(iterations):
        if f(c) < f(d):
            b = d
        else:
            a = c
        c = b - phi * (b - a)
        d = a + phi * (b - a)
        print(f"({a:.2f}, {b:.2f}, {c:.2f}, {d:.2f})")


golden(0, 2*math.pi, lambda x: math.sin(x), 10)