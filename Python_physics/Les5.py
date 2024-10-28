import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция для расчета энергий
def energy_simulation(m, k, b, y0=1.0, v0=0.0, t_max=20, dt=0.01):
    # Дифференциальное уравнение движения: m * y'' = -k * y - b * y'
    def equation(t, y):
        pos, vel = y
        accel = -(k / m) * pos - (b / m) * vel
        return [vel, accel]

    # Время, положение и скорость
    t = np.arange(0, t_max, dt)
    sol = solve_ivp(equation, [0, t_max], [y0, v0], t_eval=t)

    # Вычисляем кинетическую, потенциальную и полную энергии
    pos = sol.y[0]
    vel = sol.y[1]
    kinetic_energy = 0.5 * m * vel ** 2
    potential_energy = 0.5 * k * pos ** 2
    total_energy = kinetic_energy + potential_energy

    return t, kinetic_energy, potential_energy, total_energy


# Функция для построения графиков
def plot_energies(t, kinetic_energy, potential_energy, total_energy):
    fig, ax = plt.subplots()
    ax.plot(t, kinetic_energy, label="Кинетическая энергия", color="blue")
    ax.plot(t, potential_energy, label="Потенциальная энергия", color="orange")
    ax.plot(t, total_energy, label="Полная энергия", color="green")
    ax.set_xlabel("Время (с)")
    ax.set_ylabel("Энергия (Дж)")
    ax.set_title("Энергетические превращения при колебаниях груза на пружине")
    ax.legend()
    fig.tight_layout()
    return fig


# Функция для запуска симуляции и обновления графика
def run_simulation():
    m = float(mass_entry.get())
    k = float(stiffness_entry.get())
    b = float(damping_entry.get())

    t, ke, pe, te = energy_simulation(m, k, b)
    fig = plot_energies(t, ke, pe, te)

    # Отображаем график на Canvas
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Создаем окно интерфейса
root = tk.Tk()
root.title("Энергетические превращения при колебаниях груза на пружине")

# Поля ввода
tk.Label(root, text="Масса груза (кг):").grid(row=0, column=0, padx=5, pady=5)
mass_entry = tk.Entry(root)
mass_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Коэффициент жесткости (Н/м):").grid(row=1, column=0, padx=5, pady=5)
stiffness_entry = tk.Entry(root)
stiffness_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Коэффициент сопротивления (Нс/м):").grid(row=2, column=0, padx=5, pady=5)
damping_entry = tk.Entry(root)
damping_entry.grid(row=2, column=1, padx=5, pady=5)

# Кнопка для запуска симуляции
tk.Button(root, text="Запустить симуляцию", command=run_simulation).grid(row=3, column=0, columnspan=2, pady=10)

# Площадка для графика
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=4, column=0, columnspan=2)

root.mainloop()
