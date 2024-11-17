import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, Scrollbar, Canvas

# Константа Кулона
k = 8.9875517923e9  # Н·м²/Кл²

# Функция для построения электростатического поля
def visualize_field(charges):
    if not charges:
        messagebox.showerror("Ошибка", "Список зарядов пуст.")
        return

    # Находим минимальные и максимальные координаты зарядов
    x_coords = [charge['x'] for charge in charges]
    y_coords = [charge['y'] for charge in charges]

    # Определяем диапазон поля
    margin = 2  # Запас
    x_min, x_max = min(x_coords) - margin, max(x_coords) + margin
    y_min, y_max = min(y_coords) - margin, max(y_coords) + margin

    # Сетка расчёта
    x = np.linspace(x_min, x_max, 300)
    y = np.linspace(y_min, y_max, 300)
    X, Y = np.meshgrid(x, y)
    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)

    # Вычисляем поле
    for charge in charges:
        pos = np.array([charge['x'], charge['y']])
        q = charge['q']
        rx, ry = X - pos[0], Y - pos[1]
        r = np.sqrt(rx**2 + ry**2)
        r3 = r**3
        r3[r3 == 0] = np.inf  # Избегаем деления на ноль
        Ex += k * q * rx / r3
        Ey += k * q * ry / r3

    # Визуализация
    fig, ax = plt.subplots(figsize=(8, 6))

    # Векторное поле
    ax.quiver(X, Y, Ex, Ey, color="blue", pivot="middle", scale=1e12, width=0.005)

    # Линии уровня потенциала
    potential = np.zeros(X.shape)
    for charge in charges:
        pos = np.array([charge['x'], charge['y']])
        q = charge['q']
        r = np.sqrt((X - pos[0])**2 + (Y - pos[1])**2)
        potential += k * q / r
        potential[np.abs(potential) > 1e12] = np.nan  # Убираем точки слишком близко к зарядам

    contour = ax.contour(X, Y, potential, levels=50, cmap="viridis")
    cbar = plt.colorbar(contour, ax=ax, label="Potential (V)")
    cbar.ax.set_ylabel("Potential (V)", rotation=270, labelpad=20)

    # Оформление
    ax.set_title("Электростатическое поле точечных зарядов")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    plt.tight_layout()
    plt.show()

# Класс интерфейса для динамического добавления зарядов
class ChargeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ввод данных зарядов")

        # Пояснение для пользователя
        title_frame = Frame(root, bg="#f0f0f0", pady=10)
        title_frame.pack(fill="x")
        Label(
            title_frame,
            text="Электростатическое поле точечных зарядов",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        ).pack()
        Label(
            title_frame,
            text="Введите данные зарядов. Каждый заряд задаётся мантиссой, степенью 10, \n"
                 "и координатами X и Y (в метрах). Поле автоматически подстроится под заряды.",
            font=("Arial", 12),
            bg="#f0f0f0",
            wraplength=600,
            justify="center"
        ).pack(pady=5)

        # Область для ввода зарядов
        self.frame = Frame(root)
        self.frame.pack(fill="both", expand=True)

        # Скроллбар
        self.canvas = Canvas(self.frame)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Заголовки столбцов
        Label(self.scrollable_frame, text="Мантисса", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        Label(self.scrollable_frame, text="Степень (10^n)", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        Label(self.scrollable_frame, text="Координата X (m)", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)
        Label(self.scrollable_frame, text="Координата Y (m)", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)

        # Кнопки
        button_frame = Frame(root, pady=10)
        button_frame.pack(fill="x")

        self.add_charge_button = Button(button_frame, text="Добавить заряд", command=self.add_charge, bg="#4CAF50", fg="white", padx=10)
        self.add_charge_button.pack(side="left", padx=10)

        self.visualize_button = Button(button_frame, text="Построить поле", command=self.submit_charges, bg="#2196F3", fg="white", padx=10)
        self.visualize_button.pack(side="right", padx=10)

        # Список полей ввода
        self.entries = []
        self.add_charge()  # Добавляем первый заряд по умолчанию

    def add_charge(self):
        """Добавляет строку для ввода нового заряда."""
        row = len(self.entries) + 1
        mantissa_entry = Entry(self.scrollable_frame, width=10)
        mantissa_entry.grid(row=row, column=1, padx=5, pady=2)
        exponent_entry = Entry(self.scrollable_frame, width=10)
        exponent_entry.grid(row=row, column=2, padx=5, pady=2)
        x_entry = Entry(self.scrollable_frame, width=10)
        x_entry.grid(row=row, column=3, padx=5, pady=2)
        y_entry = Entry(self.scrollable_frame, width=10)
        y_entry.grid(row=row, column=4, padx=5, pady=2)
        self.entries.append((mantissa_entry, exponent_entry, x_entry, y_entry))

    def submit_charges(self):
        """Считывает данные из полей ввода и вызывает функцию визуализации."""
        try:
            charges = []
            for entry in self.entries:
                mantissa = float(entry[0].get())
                exponent = int(entry[1].get())
                q = mantissa * (10 ** exponent)
                x = float(entry[2].get())
                y = float(entry[3].get())
                charges.append({'q': q, 'x': x, 'y': y})
            visualize_field(charges)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения.")

# Запуск приложения
if __name__ == "__main__":
    root = Tk()
    app = ChargeApp(root)
    root.mainloop()
