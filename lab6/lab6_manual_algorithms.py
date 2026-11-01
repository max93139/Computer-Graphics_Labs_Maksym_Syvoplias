# -*- coding: utf-8 -*-
"""
Математичні алгоритми для Лабораторної роботи №6 (Варіант 22).
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Тема: Оцінка якості фільтрації зображень за допомогою лінійних та нелінійних фільтрів.

Реалізація попіксельних алгоритмів:
- Моделювання 4 типів шумів (адитивний Гауса, імпульсний 'сіль і перець',
  просторово-нестаціонарний залежно від яскравості,
  просторово-нестаціонарний залежно від координат).
- 4 лінійних фільтри (усереднюючі 3х3, 5х5, Гауса 3х3, Гауса 5х5).
- 8 нелінійних фільтрів (медіанні 3х3, 5х5, 7х7, мінімум, максимум,
  середньої точки, альфа-усічений, адаптивний медіанний).
- Метрики спотворення та якості фільтрації (квадратичне відхилення, MSE, PSNR).
"""

import math
import random


def clamp_val(val, low=0, high=255):
    """
    Обмежує числове значення діапазоном [low, high] з приведенням до цілого.
    """
    if val < low:
        return low
    if val > high:
        return high
    return int(round(val))


def calculate_luminance(r, g, b):
    """
    Обчислює скалярну яскравість (люмінанс Y) для одного пікселя.
    Формула NTSC/BT.601: Y = 0.299*R + 0.587*G + 0.114*B.
    """
    return 0.299 * r + 0.587 * g + 0.114 * b


def add_gaussian_noise(pixels, width, height, mean=0.0, sigma=15.0, seed=None):
    """
    Додає адитивний шум з нормальним (гауссівським) розподілом N(mean, sigma^2).
    """
    if not pixels:
        return []
    rng = random.Random(seed)
    noisy_pixels = []
    for p in pixels:
        noise = rng.gauss(mean, sigma)
        nr = clamp_val(p[0] + noise)
        ng = clamp_val(p[1] + noise)
        nb = clamp_val(p[2] + noise)
        if len(p) == 4:
            noisy_pixels.append((nr, ng, nb, p[3]))
        else:
            noisy_pixels.append((nr, ng, nb))
    return noisy_pixels


def add_impulse_noise(pixels, width, height, prob=0.05, seed=None):
    """
    Додає імпульсний шум типу 'сіль і перець' з ймовірністю prob.
    Ймовірність prob/2 - білий піксель (сіль, 255), prob/2 - чорний (перець, 0).
    """
    if not pixels:
        return []
    rng = random.Random(seed)
    noisy_pixels = []
    half_prob = prob / 2.0
    for p in pixels:
        q = rng.random()
        if q < half_prob:
            val = 0
            if len(p) == 4:
                noisy_pixels.append((val, val, val, p[3]))
            else:
                noisy_pixels.append((val, val, val))
        elif q < prob:
            val = 255
            if len(p) == 4:
                noisy_pixels.append((val, val, val, p[3]))
            else:
                noisy_pixels.append((val, val, val))
        else:
            noisy_pixels.append(p)
    return noisy_pixels


def add_brightness_dependent_noise(pixels, width, height, alpha=1.5, seed=None):
    """
    Додає просторово-нестаціонарний адитивний шум, дисперсія якого
    залежить від рівня яскравості пікселя: sigma^2(Y) = alpha * Y.
    """
    if not pixels:
        return []
    rng = random.Random(seed)
    noisy_pixels = []
    for p in pixels:
        lum = calculate_luminance(p[0], p[1], p[2])
        sigma = math.sqrt(max(0.0, alpha * lum))
        noise = rng.gauss(0.0, sigma) if sigma > 0 else 0.0
        nr = clamp_val(p[0] + noise)
        ng = clamp_val(p[1] + noise)
        nb = clamp_val(p[2] + noise)
        if len(p) == 4:
            noisy_pixels.append((nr, ng, nb, p[3]))
        else:
            noisy_pixels.append((nr, ng, nb))
    return noisy_pixels


