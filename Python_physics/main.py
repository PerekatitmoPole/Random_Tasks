import tkinter as tk
from tkinter import messagebox
from math import sqrt, atan2, cos, sin, acos, pi


def rectangular_to_cylindrical(x, y, z):
    """Преобразование из декартовой в цилиндрическую систему координат."""
    r = sqrt(x ** 2 + y ** 2)
    phi = atan2(y, x)
    return r, phi, z


def cylindrical_to_rectangular(r, phi, z):
    """Преобразование из цилиндрической в декартовую систему координат."""
    x = r * cos(phi)
    y = r * sin(phi)
    return x, y, z


def rectangular_to_spherical(x, y, z):
    """Преобразование из декартовой в сферическую систему координат."""
    rho = sqrt(x ** 2 + y ** 2 + z ** 2)
    if rho == 0:
        raise ValueError("Радиус rho не может быть равен нулю.")
    theta = acos(z / rho)
    phi = atan2(y, x)
    return rho, theta, phi


def spherical_to_rectangular(rho, theta, phi):
    """Преобразование из сферической в декартовую систему координат."""
    if rho == 0:
        raise ValueError("Радиус rho не может быть равен нулю.")
    x = rho * sin(theta) * cos(phi)
    y = rho * sin(theta) * sin(phi)
    z = rho * cos(theta)
    return x, y, z


def convert_coordinates():
    try:
        # Получение данных из полей ввода
        x = float(entry1.get())
        y = float(entry2.get())
        z = float(entry3.get())
        precision = int(precision_entry.get())

        system_from = from_system.get()
        system_to = to_system.get()

        if system_from == "Декартовая" and system_to == "Цилиндрическая":
            r, phi, z_out = rectangular_to_cylindrical(x, y, z)
            result_label.config(
                text=f"r: {round(r, precision)}, phi: {round(phi, precision)}, z: {round(z_out, precision)}")
        elif system_from == "Цилиндрическая" and system_to == "Декартовая":
            x_out, y_out, z_out = cylindrical_to_rectangular(x, y, z)
            result_label.config(
                text=f"x: {round(x_out, precision)}, y: {round(y_out, precision)}, z: {round(z_out, precision)}")
        elif system_from == "Декартовая" and system_to == "Сферическая":
            rho, theta, phi = rectangular_to_spherical(x, y, z)
            result_label.config(
                text=f"rho: {round(rho, precision)}, theta: {round(theta, precision)}, phi: {round(phi, precision)}")
        elif system_from == "Сферическая" and system_to == "Декартовая":
            x_out, y_out, z_out = spherical_to_rectangular(x, y, z)
            result_label.config(
                text=f"x: {round(x_out, precision)}, y: {round(y_out, precision)}, z: {round(z_out, precision)}")
        else:
            messagebox.showerror("Ошибка", "Неверная комбинация систем координат.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


# Создание окна приложения
root = tk.Tk()
root.title("Преобразование координат")

# Ввод координат
tk.Label(root, text="Координата 1 (x|r|rho):").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Координата 2 (y|phi|theta):").grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

tk.Label(root, text="Координата 3 (z|z|phi):").grid(row=2, column=0)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1)

# Выбор системы координат (откуда и куда)
tk.Label(root, text="Исходная система координат:").grid(row=3, column=0)
from_system = tk.StringVar()
from_system_menu = tk.OptionMenu(root, from_system, "Декартовая", "Цилиндрическая", "Сферическая")
from_system.set("Декартовая")
from_system_menu.grid(row=3, column=1)

tk.Label(root, text="Целевая система координат:").grid(row=4, column=0)
to_system = tk.StringVar()
to_system_menu = tk.OptionMenu(root, to_system, "Декартовая", "Цилиндрическая", "Сферическая")
to_system.set("Цилиндрическая")
to_system_menu.grid(row=4, column=1)

# Ввод точности
tk.Label(root, text="Точность (знаков после запятой):").grid(row=5, column=0)
precision_entry = tk.Entry(root)
precision_entry.grid(row=5, column=1)

# Кнопка для выполнения преобразования
convert_button = tk.Button(root, text="Преобразовать", command=convert_coordinates)
convert_button.grid(row=6, column=0, columnspan=2)

# Метка для вывода результата
result_label = tk.Label(root, text="Результат:")
result_label.grid(row=7, column=0, columnspan=2)

# Запуск главного цикла программы
root.mainloop()
