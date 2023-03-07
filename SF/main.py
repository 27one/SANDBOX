import numpy as np
from sympy import Symbol, lambdify
import torch

# x  = Symbol('x')
# y = x**3 + 1

# yprime = y.diff(x)

# f = lambdify(x, yprime, 'numpy')

# print(f(np.array([1,2,3])))

x = torch.ones(2, 2, requires_grad=True)
y = x + 2
z = y* y *3

out = z.mean()

print(x.grad)