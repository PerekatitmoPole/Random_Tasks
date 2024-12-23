import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

def calculate_vectors(e1, e2, e_field_x, e_field_y):
    # Рассчитать коэффициент преломления
    ratio = e1 / e2

    # Векторы в первой среде
    x1 = np.linspace(-1, 0, 10)
    y1 = np.linspace(-1, 1, 10)
    x1, y1 = np.meshgrid(x1, y1)
    e_x1 = np.full_like(x1, e_field_x)
    e_y1 = np.full_like(y1, e_field_y)

    # Преломление на границе: изменяем соотношение компонентов
    tan_ratio = ratio  # Для тангенциального сохранение
    norm_ratio = 1 / ratio  # Для нормального сохранения

    # Векторы во второй среде
    x2 = np.linspace(0, 1, 10)
    y2 = np.linspace(-1, 1, 10)
    x2, y2 = np.meshgrid(x2, y2)
    e_x2 = e_field_x * tan_ratio
    e_y2 = e_field_y * norm_ratio

    return (x1, y1, e_x1, e_y1), (x2, y2, e_x2, e_y2)

def visualize(e1, e2, e_field_x, e_field_y):
    # Рассчитать векторы
    (x1, y1, e_x1, e_y1), (x2, y2, e_x2, e_y2) = calculate_vectors(e1, e2, e_field_x, e_field_y)

    # Создать график
    plt.figure(figsize=(10, 6))
    plt.quiver(x1, y1, e_x1, e_y1, color='blue', label="Среда 1 (ε1)")
    plt.quiver(x2, y2, e_x2, e_y2, color='red', label="Среда 2 (ε2)")
    plt.axvline(0, color='black', linewidth=2, label="Граница")
    plt.title("Преломление линий напряжённости на границе диэлектриков")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()
    plt.show()

def run_visualization():
    try:
        e1 = float(e1_entry.get())
        e2 = float(e2_entry.get())
        e_field_x = float(ex_entry.get())
        e_field_y = float(ey_entry.get())
        visualize(e1, e2, e_field_x, e_field_y)
    except ValueError:
        error_label.config(text="Ошибка: Проверьте введенные данные.", foreground="red")

# Создание окна ввода
root = tk.Tk()
root.title("Визуализация граничных условий")

# Поля ввода
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Диэлектрическая проницаемость первой среды (ε1):").grid(row=0, column=0, sticky=tk.W)
e1_entry = ttk.Entry(frame, width=20)
e1_entry.grid(row=0, column=1)

ttk.Label(frame, text="Диэлектрическая проницаемость второй среды (ε2):").grid(row=1, column=0, sticky=tk.W)
e2_entry = ttk.Entry(frame, width=20)
e2_entry.grid(row=1, column=1)

ttk.Label(frame, text="X-компонент напряжённости поля (Ex):").grid(row=2, column=0, sticky=tk.W)
ex_entry = ttk.Entry(frame, width=20)
ex_entry.grid(row=2, column=1)

ttk.Label(frame, text="Y-компонент напряжённости поля (Ey):").grid(row=3, column=0, sticky=tk.W)
ey_entry = ttk.Entry(frame, width=20)
ey_entry.grid(row=3, column=1)

# Кнопка для запуска визуализации
run_button = ttk.Button(frame, text="Визуализировать", command=run_visualization)
run_button.grid(row=4, column=0, columnspan=2)

# Поле для сообщений об ошибках
error_label = ttk.Label(frame, text="", foreground="red")
error_label.grid(row=5, column=0, columnspan=2)

# Запуск окна
root.mainloop()
