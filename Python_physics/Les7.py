import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


# Функция для запуска расчета и построения графика
def calculate():
    try:
        # Получение и преобразование данных из полей ввода
        choice = int(choice_var.get())

        # Обработка различных типов полей
        if choice == 1:
            G = float(entry_G.get())
            m1 = float(entry_m1.get())
            m2 = float(entry_m2.get())
            U = -G * m1 * m2 / np.sqrt(X ** 2 + Y ** 2 + 1e-6)
        elif choice == 2:
            m = float(entry_m.get())
            g = float(entry_g.get())
            U = m * g * Y
        elif choice == 3:
            k = float(entry_k.get())
            U = k * (X ** 2 + Y ** 2) / 2
        elif choice == 4:
            a = float(entry_a.get())
            b = float(entry_b.get())
            p = float(entry_p.get())
            q = float(entry_q.get())
            U = a * X ** p + b * Y ** q
        else:
            messagebox.showerror("Ошибка", "Некорректный выбор!")
            return

        # Построение графика
        plt.figure(figsize=(8, 6))
        cp = plt.contourf(X, Y, U, levels=50, cmap="viridis")
        plt.colorbar(cp, label="Потенциальная энергия U(x, y)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Распределение потенциальной энергии U(x, y)")
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


# Функция для отображения нужных полей ввода
def update_fields(*args):
    # Очистка старых полей
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    choice = int(choice_var.get())

    # Запрос нужных полей на основе выбора
    if choice == 1:
        tk.Label(frame_inputs, text="G:").grid(row=0, column=0)
        tk.Label(frame_inputs, text="m1:").grid(row=1, column=0)
        tk.Label(frame_inputs, text="m2:").grid(row=2, column=0)
        global entry_G, entry_m1, entry_m2
        entry_G = tk.Entry(frame_inputs)
        entry_m1 = tk.Entry(frame_inputs)
        entry_m2 = tk.Entry(frame_inputs)
        entry_G.grid(row=0, column=1)
        entry_m1.grid(row=1, column=1)
        entry_m2.grid(row=2, column=1)
    elif choice == 2:
        tk.Label(frame_inputs, text="m:").grid(row=0, column=0)
        tk.Label(frame_inputs, text="g:").grid(row=1, column=0)
        global entry_m, entry_g
        entry_m = tk.Entry(frame_inputs)
        entry_g = tk.Entry(frame_inputs)
        entry_m.grid(row=0, column=1)
        entry_g.grid(row=1, column=1)
    elif choice == 3:
        tk.Label(frame_inputs, text="k:").grid(row=0, column=0)
        global entry_k
        entry_k = tk.Entry(frame_inputs)
        entry_k.grid(row=0, column=1)
    elif choice == 4:
        tk.Label(frame_inputs, text="a:").grid(row=0, column=0)
        tk.Label(frame_inputs, text="b:").grid(row=1, column=0)
        tk.Label(frame_inputs, text="p:").grid(row=2, column=0)
        tk.Label(frame_inputs, text="q:").grid(row=3, column=0)
        global entry_a, entry_b, entry_p, entry_q
        entry_a = tk.Entry(frame_inputs)
        entry_b = tk.Entry(frame_inputs)
        entry_p = tk.Entry(frame_inputs)
        entry_q = tk.Entry(frame_inputs)
        entry_a.grid(row=0, column=1)
        entry_b.grid(row=1, column=1)
        entry_p.grid(row=2, column=1)
        entry_q.grid(row=3, column=1)


# Создание окна приложения
root = tk.Tk()
root.title("Моделирование потенциального поля")

# Создание выпадающего списка для выбора типа поля
tk.Label(root, text="Выберите тип потенциального поля:").pack()
choice_var = tk.StringVar(value="1")
choices = [
    ("Гравитационное поле", "1"),
    ("Поле силы тяжести", "2"),
    ("Потенциальное поле упругости", "3"),
    ("Произвольное степенное поле", "4")
]
for text, value in choices:
    tk.Radiobutton(root, text=text, variable=choice_var, value=value).pack(anchor=tk.W)

# Обработчик для отображения полей ввода
frame_inputs = tk.Frame(root)
frame_inputs.pack()
choice_var.trace("w", update_fields)
update_fields()

# Кнопка запуска расчета
tk.Button(root, text="Рассчитать", command=calculate).pack()

# Задаем сетку для x и y для расчетов
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

root.mainloop()
