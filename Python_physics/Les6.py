import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import messagebox

# Включаем интерактивный режим
plt.ion()

# Функция для моделирования движения тела
def projectile_motion(v0, angle_deg, h, k):
    # Константы
    g = 9.81  # Ускорение свободного падения (м/с^2)
    m = 1.0   # Масса тела (кг), условно равна 1 для упрощения

    # Угол переведен в радианы
    angle_rad = np.radians(angle_deg)

    # Компоненты начальной скорости
    vx0 = v0 * np.cos(angle_rad)
    vy0 = v0 * np.sin(angle_rad)

    # Система дифференциальных уравнений
    def equations(t, y):
        x, y_pos, vx, vy = y
        dvx_dt = -k * vx / m
        dvy_dt = -g - k * vy / m
        return [vx, vy, dvx_dt, dvy_dt]

    # Вектор начальных условий
    y0 = [0, h, vx0, vy0]

    # Временной интервал для расчета
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 500)

    # Решаем систему с использованием метода Рунге-Кутты 4-го порядка
    sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, method='RK45')

    # Извлекаем решения
    x = sol.y[0]
    y = sol.y[1]
    vx = sol.y[2]
    vy = sol.y[3]
    t = sol.t

    # Оставляем только те значения, где тело еще не достигло земли
    ground_idx = np.where(y >= 0)[0]
    x, y, vx, vy, t = x[ground_idx], y[ground_idx], vx[ground_idx], vy[ground_idx], t[ground_idx]

    # Построение графиков
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Траектория
    axs[0].plot(x, y, label="Траектория", color="blue")
    axs[0].set_title("Траектория движения тела", fontsize=14, fontweight='bold', pad=15)
    axs[0].set_xlabel("Горизонтальное расстояние (м)", fontsize=12)
    axs[0].set_ylabel("Вертикальное расстояние (м)", fontsize=12)
    axs[0].grid(True)

    # Скорость от времени
    axs[1].plot(t, np.sqrt(vx**2 + vy**2), label="Скорость", color="green")
    axs[1].set_title("Скорость тела со временем", fontsize=14, fontweight='bold', pad=15)
    axs[1].set_xlabel("Время (с)", fontsize=12)
    axs[1].set_ylabel("Скорость (м/с)", fontsize=12)
    axs[1].grid(True)

    # Положение по осям от времени
    axs[2].plot(t, x, label="Горизонтальное положение", color="orange")
    axs[2].plot(t, y, label="Вертикальное положение", color="purple")
    axs[2].set_title("Положение тела со временем", fontsize=14, fontweight='bold', pad=15)
    axs[2].set_xlabel("Время (с)", fontsize=12)
    axs[2].set_ylabel("Положение (м)", fontsize=12)
    axs[2].legend()
    axs[2].grid(True)

    # Настройка интервалов между графиками
    plt.tight_layout(pad=5.0)
    fig.canvas.draw()
    fig.canvas.flush_events()

# Функция для обработки нажатия кнопки и запуска моделирования
def start_simulation():
    try:
        v0 = float(entry_velocity.get())
        angle_deg = float(entry_angle.get())
        h = float(entry_height.get())
        k = float(entry_resistance.get())
        projectile_motion(v0, angle_deg, h, k)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения.")

# Создание окна с полями ввода
root = tk.Tk()
root.title("Моделирование движения тела под углом")

# Поля для ввода параметров
tk.Label(root, text="Начальная скорость (м/с):").grid(row=0, column=0, padx=10, pady=5)
entry_velocity = tk.Entry(root)
entry_velocity.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Угол броска (градусы):").grid(row=1, column=0, padx=10, pady=5)
entry_angle = tk.Entry(root)
entry_angle.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Начальная высота (м):").grid(row=2, column=0, padx=10, pady=5)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Коэффициент сопротивления k:").grid(row=3, column=0, padx=10, pady=5)
entry_resistance = tk.Entry(root)
entry_resistance.grid(row=3, column=1, padx=10, pady=5)

# Кнопка для запуска моделирования
button = tk.Button(root, text="Моделировать", command=start_simulation)
button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
