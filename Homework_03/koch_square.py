import turtle as t

def fractal(n, L):
    if n == 0:
        t.forward(L)
    else:
        fractal(n-1, L/3)
        t.left(90)
        fractal(n-1, L/3)
        t.right(90)
        fractal(n-1, L/3)
        t.right(90)
        fractal(n-1, L/3)
        t.left(90)
        fractal (n-1, L/3)

fractal(4, 300)
t.right(90)
fractal(4, 300)
t.right(90)
fractal(4, 300)
t.right(90)
fractal(4, 300)

t.done()