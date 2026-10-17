
"""
1. Прозорість та накладання шарів
2. Кадрування та поділ на частини
3. Зміна контрастності за формулою
"""


# 1. Прозорість та накладання

def set_transparency(pixels, alpha):
    """
    Додає або змінює прозорість (альфа-канал) для всіх пікселів.
    alpha: від 0 (прозорий) до 255 (непрозорий)
    """
    alpha = max(0, min(255, int(alpha)))
    result = []
    for p in pixels:
        r, g, b = p[0], p[1], p[2]
        result.append((r, g, b, alpha))
    return result


def overlay_layers(base_pixels, base_w, base_h, over_pixels, over_w, over_h, pos_x, pos_y, alpha_factor=1.0):
    """
    Накладає одне зображення поверх іншого з урахуванням прозорості (Alpha Blending).
    """
    # Створюємо копію фону у форматі RGBA
    result = []
    for p in base_pixels:
        if len(p) == 4:
            result.append((p[0], p[1], p[2], p[3]))
        else:
            result.append((p[0], p[1], p[2], 255))

    # Накладаємо пікселі верхнього шару
    for y in range(over_h):
        for x in range(over_w):
            bx = pos_x + x
            by = pos_y + y

            # Перевіряємо чи піксель в межах базового зображення
            if 0 <= bx < base_w and 0 <= by < base_h:
                top_p = over_pixels[y * over_w + x]
                bot_p = result[by * base_w + bx]

                top_r, top_g, top_b = top_p[0], top_p[1], top_p[2]
                top_a = top_p[3] if len(top_p) == 4 else 255

                # Пропорція накладання (0.0 .. 1.0)
                a = (top_a / 255.0) * alpha_factor

                # Лінійне змішування кольорів
                new_r = int(top_r * a + bot_p[0] * (1 - a))
                new_g = int(top_g * a + bot_p[1] * (1 - a))
                new_b = int(top_b * a + bot_p[2] * (1 - a))

                result[by * base_w + bx] = (new_r, new_g, new_b, 255)

    return result


# 2. Кадрування та розбиття на частини

def split_image(pixels, width, height, rows, cols):
    """
    Розбиває зображення на rows x cols рівних частин.
    """
    part_w = width // cols
    part_h = height // rows
    parts = []

    for r in range(rows):
        for c in range(cols):
            x1 = c * part_w
            y1 = r * part_h
            x2 = width if c == cols - 1 else (c + 1) * part_w
            y2 = height if r == rows - 1 else (r + 1) * part_h

            current_w = x2 - x1
            current_h = y2 - y1

            part_pixels = []
            for y in range(y1, y2):
                for x in range(x1, x2):
                    part_pixels.append(pixels[y * width + x])

            parts.append({
                "index": len(parts) + 1,
                "width": current_w,
                "height": current_h,
                "pixels": part_pixels
            })

    return parts


def crop_area(pixels, width, height, x1, y1, x2, y2):
    """
    Вилучає все, що за межами обраної прямокутної області (залишає тільки область).
    """
    # Впорядковуємо та обмежуємо координати
    left = max(0, min(x1, x2))
    right = min(width, max(x1, x2))
    top = max(0, min(y1, y2))
    bottom = min(height, max(y1, y2))

    new_w = right - left
    new_h = bottom - top

    cropped = []
    for y in range(top, bottom):
        for x in range(left, right):
            cropped.append(pixels[y * width + x])

    return cropped, new_w, new_h


def remove_area(pixels, width, height, x1, y1, x2, y2, fill_color=(255, 255, 255)):
    """
    Вилучає обрану область (зафарбовує її вказаним кольором).
    """
    left = max(0, min(x1, x2))
    right = min(width, max(x1, x2))
    top = max(0, min(y1, y2))
    bottom = min(height, max(y1, y2))

    result = []
    for y in range(height):
        for x in range(width):
            if left <= x < right and top <= y < bottom:
                result.append(fill_color)
            else:
                result.append(pixels[y * width + x])

    return result


# 3. Зміна контрастності

def change_contrast(pixels, k):
    """
    Зміна контрастності за формулою з методички:
    NewY = K * (OldY - AveY) + AveY
    """
    total = len(pixels)
    if total == 0:
        return pixels, (0, 0, 0)

    # 1. Знаходимо середнє значення кожного каналу (AveY)
    sum_r = sum(p[0] for p in pixels)
    sum_g = sum(p[1] for p in pixels)
    sum_b = sum(p[2] for p in pixels)

    ave_r = sum_r / total
    ave_g = sum_g / total
    ave_b = sum_b / total

    # 2. Перераховуємо кожен піксель
    result = []
    for p in pixels:
        new_r = int(k * (p[0] - ave_r) + ave_r)
        new_g = int(k * (p[1] - ave_g) + ave_g)
        new_b = int(k * (p[2] - ave_b) + ave_b)

        # Обмежуємо значення діапазоном 0..255
        new_r = max(0, min(255, new_r))
        new_g = max(0, min(255, new_g))
        new_b = max(0, min(255, new_b))

        if len(p) == 4:
            result.append((new_r, new_g, new_b, p[3]))
        else:
            result.append((new_r, new_g, new_b))

    return result, (round(ave_r, 1), round(ave_g, 1), round(ave_b, 1))
