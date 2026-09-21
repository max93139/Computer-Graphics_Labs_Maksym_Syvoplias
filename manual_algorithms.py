# -*- coding: utf-8 -*-
"""
Модуль власних алгоритмів обробки зображень для лабораторної роботи №1.
Містить покрокові математичні реалізації без використання сторонніх бібліотек:
  1. Зміна розміру: Інтерполяція найближчого сусіда (Nearest Neighbor)
  2. Зміна розміру: Білінійна інтерполяція (Bilinear Interpolation)
  3. Перетворення кольорів: Попіксельна заміна кольору з толерантністю
  4. Корекція колірного балансу: Ручне налаштування та автобаланс
"""


# 1. ЗМІНА РОЗМІРУ: ІНТЕРПОЛЯЦІЯ НАЙБЛИЖЧОГО СУСІДА (Nearest Neighbor)


def resize_nearest_neighbor(
    pixels: list[tuple[int, int, int]],
    orig_w: int,
    orig_h: int,
    new_w: int,
    new_h: int
) -> list[tuple[int, int, int]]:
    """
    Власний алгоритм зміни розміру методом найближчого сусіда.
    Для кожної нової точки (x, y) обчислюються координати найближчого вихідного пікселя.
    """
    resized = []
    x_ratio = orig_w / new_w
    y_ratio = orig_h / new_h

    for y in range(new_h):
        orig_y = min(orig_h - 1, int(y * y_ratio))
        row_offset = orig_y * orig_w
        for x in range(new_w):
            orig_x = min(orig_w - 1, int(x * x_ratio))
            resized.append(pixels[row_offset + orig_x])

    return resized


# 2. ЗМІНА РОЗМІРУ: БІЛІНІЙНА ІНТЕРПОЛЯЦІЯ (Bilinear Interpolation)


def resize_bilinear(
    pixels: list[tuple[int, int, int]],
    orig_w: int,
    orig_h: int,
    new_w: int,
    new_h: int
) -> list[tuple[int, int, int]]:
    """
    Власний алгоритм зміни розміру методом білінійної інтерполяції.
    Значення кожного каналу розраховується як зважена сума 4 сусідніх пікселів.
    """
    def get_pixel(px, py):
        px = max(0, min(orig_w - 1, px))
        py = max(0, min(orig_h - 1, py))
        return pixels[py * orig_w + px]

    resized = []
    x_ratio = (orig_w - 1) / new_w if new_w > 0 else 0
    y_ratio = (orig_h - 1) / new_h if new_h > 0 else 0

    for y in range(new_h):
        src_y = y * y_ratio
        y1 = int(src_y)
        y2 = min(orig_h - 1, y1 + 1)
        dy = src_y - y1

        for x in range(new_w):
            src_x = x * x_ratio
            x1 = int(src_x)
            x2 = min(orig_w - 1, x1 + 1)
            dx = src_x - x1

            p11 = get_pixel(x1, y1)
            p21 = get_pixel(x2, y1)
            p12 = get_pixel(x1, y2)
            p22 = get_pixel(x2, y2)

            r = int((1 - dx) * (1 - dy) * p11[0] + dx * (1 - dy) * p21[0] + (1 - dx) * dy * p12[0] + dx * dy * p22[0])
            g = int((1 - dx) * (1 - dy) * p11[1] + dx * (1 - dy) * p21[1] + (1 - dx) * dy * p12[1] + dx * dy * p22[1])
            b = int((1 - dx) * (1 - dy) * p11[2] + dx * (1 - dy) * p21[2] + (1 - dx) * dy * p12[2] + dx * dy * p22[2])

            resized.append((max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))))

    return resized


# 3. ПЕРЕТВОРЕННЯ КОЛЬОРІВ (Попіксельна заміна)


def replace_pixels_color(
    pixels: list[tuple[int, int, int]],
    target_rgb: tuple[int, int, int],
    new_rgb: tuple[int, int, int],
    tolerance: int = 15
) -> tuple[list[tuple[int, int, int]], int]:
    """
    Попіксельна заміна цільового кольору на новий з урахуванням допустимого відхилення tolerance.
    """
    tr, tg, tb = target_rgb
    nr, ng, nb = new_rgb
    replaced_count = 0
    result = []

    for r, g, b in pixels:
        if abs(r - tr) <= tolerance and abs(g - tg) <= tolerance and abs(b - tb) <= tolerance:
            result.append((nr, ng, nb))
            replaced_count += 1
        else:
            result.append((r, g, b))

    return result, replaced_count


# 4. КОЛІРНИЙ БАЛАНС ТА АВТОБАЛАНС


def apply_color_balance(
    pixels: list[tuple[int, int, int]],
    r_factor: float = 1.0,
    g_factor: float = 1.0,
    b_factor: float = 1.0,
    r_delta: int = 0,
    g_delta: int = 0,
    b_delta: int = 0
) -> list[tuple[int, int, int]]:
    """
    Попіксельна ручна корекція колірного балансу:
      C_new = clamp(int(C_old * factor + delta), 0, 255)
    """
    def clamp(v):
        return max(0, min(255, int(v)))

    result = []
    for r, g, b in pixels:
        new_r = clamp(r * r_factor + r_delta)
        new_g = clamp(g * g_factor + g_delta)
        new_b = clamp(b * b_factor + b_delta)
        result.append((new_r, new_g, new_b))

    return result


def apply_auto_color_balance(
    pixels: list[tuple[int, int, int]],
    target_mean: float = 128.0
) -> tuple[list[tuple[int, int, int]], dict]:
    """
    Автоматичний баланс кольорів за формулою з методички:
      1. Середні значення яскравості: mean_R, mean_G, mean_B.
      2. Зсув: shift_C = target_mean (128) - mean_C.
      3. C_new = clamp(C_old + shift_C, 0, 255).
    """
    def clamp(v):
        return max(0, min(255, int(v)))

    total = len(pixels)
    if total == 0:
        return pixels, {}

    sum_r = sum(p[0] for p in pixels)
    sum_g = sum(p[1] for p in pixels)
    sum_b = sum(p[2] for p in pixels)

    mean_r = sum_r / total
    mean_g = sum_g / total
    mean_b = sum_b / total

    shift_r = target_mean - mean_r
    shift_g = target_mean - mean_g
    shift_b = target_mean - mean_b

    result = []
    for r, g, b in pixels:
        new_r = clamp(r + shift_r)
        new_g = clamp(g + shift_g)
        new_b = clamp(b + shift_b)
        result.append((new_r, new_g, new_b))

    stats = {
        "means": (round(mean_r, 2), round(mean_g, 2), round(mean_b, 2)),
        "shifts": (round(shift_r, 2), round(shift_g, 2), round(shift_b, 2)),
        "target_mean": target_mean
    }

    return result, stats
