# -*- coding: utf-8 -*-
"""
Власні алгоритми для Лабораторної роботи №4:
1. Розрахунок матриці значень яскравості за формулою:
   Y = 0.299 * R + 0.587 * G + 0.114 * B
2. Побудова гістограми розподілу яскравості (поканально та сумарно).
3. Зміна кольоровості:
   - Бінаризація за порогом P (чорно-біле)
   - Перехід до відтінків сірого (R = G = B = Y)
   - Створення негативу (New = 255 - Old)
"""


def calculate_pixel_brightness(r, g, b):
    """
    Обчислює яскравість одного пікселя за стандартною формулою люмінансу:
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    """
    val = int(round(0.299 * r + 0.587 * g + 0.114 * b))
    return max(0, min(255, val))


def calculate_brightness_matrix(pixels, width, height):
    """
    Створює двовимірну матрицю значень яскравості Y розміром height x width.
    """
    matrix = []
    for y in range(height):
        row = []
        row_offset = y * width
        for x in range(width):
            p = pixels[row_offset + x]
            row.append(calculate_pixel_brightness(p[0], p[1], p[2]))
        matrix.append(row)
    return matrix


def build_histogram(values):
    """
    Будує гістограму розподілу інтенсивностей (список частот для значень 0..255).
    """
    hist = [0] * 256
    for val in values:
        v = max(0, min(255, int(val)))
        hist[v] += 1
    return hist


def to_grayscale(pixels):
    """
    Перетворює повнокольорове зображення у відтінки сірого:
    R = G = B = Y
    """
    result = []
    for p in pixels:
        y = calculate_pixel_brightness(p[0], p[1], p[2])
        if len(p) == 4:
            result.append((y, y, y, p[3]))
        else:
            result.append((y, y, y))
    return result


def binarize(pixels, threshold=128):
    """
    Бінаризація зображення за порогом P:
    Якщо Y <= P -> 0 (чорний)
    Якщо Y > P  -> 255 (білий)
    """
    p_val = max(0, min(255, int(threshold)))
    result = []
    for p in pixels:
        y = calculate_pixel_brightness(p[0], p[1], p[2])
        bw = 255 if y > p_val else 0
        if len(p) == 4:
            result.append((bw, bw, bw, p[3]))
        else:
            result.append((bw, bw, bw))
    return result


def to_negative(pixels):
    """
    Створення фотографічного негативу:
    NewC = 255 - OldC для кожного колірного каналу.
    """
    result = []
    for p in pixels:
        inv_r = 255 - p[0]
        inv_g = 255 - p[1]
        inv_b = 255 - p[2]
        if len(p) == 4:
            result.append((inv_r, inv_g, inv_b, p[3]))
        else:
            result.append((inv_r, inv_g, inv_b))
    return result
