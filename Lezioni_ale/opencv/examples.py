import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 400)
f = x**3 - 3*x
f_prime = 3*x**2 - 3
f_double_prime = 6*x

plt.figure(figsize=(12, 8))

# Funzione originale
plt.subplot(3, 1, 1)
plt.plot(x, f, label='f(x) = x^3 - 3x')
plt.title('Funzione originale')
plt.grid(True)
plt.legend()

# Derivata prima
plt.subplot(3, 1, 2)
plt.plot(x, f_prime, color='orange', label="f'(x) = 3x^2 - 3")
plt.title('Derivata prima')
plt.grid(True)
plt.legend()

# Derivata seconda
plt.subplot(3, 1, 3)
plt.plot(x, f_double_prime, color='green', label="f''(x) = 6x")
plt.title('Derivata seconda')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
