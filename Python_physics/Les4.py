import pygame
import math
import tkinter as tk
from tkinter import simpledialog

# Инициализация Pygame
pygame.init()


# Функция для обработки столкновения двух тел
def handle_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance < ball1.radius + ball2.radius:
        normal_x = dx / distance
        normal_y = dy / distance

        v1_normal = ball1.vx * normal_x + ball1.vy * normal_y
        v2_normal = ball2.vx * normal_x + ball2.vy * normal_y

        v1_new = (v1_normal * (ball1.mass - ball2.mass) + 2 * ball2.mass * v2_normal) / (ball1.mass + ball2.mass)
        v2_new = (v2_normal * (ball2.mass - ball1.mass) + 2 * ball1.mass * v1_normal) / (ball1.mass + ball2.mass)

        ball1.vx += (v1_new - v1_normal) * normal_x
        ball1.vy += (v1_new - v1_normal) * normal_y
        ball2.vx += (v2_new - v2_normal) * normal_x
        ball2.vy += (v2_new - v2_normal) * normal_y


# Класс для представления тел
class Ball:
    def __init__(self, x, y, vx, vy, radius, mass, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.mass = mass
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vx = -self.vx
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# Функция для инициализации симуляции
def run_simulation(mass1, vx1, vy1, mass2, vx2, vy2):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = 800, 600  # Устанавливаем размеры оболочки 800x600

    # Установка окна Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Абсолютно упругое соударение")

    # Создаем два тела
    ball1 = Ball(100, 100, vx1, vy1, 30, mass1, (255, 0, 0))
    ball2 = Ball(300, 300, vx2, vy2, 40, mass2, (0, 0, 255))

    clock = pygame.time.Clock()
    FPS = 60

    # Основной цикл симуляции
    running = True
    while running:
        screen.fill((255, 255, 255))  # Белый фон

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Движение и отрисовка тел
        ball1.move()
        ball2.move()
        ball1.draw(screen)
        ball2.draw(screen)

        # Обработка столкновения тел
        handle_collision(ball1, ball2)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# Функция для отображения окна ввода параметров
def get_parameters():
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно Tkinter

    # Ввод параметров с помощью диалоговых окон
    mass1 = float(simpledialog.askstring("Масса тела 1", "Введите массу тела 1:"))
    vx1 = float(simpledialog.askstring("Скорость тела 1 по X", "Введите скорость тела 1 по оси X:"))
    vy1 = float(simpledialog.askstring("Скорость тела 1 по Y", "Введите скорость тела 1 по оси Y:"))

    mass2 = float(simpledialog.askstring("Масса тела 2", "Введите массу тела 2:"))
    vx2 = float(simpledialog.askstring("Скорость тела 2 по X", "Введите скорость тела 2 по оси X:"))
    vy2 = float(simpledialog.askstring("Скорость тела 2 по Y", "Введите скорость тела 2 по оси Y:"))

    # Запуск симуляции с введёнными параметрами
    run_simulation(mass1, vx1, vy1, mass2, vx2, vy2)


# Запуск окна ввода параметров
get_parameters()
