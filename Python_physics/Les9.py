import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Константы
k = 9e9  # Электростатическая постоянная


# Функция для вычисления потенциала в точке (x, y)
def potential(x, y, charges):
    V = np.zeros_like(x)
    for charge in charges:
        q, xq, yq = charge
        r = np.sqrt((x - xq) ** 2 + (y - yq) ** 2)
        r = np.maximum(r, 1e-12)  # Избежание деления на ноль
        V += k * q / r
    return np.clip(V, -1e12, 1e12)  # Ограничение значений


# Функция для вычисления компонент электрического поля
def electric_field(x, y, charges):
    Ex = np.zeros_like(x)
    Ey = np.zeros_like(y)
    for charge in charges:
        q, xq, yq = charge
        dx = x - xq
        dy = y - yq
        r2 = dx ** 2 + dy ** 2
        r2 = np.maximum(r2, 1e-12)  # Избежание деления на ноль
        Ex += k * q * dx / r2
        Ey += k * q * dy / r2
    return Ex, Ey


# Функция для расчета и визуализации
def calculate_and_plot(charges):
    if not charges:
        messagebox.showerror("Ошибка", "Добавьте хотя бы один заряд для расчета!")
        return

    # Создаем сетку для расчетов
    x = np.linspace(-5, 5, 300)
    y = np.linspace(-5, 5, 300)
    X, Y = np.meshgrid(x, y)

    # Вычисляем потенциал и поле
    V = potential(X, Y, charges)
    Ex, Ey = electric_field(X, Y, charges)

    # Визуализация
    fig, ax = plt.subplots(figsize=(10, 8))

    # Эквипотенциальные линии
    contour = ax.contour(X, Y, V, levels=30, cmap='coolwarm', alpha=0.9)
    plt.clabel(contour, inline=True, fontsize=8, fmt="%.1e", colors='black')

    # Линии напряженности
    magnitude = np.sqrt(Ex ** 2 + Ey ** 2)
    magnitude = np.clip(magnitude, 0, np.percentile(magnitude, 95))  # Ограничение интенсивности
    stream = ax.streamplot(X, Y, Ex, Ey, color=magnitude, cmap='plasma', linewidth=1.2, density=1.5)
    cbar = plt.colorbar(stream.lines, ax=ax, shrink=0.8, label='Intensity of E-field')

    # Отображение зарядов
    for q, xq, yq in charges:
        color = 'red' if q > 0 else 'blue'
        ax.scatter(xq, yq, color=color, s=100, edgecolor='black', label=f"{'+' if q > 0 else ''}{q * 1e9:.1f} nC")

    ax.set_title("Эквипотенциальные линии и линии напряженности", fontsize=16, pad=20)
    ax.set_xlabel("x (m)", fontsize=12)
    ax.set_ylabel("y (m)", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.legend(loc='upper right', fontsize=10, frameon=True)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    plt.show()


# Основная программа с GUI
def main():
    charges = []

    def add_charge():
        try:
            q = float(entry_charge.get())
            xq = float(entry_x.get())
            yq = float(entry_y.get())
            charges.append((q, xq, yq))
            listbox.insert(tk.END, f"{'+' if q > 0 else ''}{q:.1e} C | ({xq:.2f}, {yq:.2f})")
            entry_charge.delete(0, tk.END)
            entry_x.delete(0, tk.END)
            entry_y.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные значения!")

    def calculate():
        calculate_and_plot(charges)

    # Создаем окно
    root = tk.Tk()
    root.title("Система зарядов")

    # Поля для ввода заряда
    tk.Label(root, text="Величина заряда (Кл):", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_charge = tk.Entry(root, font=("Arial", 10))
    entry_charge.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Координата x (м):", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_x = tk.Entry(root, font=("Arial", 10))
    entry_x.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Координата y (м):", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_y = tk.Entry(root, font=("Arial", 10))
    entry_y.grid(row=2, column=1, padx=5, pady=5)

    # Кнопка для добавления заряда
    btn_add = tk.Button(root, text="Добавить заряд", font=("Arial", 10), command=add_charge)
    btn_add.grid(row=3, column=0, columnspan=2, pady=10)

    # Список зарядов
    tk.Label(root, text="Список зарядов:", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, padx=5,
                                                                            pady=5)
    listbox = tk.Listbox(root, width=40, height=10, font=("Courier", 10))
    listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Кнопка для расчета
    btn_calculate = tk.Button(root, text="Рассчитать систему", font=("Arial", 12, "bold"), bg="green", fg="white",
                              command=calculate)
    btn_calculate.grid(row=6, column=0, columnspan=2, pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
