
## Задание к лекции 1 - Les 1

**Задача:**  
Написать программу, в виде исполняемого файла, которая переводит координат из одной системы координат в другую.

**Входные данные:**  
- Координаты в выбранной системе координат.
- Количество знаков после запятой.
  

**Результат:**  
- Координаты в другой системе координат.

---

## Задание к лекции 2 - Les 2

**Задача:**  
Написать программу, в виде исполняемого файла, которая визуализирует баллистическое движение тела, брошенного под углом к горизонту (сопротивлением воздуха пренебречь).

**Входные данные:**  
- Высота, с которой брошено тело
- Начальная скорость
- Угол, под которым брошено тело

**Результат:**  
- Визуализация траектории движения тела
- Графики зависимости скорости и координат от времени

---

## Задание к лекции 3 - Les 3

**Задача:**  
Написать программу, визуализирующую движения точки на ободе колеса/диска

**Входные данные:**  
- Радиус колеса
- Скорость центра масс.


**Результат:**  
- Итоговый вид модели: траектория точки на ободе колеса

---

## Задание к лекции 4 - Les 4

**Задача:**
Визуализация абсолютно упругого нецентрального соударения двух тел с разными массами. 
Тела находятся в ограниченной прямоугольной оболочке, соударения с оболочкой также считать абсолютно упругими.

**Входные данные:**
- Массы тел.
- Начальные скорости (модуль и направление)

**Результат:**
- Динамическое столкновение тел друг с другом и с оболочкой.

---

## Задание к лекции 8 - Les 5

**Задача:**
Энергетические превращения при колебании груза на пружине.

**Входные данные:**
- Масса груза
- Коэффициент жесткости
- Коэффициент сопротивления среды (сила сопротивления пропорциональная скорости).

**Итоговый вид:** 
Графики зависимости кинетической, потенциальной и полной механической энергии от времени. 

---


## Задание к лекциям 5, 6, 7 - les 6 и les 7

**Часть 1**
**Моделирование движения тела, брошенного под углом к горизонту с учетом силы сопротивления воздуха.**
Сила сопротивления воздуха пропорциональна скорости движения тела 𝐹 = −𝑘𝜐. 

**Входные параметры:**
∙ начальная скорость
∙ угол между вектором скорости и линией горизонта
∙ высота, с которой брошено тело
∙ коэффициент сопротивления среда 𝑘
**Результат:** 
Графики (траектория движения тела, зависимость скорости и координат от времени)

**Часть 2** 
**Задача - моделирование потенциального поля.**
Визуализировать двумерное распределение потенциальное энергии U (x,y). 
**Входные параметры:**
- зависимость равнодействующей всех сил, действующих на тело от координат 𝐹 𝑥, 𝑦 .
**Дополнительная информация**
При моделировании можно использовать известные силы из механики (упругости, гравитации, тяжести) или неизвестные силы, выраженные, как степенные функции от координат.


**Обоснование решения ОДУ**
В данной программе используется **метод Рунге-Кутты 4-го порядка**.

**Почему выбран метод Рунге-Кутты 4-го порядка?**
Метод Рунге-Кутты 4-го порядка — это один из наиболее популярных и надежных методов численного решения ОДУ:

- **Высокая точность**: Метод обладает точностью 4-го порядка, что делает его более точным, чем методы более низкого порядка, такие как метод Эйлера.
- **Устойчивость**: хорошо справляется с задачами, где присутствует затухающая динамика, вызванная, в данном случае, сопротивлением воздуха.
- **Эффективность**: Приемлемый уровень вычислительных затрат.


  ---

## Задание к лекции 10 - Les 8
**Моделирование:**
Визуализация электростатического поля системы неподвижных точечных зарядов в двумерном пространстве.

**Входные параметры:**
- Мантисса (число со знаком) и степень 10 заряда в Кулонах.
- Координаты заряда X, Y.
- Количество зарядов.

**Результат**
Двумерное пространство с зарядами


 ---
## Задание к лекции 12 - Les 9
**Моделирование:**
Визуализация эквипотенциальных поверхностей системы точечных зарядов.

**Входные параметры:**
- Величина заряда.
- Координаты заряда X, Y.

**Результаты**
Визуализация системы зарядов

### Формулы

1. **Потенциал \( V \) из заряда:**

   $$ V = k \cdot \frac{q}{r} $$

   где:
   - \( k \) — электрическая постоянная,
   - \( q \) — величина заряда,
   - \( r \) — расстояние между точкой наблюдения и зарядом.

2. **Компоненты электрического поля:**
   
$$ E_x = k \cdot \frac{q \cdot (x - x_q)}{r^3} $$

$$ E_y = k \cdot \frac{q \cdot (y - y_q)}{r^3} $$

   где:
   - \( E_x \) и \( E_y \) — компоненты электрического поля по осям \( x \) и \( y \),
   - \( r \) — расстояние между точкой наблюдения и зарядом.

