import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import quad

# Параметры задачи (ввод пользователем начальной высоты и скорости)
g_L_moon = 1.62  # м/с^2, лунное ускорение свободного падения
mass_ship = 2000 + 150  # кг, масса космического аппарата
exhaust_velocity = -3660  # м/с, скорость истечения топлива
fuel_mass_initial = 150  # кг, начальная масса топлива
fuel_consumption_rate = 15  # кг/с, скорость расхода топлива
safe_landing_velocity = 0.001  # м/с, безопасная скорость посадки

try:
    initial_height = float(input("Введите начальную высоту (в метрах): "))
    initial_velocity = float(input("Введите начальную вертикальную скорость (в м/с): "))
except ValueError:
    print("Ошибка ввода! Пожалуйста, введите числовые значения.")
    exit()

# Функция скорости Мещерского
def calc_velocity_with_thrust(time):
    return exhaust_velocity * np.log((mass_ship + fuel_mass_initial) / (mass_ship + fuel_mass_initial - fuel_consumption_rate * time)) - g_L_moon * time

# Функция ускорения аппарата при включенных двигателях
def calc_acceleration_with_thrust(time):
    remaining_fuel_mass = fuel_mass_initial - fuel_consumption_rate * time
    total_mass = mass_ship + remaining_fuel_mass
    return (fuel_consumption_rate * exhaust_velocity - total_mass * g_L_moon) / total_mass

# Функция для расчета времени свободного падения и времени работы двигателей
def landing_equations(variables):
    free_fall_time, engine_burn_time = variables
    velocity_at_engine_start = initial_velocity + g_L_moon * free_fall_time
    height_with_thrust, _ = quad(calc_velocity_with_thrust, 0, engine_burn_time)

    equation1 = (velocity_at_engine_start
           + exhaust_velocity * np.log((mass_ship + fuel_mass_initial) / (mass_ship + fuel_mass_initial - fuel_consumption_rate * engine_burn_time))
           - g_L_moon * engine_burn_time - safe_landing_velocity)

    equation2 = (initial_velocity * free_fall_time
           + 0.5 * g_L_moon * free_fall_time ** 2
           + velocity_at_engine_start * engine_burn_time
           + height_with_thrust - initial_height)

    return [equation1, equation2]

# Решение уравнений
free_fall_time, engine_burn_time = fsolve(landing_equations, (0, 0))

# Высота включения двигателей и скорость на этом уровне
height_at_engine_start = initial_height - (initial_velocity * free_fall_time + 0.5 * g_L_moon * free_fall_time ** 2)
velocity_at_engine_start = initial_velocity + g_L_moon * free_fall_time

print(f"Высота включения двигателей: {height_at_engine_start:.2f} м")
print(f"Скорость при включении двигателей: {velocity_at_engine_start:.2f} м/с")

# Расчет конечной скорости на высоте 0
final_velocity = (velocity_at_engine_start
                  + exhaust_velocity * np.log((mass_ship + fuel_mass_initial) / (mass_ship + fuel_mass_initial - fuel_consumption_rate * engine_burn_time))
                  - g_L_moon * engine_burn_time)
print(f"Вертикальная скорость на высоте 0: {final_velocity:.2f} м/с")

# Подготовка данных для графиков
time_range = np.linspace(0, free_fall_time + engine_burn_time, 500)
velocity_values = []
acceleration_values = []
height_values = []

for t in time_range:
    if t < free_fall_time:
        acceleration = g_L_moon
        velocity = initial_velocity + acceleration * t
        height = initial_height - (initial_velocity * t + 0.5 * acceleration * t ** 2)
    else:
        thrust_duration = t - free_fall_time
        acceleration = calc_acceleration_with_thrust(thrust_duration)
        velocity_integral, _ = quad(calc_acceleration_with_thrust, 0, thrust_duration)
        velocity = velocity_at_engine_start + velocity_integral
        height_integral, _ = quad(calc_velocity_with_thrust, 0, thrust_duration)
        height = height_at_engine_start - (velocity_at_engine_start * thrust_duration + height_integral)

    velocity_values.append(velocity)
    acceleration_values.append(acceleration)
    height_values.append(height)

# Построение графиков
plt.figure(figsize=(15, 8))

# График скорости
ax1 = plt.subplot(3, 1, 1)
ax1.plot(time_range, velocity_values, label="Скорость $V_y$")
ax1.set_facecolor("white")
plt.ylabel("Скорость (м/с)")
plt.title("Зависимость скорости от времени")
plt.legend()

# График ускорения
ax2 = plt.subplot(3, 1, 2)
ax2.plot(time_range, acceleration_values, label="Ускорение $a_y$", color="orange")
ax2.set_facecolor("blue")
plt.ylabel("Ускорение (м/с²)")
plt.title("Зависимость ускорения от времени")
plt.legend()

# График высоты
ax3 = plt.subplot(3, 1, 3)
ax3.plot(time_range, height_values, label="Высота $H$", color="green")
ax3.set_facecolor("red")
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.title("Зависимость высоты от времени")
plt.legend()

plt.tight_layout()
plt.show()
