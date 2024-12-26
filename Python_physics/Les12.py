import tkinter as tk
from tkinter import ttk


def calculate_capacitor_parameters(voltage, distance, dielectric_constant, area, is_connected):
    """
    Рассчитывает параметры плоского конденсатора.

    :param voltage: Напряжение на конденсаторе (В)
    :param distance: Расстояние между пластинами (м)
    :param dielectric_constant: Относительная диэлектрическая проницаемость
    :param area: Площадь пластин (м²)
    :param is_connected: True, если конденсатор подключен к источнику питания
    :return: Словарь с параметрами конденсатора
    """
    epsilon_0 = 8.854e-12  # Ф/м (Фарады на метр)
    electric_field = voltage / distance
    capacitance = dielectric_constant * epsilon_0 * area / distance
    charge = capacitance * voltage

    if not is_connected:
        voltage = charge / capacitance
        electric_field = voltage / distance

    return {
        "electric_field": electric_field,
        "capacitance": capacitance,
        "charge": charge,
        "voltage": voltage
    }


def show_results(result):
    """
    Создает и показывает окно с результатами расчета.
    """
    result_window = tk.Toplevel()
    result_window.title("Результаты расчета")
    result_window.geometry("400x250")
    result_window.configure(bg="lightyellow")

    # Заголовок
    title_label = tk.Label(result_window, text="Результаты расчета", font=("Arial", 16, "bold"), bg="lightyellow")
    title_label.pack(pady=10)

    # Текст с результатами
    result_text = (
        f"Напряженность электрического поля: {result['electric_field']:.2e} В/м\n"
        f"Емкость: {result['capacitance']:.2e} Ф\n"
        f"Заряд на пластинах: {result['charge']:.2e} Кл\n"
        f"Напряжение: {result['voltage']:.2f} В"
    )
    result_label = tk.Label(result_window, text=result_text, font=("Arial", 12), bg="lightyellow", justify="left")
    result_label.pack(pady=10, padx=10)

    # Кнопка закрытия
    close_button = ttk.Button(result_window, text="Закрыть", command=result_window.destroy)
    close_button.pack(pady=10)


def calculate_and_show():
    try:
        # Чтение данных
        voltage = float(entry_voltage.get())
        distance = float(entry_distance.get())
        dielectric_constant = float(entry_dielectric_constant.get())
        area = float(entry_area.get())
        is_connected = var_is_connected.get()

        # Проверка на положительные значения
        if voltage <= 0 or distance <= 0 or dielectric_constant <= 0 or area <= 0:
            raise ValueError("Все вводимые значения должны быть положительными.")

        # Расчет параметров
        result = calculate_capacitor_parameters(voltage, distance, dielectric_constant, area, is_connected)

        # Показать красивое окно с результатами
        show_results(result)

    except ValueError as e:
        error_window = tk.Toplevel()
        error_window.title("Ошибка ввода")
        error_window.geometry("300x150")
        error_window.configure(bg="lightcoral")

        error_label = tk.Label(error_window, text=f"Ошибка: {e}", font=("Arial", 12), bg="lightcoral", fg="white")
        error_label.pack(pady=20)

        close_button = ttk.Button(error_window, text="Закрыть", command=error_window.destroy)
        close_button.pack(pady=10)


# Создание окна приложения
app = tk.Tk()
app.title("Расчет параметров плоского конденсатора")

# Описание
label_description = tk.Label(app, text="Введите параметры конденсатора:", font=("Arial", 14))
label_description.grid(row=0, column=0, columnspan=2, pady=10)

# Поля ввода
label_voltage = tk.Label(app, text="Напряжение (В):")
label_voltage.grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_voltage = tk.Entry(app)
entry_voltage.grid(row=1, column=1, padx=5, pady=5)

label_distance = tk.Label(app, text="Расстояние между пластинами (м):")
label_distance.grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_distance = tk.Entry(app)
entry_distance.grid(row=2, column=1, padx=5, pady=5)

label_dielectric_constant = tk.Label(app, text="Диэлектрическая проницаемость:")
label_dielectric_constant.grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_dielectric_constant = tk.Entry(app)
entry_dielectric_constant.grid(row=3, column=1, padx=5, pady=5)

label_area = tk.Label(app, text="Площадь пластин (м²):")
label_area.grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_area = tk.Entry(app)
entry_area.grid(row=4, column=1, padx=5, pady=5)

# Переключатель "Подключен к источнику"
label_is_connected = tk.Label(app, text="Конденсатор подключен к источнику:")
label_is_connected.grid(row=5, column=0, sticky="e", padx=5, pady=5)
var_is_connected = tk.BooleanVar(value=True)
check_is_connected = tk.Checkbutton(app, text="Да", variable=var_is_connected)
check_is_connected.grid(row=5, column=1, padx=5, pady=5)

# Кнопка расчета
button_calculate = tk.Button(app, text="Рассчитать", command=calculate_and_show, font=("Arial", 12), bg="lightblue")
button_calculate.grid(row=6, column=0, columnspan=2, pady=10)

# Запуск приложения
app.mainloop()
