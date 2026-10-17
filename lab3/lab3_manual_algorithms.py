# -*- coding: utf-8 -*-
"""
Власні алгоритми для Лабораторної роботи №3:
1. Попіксельне об'єднання (зшивання) двох зображень: горизонтально та вертикально.
2. Попіксельне накладання напівпрозорого шару водяного знаку (Alpha Blending).
"""


def merge_horizontal(pixels1, w1, h1, pixels2, w2, h2, bg_color=(255, 255, 255)):
    """
    Зшиває два зображення горизонтально (пліч-о-пліч).
    Нова ширина = w1 + w2, нова висота = max(h1, h2).
    """
    out_w = w1 + w2
    out_h = max(h1, h2)

    result = []
    for y in range(out_h):
        # Ліва частина (перше зображення)
        if y < h1:
            row_start1 = y * w1
            for x in range(w1):
                p = pixels1[row_start1 + x]
                result.append((p[0], p[1], p[2]))
        else:
            for _ in range(w1):
                result.append(bg_color)

        # Права частина (друге зображення)
        if y < h2:
            row_start2 = y * w2
            for x in range(w2):
                p = pixels2[row_start2 + x]
                result.append((p[0], p[1], p[2]))
        else:
            for _ in range(w2):
                result.append(bg_color)

    return result, out_w, out_h


def merge_vertical(pixels1, w1, h1, pixels2, w2, h2, bg_color=(255, 255, 255)):
    """
    Зшиває два зображення вертикально (одне під іншим).
    Нова ширина = max(w1, w2), нова висота = h1 + h2.
    """
    out_w = max(w1, w2)
    out_h = h1 + h2

    result = []

    # Верхнє зображення
    for y in range(h1):
        row_start = y * w1
        for x in range(out_w):
            if x < w1:
                p = pixels1[row_start + x]
                result.append((p[0], p[1], p[2]))
            else:
                result.append(bg_color)

    # Нижнє зображення
    for y in range(h2):
        row_start = y * w2
        for x in range(out_w):
            if x < w2:
                p = pixels2[row_start + x]
                result.append((p[0], p[1], p[2]))
            else:
                result.append(bg_color)

    return result, out_w, out_h


def blend_watermark(base_pixels, w, h, mark_pixels, opacity=0.5):
    """
    Накладає шар водяного знаку mark_pixels (RGBA) на базове зображення (RGB).
    Формула лінійного змішування: NewColor = MarkColor * a + BaseColor * (1 - a)
    """
    opacity = max(0.0, min(1.0, float(opacity)))
    result = []

    for i in range(w * h):
        base_r, base_g, base_b = base_pixels[i][0], base_pixels[i][1], base_pixels[i][2]
        mark_p = mark_pixels[i]

        mark_r, mark_g, mark_b = mark_p[0], mark_p[1], mark_p[2]
        mark_a = mark_p[3] / 255.0 if len(mark_p) == 4 else 1.0

        effective_a = mark_a * opacity

        if effective_a <= 0.0:
            result.append((base_r, base_g, base_b))
        else:
            new_r = int(mark_r * effective_a + base_r * (1.0 - effective_a))
            new_g = int(mark_g * effective_a + base_g * (1.0 - effective_a))
            new_b = int(mark_b * effective_a + base_b * (1.0 - effective_a))

            new_r = max(0, min(255, new_r))
            new_g = max(0, min(255, new_g))
            new_b = max(0, min(255, new_b))

            result.append((new_r, new_g, new_b))

    return result