def add_spatial_coordinate_noise(pixels, width, height, sigma_min=5.0, sigma_max=35.0, mode='linear', seed=None):
    """
    Додає просторово-нестаціонарний адитивний шум, дисперсія якого є функцією
    просторових координат (x, y): лінійний градієнт або радіальна залежність.
    """
    if not pixels:
        return []
    rng = random.Random(seed)
    noisy_pixels = []
    max_dist = math.sqrt((width - 1) ** 2 + (height - 1) ** 2) if mode == 'radial' else float((width - 1) + (height - 1))

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            p = pixels[idx]

            if mode == 'linear':
                factor = (x + y) / max_dist if max_dist > 0 else 0.0
            else:
                cx = (width - 1) / 2.0
                cy = (height - 1) / 2.0
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                factor = d / (max_dist / 2.0) if max_dist > 0 else 0.0

            factor = max(0.0, min(1.0, factor))
            sigma = sigma_min + (sigma_max - sigma_min) * factor
            noise = rng.gauss(0.0, sigma)

            nr = clamp_val(p[0] + noise)
            ng = clamp_val(p[1] + noise)
            nb = clamp_val(p[2] + noise)
            if len(p) == 4:
                noisy_pixels.append((nr, ng, nb, p[3]))
            else:
                noisy_pixels.append((nr, ng, nb))
    return noisy_pixels


def get_box_filter_kernel(size):
    """
    Повертає ядро усереднюючого прямокутного фільтра розміром size x size.
    Кожен коефіцієнт дорівнює 1 / (size * size).
    """
    weight = 1.0 / (size * size)
    return [[weight for _ in range(size)] for _ in range(size)]


def get_gaussian_3x3_kernel():
    """
    Повертає нормалізоване цілочисельне наближення фільтра Гауса 3х3:
    [[1, 2, 1], [2, 4, 2], [1, 2, 1]] / 16.
    """
    base = [
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]
    return [[val / 16.0 for val in row] for row in base]


def get_gaussian_5x5_kernel():
    """
    Повертає нормалізоване дискретне ядро Гауса 5х5 з нормалізацією на 256.
    """
    base = [
        [1, 4, 6, 4, 1],
        [4, 16, 24, 16, 4],
        [6, 24, 36, 24, 6],
        [4, 16, 24, 16, 4],
        [1, 4, 6, 4, 1]
    ]
    return [[val / 256.0 for val in row] for row in base]


