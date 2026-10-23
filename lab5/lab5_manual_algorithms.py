# -*- coding: utf-8 -*-
"""
Власні попіксельні алгоритми для Лабораторної роботи №5 (Варіант 22).
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Варіант 22: Застосування курсової маски схід (East compass / directional edge detection mask).

Алгоритм базується на просторовій 2D-згортці (конволюції) 3x3 над значеннями
люмінансу (яскравості) пікселів згідно стандарту ITU-R BT.601:
  Y = 0.299 * R + 0.587 * G + 0.114 * B

Курсова маска 'Схід' (East compass mask):
  [-1,  0,  1]
  [-1,  0,  1] (або маска Собеля для сходу [-1, 0, 1; -2, 0, 2; -1, 0, 1])
  [-1,  0,  1]
"""


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


def get_east_compass_kernel(kernel_type='prewitt'):
    """
    Повертає ядро курсової маски 'Схід' 3x3.
    Підтримуються стандартні класичні варіації:
    - 'prewitt' (рівномірна курсова маска):
        [[-1, 0, 1],
         [-1, 0, 1],
         [-1, 0, 1]]
    - 'sobel' (зважена курсова маска):
        [[-1, 0, 1],
         [-2, 0, 2],
         [-1, 0, 1]]
    - 'robinson' / 'kirsch_east' (компасна маска Робінсона/Кірша на схід):
        [[-1, 0, 1],
         [-2, 0, 2],
         [-1, 0, 1]]
    """
    if kernel_type == 'sobel':
        return [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
    elif kernel_type == 'robinson':
        return [
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ]
    return [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]


def apply_east_compass_mask(pixels, width, height, kernel_type='prewitt', offset=0, threshold=None):
    """
    Застосовує курсову маску 'Схід' до зображення.
    
    Параметри:
      pixels: одновимірний список кортежів пікселів (R, G, B) або (R, G, B, A)
      width, height: розміри зображення
      kernel_type: 'prewitt' або 'sobel'
      offset: зсув яскравості (наприклад, +100 або 128 для збереження фону)
      threshold: необов'язковий поріг бінаризації виділених меж
      
    Повертає:
      новий одновимірний список пікселів (R, G, B) у градаціях сірого
    """
    matrix = get_brightness_plane(pixels, width, height)
    kernel = get_east_compass_kernel(kernel_type)

    result_pixels = []

    for y in range(height):
        for x in range(width):
            # Обробка граничних пікселів (крайові умови з реплікацією сусідів)
            val = 0
            for ky in range(-1, 2):
                py = min(max(y + ky, 0), height - 1)
                for kx in range(-1, 2):
                    px = min(max(x + kx, 0), width - 1)
                    val += matrix[py][px] * kernel[ky + 1][kx + 1]

            if offset != 0:
                val = val + offset
            else:
                val = abs(val)

            # Обмеження діапазону [0..255]
            val = max(0, min(255, int(round(val))))

            if threshold is not None:
                val = 255 if val >= threshold else 0

            result_pixels.append((val, val, val))

    return result_pixels


def apply_convolution_rgb(pixels, width, height, kernel, offset=0):
    """
    Застосовує довільну матрицю згортки 3x3 окремо до кожного каналу R, G, B.
    """
    result = []
    for y in range(height):
        for x in range(width):
            r_acc, g_acc, b_acc = 0, 0, 0
            for ky in range(-1, 2):
                py = min(max(y + ky, 0), height - 1)
                for kx in range(-1, 2):
                    px = min(max(x + kx, 0), width - 1)
                    idx = py * width + px
                    p = pixels[idx]
                    weight = kernel[ky + 1][kx + 1]
                    r_acc += p[0] * weight
                    g_acc += p[1] * weight
                    b_acc += p[2] * weight

            if offset != 0:
                r_val = r_acc + offset
                g_val = g_acc + offset
                b_val = b_acc + offset
            else:
                r_val = abs(r_acc)
                g_val = abs(g_acc)
                b_val = abs(b_acc)

            r_val = max(0, min(255, int(round(r_val))))
            g_val = max(0, min(255, int(round(g_val))))
            b_val = max(0, min(255, int(round(b_val))))

            result.append((r_val, g_val, b_val))
    return result
