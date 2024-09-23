import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np


# Функция для расчета траектории
def calculate_trajectory(v0, angle_deg, height):
    g = 9.81  # ускорение свободного падения, м/с²
    angle_rad = np.radians(angle_deg)  # угол в радианах

    # Время до достижения максимальной высоты
    t_flight = (v0 * np.sin(angle_rad) + np.sqrt((v0 * np.sin(angle_rad)) ** 2 + 2 * g * height)) / g

    # Время
    t = np.linspace(0, t_flight, num=500)

    # Координаты движения
    x = v0 * t * np.cos(angle_rad)
    y = height + v0 * t * np.sin(angle_rad) - 0.5 * g * t ** 2

    # Ускорение и скорость
    vx = np.full_like(t, v0 * np.cos(angle_rad))
    vy = v0 * np.sin(angle_rad) - g * t
    v = np.sqrt(vx ** 2 + vy ** 2)

    return t, x, y, vx, vy, v


# Функция для построения графиков
def plot_trajectory(v0, angle_deg, height):
    t, x, y, vx, vy, v = calculate_trajectory(v0, angle_deg, height)

    # Создание графиков
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # График траектории
    axs[0, 0].plot(x, y)
    axs[0, 0].set_title("Траектория движения")
    axs[0, 0].set_xlabel("Расстояние, м")
    axs[0, 0].set_ylabel("Высота, м")

    # График скорости
    axs[0, 1].plot(t, v)
    axs[0, 1].set_title("Зависимость скорости от времени")
    axs[0, 1].set_xlabel("Время, с")
    axs[0, 1].set_ylabel("Скорость, м/с")

    # График координаты x от времени
    axs[1, 0].plot(t, x)
    axs[1, 0].set_title("Координата x от времени")
    axs[1, 0].set_xlabel("Время, с")
    axs[1, 0].set_ylabel("x, м")

    # График координаты y от времени
    axs[1, 1].plot(t, y)
    axs[1, 1].set_title("Координата y от времени")
    axs[1, 1].set_xlabel("Время, с")
    axs[1, 1].set_ylabel("y, м")

    plt.tight_layout()
    plt.show()


# Функция для обработки нажатия кнопки
def on_calculate():
    try:
        # Получение значений
        v0 = float(velocity_entry.get())
        angle = float(angle_entry.get())
        height = float(height_entry.get())

        # Построение графиков
        plot_trajectory(v0, angle, height)

    except ValueError:
        result_label.config(text="Пожалуйста, введите числовые значения.")


# Создание окна
root = tk.Tk()
root.title("Баллистическое движение")

# Добавление полей ввода
ttk.Label(root, text="Начальная скорость (м/с):").grid(row=0, column=0, padx=10, pady=5)
velocity_entry = ttk.Entry(root)
velocity_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Угол броска (градусы):").grid(row=1, column=0, padx=10, pady=5)
angle_entry = ttk.Entry(root)
angle_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Высота броска (м):").grid(row=2, column=0, padx=10, pady=5)
height_entry = ttk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=5)

# Кнопка для расчета
calculate_button = ttk.Button(root, text="Рассчитать", command=on_calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Место для вывода результатов
result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Запуск программы
root.mainloop()
