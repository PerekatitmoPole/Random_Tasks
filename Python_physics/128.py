import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Функция для построения статической траектории
def plot_static(radius, velocity):
    R = radius
    t = np.linspace(0, 4 * np.pi, 500)

    # Уравнение циклоиды
    x = R * (t - np.sin(t))
    y = R * (1 - np.cos(t))

    plt.figure(figsize=(12, 6))
    plt.plot(x, y, label='Траектория точки на ободе (циклоид)')
    plt.title('Траектория точки на ободе колеса (Циклоид)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)

    # Подбор границ графика
    plt.xlim([0, max(x) + R])
    plt.ylim([min(y) - R, max(y) + R])

    plt.legend()
    plt.show()

# Функция для получения данных из GUI
def get_inputs():
    try:
        radius = float(entry_radius.get())
        velocity = float(entry_velocity.get())

        if radius <= 0 or velocity <= 0:
            raise ValueError

        plot_static(radius, velocity)

    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для радиуса и скорости!")

# Создание окна GUI
root = tk.Tk()
root.title("Визуализация движения точки на ободе колеса")

# Метки и поля ввода для радиуса и скорости
label_radius = tk.Label(root, text="Радиус колеса:")
label_radius.grid(row=0, column=0, padx=10, pady=10)

entry_radius = tk.Entry(root)
entry_radius.grid(row=0, column=1, padx=10, pady=10)

label_velocity = tk.Label(root, text="Скорость центра масс:")
label_velocity.grid(row=1, column=0, padx=10, pady=10)

entry_velocity = tk.Entry(root)
entry_velocity.grid(row=1, column=1, padx=10, pady=10)

# Кнопка для запуска визуализации
btn_visualize = tk.Button(root, text="Построить", command=get_inputs)
btn_visualize.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Запуск окна
root.mainloop()
