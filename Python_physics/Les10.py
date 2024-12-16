import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# Размеры поля
FIELD_RANGE = 8

class ChargeField:
    def __init__(self):
        self.charges = []  # Список зарядов в формате (q, x, y)
        self.dipoles = []  # Список диполей в формате (p, x, y, angle)

    def add_charge(self, q, x, y):
        if -FIELD_RANGE <= x <= FIELD_RANGE and -FIELD_RANGE <= y <= FIELD_RANGE:
            self.charges.append((q, x, y))
        else:
            messagebox.showerror("Error", "Coordinates out of range [-8, 8].")

    def add_dipole(self, p, x, y, angle):
        if -FIELD_RANGE <= x <= FIELD_RANGE and -FIELD_RANGE <= y <= FIELD_RANGE:
            self.dipoles.append((p, x, y, angle))
        else:
            messagebox.showerror("Error", "Coordinates out of range [-8, 8].")

    def electric_field(self, x, y):
        Ex, Ey = 0, 0
        for q, cx, cy in self.charges:
            dx = x - cx
            dy = y - cy
            r = np.sqrt(dx**2 + dy**2)
            if r != 0:
                E = q / r**2
                Ex += E * dx / r
                Ey += E * dy / r
        return Ex, Ey

    def plot_field(self):
        fig, ax = plt.subplots()
        x = np.linspace(-FIELD_RANGE, FIELD_RANGE, 40)
        y = np.linspace(-FIELD_RANGE, FIELD_RANGE, 40)
        X, Y = np.meshgrid(x, y)

        # Расчёт вектора поля
        Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Ex[i, j], Ey[i, j] = self.electric_field(X[i, j], Y[i, j])

        # Визуализация линий напряженности
        epsilon = 1e-10  # Малое значение для избежания логарифма нуля
        ax.streamplot(X, Y, Ex, Ey, color=np.log(np.sqrt(Ex ** 2 + Ey ** 2) + epsilon), cmap='viridis')

        # Отображение зарядов
        for q, cx, cy in self.charges:
            ax.plot(cx, cy, 'ro' if q > 0 else 'bo', markersize=abs(q) * 5)

        # Обработка диполей
        for idx, dipole in enumerate(self.dipoles):
            p, dx, dy, angle = dipole
            angle_rad = np.radians(angle)
            px, py = p * np.cos(angle_rad), p * np.sin(angle_rad)

            # Вычисление сил на диполь
            E_dipole = self.electric_field(dx, dy)
            torque = p * (E_dipole[0] * np.sin(angle_rad) - E_dipole[1] * np.cos(angle_rad))
            force = np.sqrt(E_dipole[0]**2 + E_dipole[1]**2) * p

            # Отрисовка диполя
            ax.quiver(dx, dy, px, py, angles='xy', scale_units='xy', scale=1, color='purple', label=f'Dipole {idx+1}', width=0.005)

            # Визуализация точек диполя
            ax.plot(dx - px / (2 * p), dy - py / (2 * p), 'go', markersize=8)
            ax.plot(dx + px / (2 * p), dy + py / (2 * p), 'mo', markersize=8)

            # Улучшенная аннотация диполя
            ax.text(dx, dy, f"Dipole {idx + 1}\nF={force:.2f}, T={torque:.2f}",
                    color='black', fontsize=8, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='purple', boxstyle='round,pad=0.3'))

        ax.set_xlim(-FIELD_RANGE, FIELD_RANGE)
        ax.set_ylim(-FIELD_RANGE, FIELD_RANGE)
        ax.set_title("Electric Field and Charges")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.legend()
        plt.show()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Charge and Dipole Simulation")
        self.geometry("400x400")

        self.field = ChargeField()

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Input fields
        ttk.Label(frame, text="Charge (q, x, y):").grid(row=0, column=0, sticky=tk.W)
        self.charge_entry = ttk.Entry(frame)
        self.charge_entry.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(frame, text="Dipole (p, x, y, angle):").grid(row=1, column=0, sticky=tk.W)
        self.dipole_entry = ttk.Entry(frame)
        self.dipole_entry.grid(row=1, column=1, sticky=tk.EW)

        # Buttons
        ttk.Button(frame, text="Add Charge", command=self.add_charge).grid(row=2, column=0, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="Add Dipole", command=self.add_dipole).grid(row=2, column=1, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="Show Details", command=self.show_details).grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="Run Simulation", command=self.run_simulation).grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.EW)

        frame.columnconfigure(1, weight=1)

    def add_charge(self):
        try:
            values = list(map(float, self.charge_entry.get().split(',')))
            if len(values) == 3:
                q, x, y = values
                self.field.add_charge(q, x, y)
                messagebox.showinfo("Success", f"Added charge: q={q}, x={x}, y={y}")
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid input for charge. Format: q, x, y")

    def add_dipole(self):
        try:
            values = list(map(float, self.dipole_entry.get().split(',')))
            if len(values) == 4:
                p, x, y, angle = values
                self.field.add_dipole(p, x, y, angle)
                messagebox.showinfo("Success", f"Added dipole: p={p}, x={x}, y={y}, angle={angle}")
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid input for dipole. Format: p, x, y, angle")

    def show_details(self):
        details = []
        if self.field.charges:
            for q, x, y in self.field.charges:
                details.append(f"Charge q={q}, x={x}, y={y}")
        if self.field.dipoles:
            for idx, (p, x, y, angle) in enumerate(self.field.dipoles):
                details.append(f"Dipole {idx+1} p={p}, x={x}, y={y}, angle={angle}")
        if details:
            messagebox.showinfo("Details", "\n".join(details))
        else:
            messagebox.showinfo("Details", "No charges or dipoles added.")

    def run_simulation(self):
        self.field.plot_field()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
