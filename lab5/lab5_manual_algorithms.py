# -*- coding: utf-8 -*-
"""
Власні попіксельні алгоритми для Лабораторної роботи №5 (Варіант 22).
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Варіант 22: Застосування курсової маски схід (East compass mask).
Також реалізовано алгоритм зашумлення (додавання імпульсного шуму)
згідно з теоретичними відомостями практикуму (стор. 69-70).
"""

import random


def calculate_pixel_brightness(r, g, b):
    """
    Обчислює скалярну яскравість (люмінанс Y) для одного пікселя.
    Формула: Y = round(0.299*R + 0.587*G + 0.114*B)
    """
    y = int(round(0.299 * r + 0.587 * g + 0.114 * b))
    return max(0, min(255, y))


def get_brightness_plane(pixels, width, height):
    """
    Формує двовимірну матрицю значень яскравості для зображення.
    """
    plane = []
    for y in range(height):
        row = []
        row_offset = y * width
        for x in range(width):
            p = pixels[row_offset + x]
            row.append(calculate_pixel_brightness(p[0], p[1], p[2]))
        plane.append(row)
    return plane


def add_noise(pixels, width, height, count=500, noise_color=(0, 0, 0)):
    """
    Додає штучний імпульсний шум (випадкові точки) до зображення.
    Реалізація за принципом з методичних вказівок (стор. 69-70):
    випадкові точки отримують заданий колір (наприклад, чорний або білий).
    """
    noisy_pixels = list(pixels)
    for _ in range(count):
        rx = random.randint(0, width - 1)
        ry = random.randint(0, height - 1)
        idx = ry * width + rx
        if len(noisy_pixels[idx]) == 4:
            noisy_pixels[idx] = (noise_color[0], noise_color[1], noise_color[2], noisy_pixels[idx][3])
        else:
            noisy_pixels[idx] = noise_color
    return noisy_pixels


def get_east_compass_kernel():
    """
    Повертає класичне ядро курсової маски 'Схід' 3x3:
      [-1,  0,  1]
      [-1,  0,  1]
      [-1,  0,  1]
    """
    return [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]


def apply_east_compass_mask(pixels, width, height):
    """
    Застосовує курсову маску 'Схід' до зображення.
    Обчислює просторову згортку 3x3 для виділення контурів зі східного напрямку.
    """
    matrix = get_brightness_plane(pixels, width, height)
    kernel = get_east_compass_kernel()

    result_pixels = []

    for y in range(height):
        for x in range(width):
            val = 0
            for ky in range(-1, 2):
                py = min(max(y + ky, 0), height - 1)
                for kx in range(-1, 2):
                    px = min(max(x + kx, 0), width - 1)
                    val += matrix[py][px] * kernel[ky + 1][kx + 1]

            val = max(0, min(255, abs(int(round(val)))))
            result_pixels.append((val, val, val))

    return result_pixels