def apply_linear_filter(pixels, width, height, kernel):
    """
    Застосовує довільний лінійний фільтр (2D-згортку) з ядром довільного непарного розміру.
    Використовує крайову обробку методом реплікації граничних пікселів (clamp).
    """
    if not pixels:
        return []
    k_height = len(kernel)
    k_width = len(kernel[0])
    rad_y = k_height // 2
    rad_x = k_width // 2

    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            acc_r = 0.0
            acc_g = 0.0
            acc_b = 0.0

            for ky in range(-rad_y, rad_y + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                w_row = kernel[ky + rad_y]
                for kx in range(-rad_x, rad_x + 1):
                    px = min(max(x + kx, 0), width - 1)
                    w = w_row[kx + rad_x]
                    nbr = pixels[py_offset + px]
                    acc_r += nbr[0] * w
                    acc_g += nbr[1] * w
                    acc_b += nbr[2] * w

            fr = clamp_val(acc_r)
            fg = clamp_val(acc_g)
            fb = clamp_val(acc_b)

            if has_alpha:
                result_pixels.append((fr, fg, fb, pixels[y_offset + x][3]))
            else:
                result_pixels.append((fr, fg, fb))

    return result_pixels


def apply_median_filter(pixels, width, height, radius=1):
    """
    Застосовує медіанний нелінійний фільтр з вікном (2*radius + 1) x (2*radius + 1).
    Для radius=1 розмір вікна 3x3, для radius=2 розмір вікна 5x5, для radius=3 - 7x7.
    """
    if not pixels:
        return []
    size = 2 * radius + 1
    total_elements = size * size
    med_index = total_elements // 2
    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            r_vals = []
            g_vals = []
            b_vals = []

            for ky in range(-radius, radius + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                for kx in range(-radius, radius + 1):
                    px = min(max(x + kx, 0), width - 1)
                    nbr = pixels[py_offset + px]
                    r_vals.append(nbr[0])
                    g_vals.append(nbr[1])
                    b_vals.append(nbr[2])

            r_vals.sort()
            g_vals.sort()
            b_vals.sort()

            mr = r_vals[med_index]
            mg = g_vals[med_index]
            mb = b_vals[med_index]

            if has_alpha:
                result_pixels.append((mr, mg, mb, pixels[y_offset + x][3]))
            else:
                result_pixels.append((mr, mg, mb))

    return result_pixels


def apply_min_filter(pixels, width, height, radius=1):
    """
    Застосовує нелінійний мінімальний фільтр (морфологічна ерозія відтінків) у вікні.
    """
    if not pixels:
        return []
    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            min_r = 255
            min_g = 255
            min_b = 255

            for ky in range(-radius, radius + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                for kx in range(-radius, radius + 1):
                    px = min(max(x + kx, 0), width - 1)
                    nbr = pixels[py_offset + px]
                    if nbr[0] < min_r:
                        min_r = nbr[0]
                    if nbr[1] < min_g:
                        min_g = nbr[1]
                    if nbr[2] < min_b:
                        min_b = nbr[2]

            if has_alpha:
                result_pixels.append((min_r, min_g, min_b, pixels[y_offset + x][3]))
            else:
                result_pixels.append((min_r, min_g, min_b))

    return result_pixels


def apply_max_filter(pixels, width, height, radius=1):
    """
    Застосовує нелінійний максимальний фільтр (морфологічна дилатація відтінків) у вікні.
    """
    if not pixels:
        return []
    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            max_r = 0
            max_g = 0
            max_b = 0

            for ky in range(-radius, radius + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                for kx in range(-radius, radius + 1):
                    px = min(max(x + kx, 0), width - 1)
                    nbr = pixels[py_offset + px]
                    if nbr[0] > max_r:
                        max_r = nbr[0]
                    if nbr[1] > max_g:
                        max_g = nbr[1]
                    if nbr[2] > max_b:
                        max_b = nbr[2]

            if has_alpha:
                result_pixels.append((max_r, max_g, max_b, pixels[y_offset + x][3]))
            else:
                result_pixels.append((max_r, max_g, max_b))

    return result_pixels


def apply_midpoint_filter(pixels, width, height, radius=1):
    """
    Застосовує нелінійний фільтр середньої точки (Midpoint Filter):
    Нове значення = (min + max) / 2.
    Ефективний для шуму з рівномірним або гауссівським розподілом на малих вибірках.
    """
    if not pixels:
        return []
    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            min_r, max_r = 255, 0
            min_g, max_g = 255, 0
            min_b, max_b = 255, 0

            for ky in range(-radius, radius + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                for kx in range(-radius, radius + 1):
                    px = min(max(x + kx, 0), width - 1)
                    nbr = pixels[py_offset + px]
                    if nbr[0] < min_r:
                        min_r = nbr[0]
                    if nbr[0] > max_r:
                        max_r = nbr[0]
                    if nbr[1] < min_g:
                        min_g = nbr[1]
                    if nbr[1] > max_g:
                        max_g = nbr[1]
                    if nbr[2] < min_b:
                        min_b = nbr[2]
                    if nbr[2] > max_b:
                        max_b = nbr[2]

            mid_r = clamp_val((min_r + max_r) / 2.0)
            mid_g = clamp_val((min_g + max_g) / 2.0)
            mid_b = clamp_val((min_b + max_b) / 2.0)

            if has_alpha:
                result_pixels.append((mid_r, mid_g, mid_b, pixels[y_offset + x][3]))
            else:
                result_pixels.append((mid_r, mid_g, mid_b))

    return result_pixels


def apply_alpha_trimmed_mean_filter(pixels, width, height, radius=1, d=4):
    """
    Застосовує альфа-усічений усереднюючий фільтр (Alpha-trimmed Mean Filter):
    У вікні 3х3 (9 елементів) відкидає d/2 найменших і d/2 найбільших значень,
    а потім обчислює середнє арифметичне решти (9 - d) елементів.
    """
    if not pixels:
        return []
    size = 2 * radius + 1
    total = size * size
    low_trim = d // 2
    high_trim = total - low_trim
    count = high_trim - low_trim
    if count <= 0:
        count = 1
        low_trim = 0
        high_trim = total

    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            r_vals = []
            g_vals = []
            b_vals = []

            for ky in range(-radius, radius + 1):
                py = min(max(y + ky, 0), height - 1)
                py_offset = py * width
                for kx in range(-radius, radius + 1):
                    px = min(max(x + kx, 0), width - 1)
                    nbr = pixels[py_offset + px]
                    r_vals.append(nbr[0])
                    g_vals.append(nbr[1])
                    b_vals.append(nbr[2])

            r_vals.sort()
            g_vals.sort()
            b_vals.sort()

            avg_r = sum(r_vals[low_trim:high_trim]) / float(count)
            avg_g = sum(g_vals[low_trim:high_trim]) / float(count)
            avg_b = sum(b_vals[low_trim:high_trim]) / float(count)

            if has_alpha:
                result_pixels.append((clamp_val(avg_r), clamp_val(avg_g), clamp_val(avg_b), pixels[y_offset + x][3]))
            else:
                result_pixels.append((clamp_val(avg_r), clamp_val(avg_g), clamp_val(avg_b)))

    return result_pixels


def apply_adaptive_median_filter(pixels, width, height, max_radius=2):
    """
    Застосовує адаптивний медіанний фільтр (Adaptive Median Filter).
    Динамічно змінює розмір вікна від 3x3 (radius=1) до max_radius (наприклад, 5x5 чи 7x7),
    зберігаючи текстури та усуваючи високу щільність імпульсного шуму.
    """
    if not pixels:
        return []
    has_alpha = (len(pixels[0]) == 4)
    result_pixels = []

    for y in range(height):
        y_offset = y * width
        for x in range(width):
            curr_p = pixels[y_offset + x]
            out_c = []

            for c in range(3):
                z_xy = curr_p[c]
                r = 1
                filtered_val = z_xy

                while r <= max_radius:
                    vals = []
                    for ky in range(-r, r + 1):
                        py = min(max(y + ky, 0), height - 1)
                        py_offset = py * width
                        for kx in range(-r, r + 1):
                            px = min(max(x + kx, 0), width - 1)
                            vals.append(pixels[py_offset + px][c])

                    vals.sort()
                    z_min = vals[0]
                    z_max = vals[-1]
                    z_med = vals[len(vals) // 2]

                    a1 = z_med - z_min
                    a2 = z_med - z_max

                    if a1 > 0 and a2 < 0:
                        b1 = z_xy - z_min
                        b2 = z_xy - z_max
                        if b1 > 0 and b2 < 0:
                            filtered_val = z_xy
                        else:
                            filtered_val = z_med
                        break
                    else:
                        r += 1
                        if r > max_radius:
                            filtered_val = z_med

                out_c.append(filtered_val)

            if has_alpha:
                result_pixels.append((out_c[0], out_c[1], out_c[2], curr_p[3]))
            else:
                result_pixels.append((out_c[0], out_c[1], out_c[2]))

    return result_pixels


def calculate_mse(pixels_a, pixels_b):
    """
    Обчислює середньоквадратичну похибку (MSE) між двома наборами пікселів.
    Формула: MSE = (1 / (N * M * 3)) * sum(|a - b|^2)
    """
    if not pixels_a or not pixels_b:
        return 0.0

    if len(pixels_a) != len(pixels_b):
        raise ValueError("Розміри масивів пікселів для порівняння не збігаються.")

    total_diff_sq = 0.0
    for p_a, p_b in zip(pixels_a, pixels_b):
        dr = p_a[0] - p_b[0]
        dg = p_a[1] - p_b[1]
        db = p_a[2] - p_b[2]
        total_diff_sq += dr * dr + dg * dg + db * db

    mse = total_diff_sq / (len(pixels_a) * 3.0)
    return mse


def calculate_distortion(pixels_filtered, pixels_original):
    """
    Обчислює величину спотворення / квадратичного відхилення (epsilon^2):
    epsilon^2 = (1 / (N * M)) * sum(|g(i,j) - f(i,j)|^2).
    """
    return calculate_mse(pixels_filtered, pixels_original)


def calculate_psnr(pixels_filtered, pixels_ground_truth):
    """
    Обчислює пікове відношення сигналу до шуму (PSNR) у децибелах (дБ):
    PSNR = 10 * log10(255^2 / MSE).
    """
    mse = calculate_mse(pixels_filtered, pixels_ground_truth)
    if mse <= 1e-10:
        return 99.99
    return 10.0 * math.log10((255.0 * 255.0) / mse)
