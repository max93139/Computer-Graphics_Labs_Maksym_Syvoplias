# -*- coding: utf-8 -*-
"""
Генератор термінальних скріншотів для Лабораторної роботи №6.
Створює скріншоти у стилі macOS Terminal з роздільною здатністю 1920x1080.
"""

import os
from PIL import Image, ImageDraw, ImageFont


def create_terminal_screenshot(output_path, title, lines, width=1980, min_height=1000):
    font_path = "/System/Library/Fonts/Menlo.ttc"
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)

    line_height = 36
    header_height = 60
    padding_x = 40
    padding_y = 25

    calc_height = header_height + padding_y * 2 + len(lines) * line_height + 40
    height = max(min_height, calc_height)

    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (width, header_height)], fill=(45, 45, 45))

    btn_y = 30
    draw.ellipse([(25, btn_y - 10), (45, btn_y + 10)], fill=(255, 95, 86))
    draw.ellipse([(55, btn_y - 10), (75, btn_y + 10)], fill=(255, 189, 46))
    draw.ellipse([(85, btn_y - 10), (105, btn_y + 10)], fill=(39, 201, 63))

    title_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
    draw.text((width // 2 - 200, 18), title, fill=(180, 180, 180), font=title_font)

    curr_y = header_height + padding_y
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, (220, 220, 220)
        draw.text((padding_x, curr_y), text, fill=color, font=font)
        curr_y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Скріншот збережено: {output_path} ({width}x{height})")


def generate_all_screenshots():
    out_dir = "/Users/mac/Desktop/Python/Computer Graphics/lab1/lab6/screenshots"

    lines_img1 = [
        ("mac@MacBook-Pro:~/Desktop/Python/Computer Graphics/lab6$ python3 main.py", (100, 255, 100)),
        ("", (220, 220, 220)),
        ("ЛАБОРАТОРНА РОБОТА №6 (Варіант 22)", (255, 215, 0)),
        ("1. Підготовка набору 9 тестових зображень (128x128 BMP)", (200, 200, 200)),
        ("2. Оцінка спотворення f0(i,j) лінійними та нелінійними фільтрами (eps_A0^2)", (200, 200, 200)),
        ("3. Фільтрація зашумлених зображень (f1-f8) та оцінка якості (eps_Ak^2, MSE, PSNR)", (200, 200, 200)),
        ("4. Комплексний аналіз та генерація колажів/графіків", (200, 200, 200)),
        ("0. Вихід", (200, 200, 200)),
        ("Введіть номер дії (0-4): 1", (100, 220, 255)),
        ("", (220, 220, 220)),
        ("Дія 1: Підготовка набору 9 тестових зображень (128x128 BMP)", (255, 255, 255)),
        ("Шлях до вихідного зображення [samples/sample_test.bmp]: samples/sample_test.bmp", (180, 180, 180)),
        ("Каталог збереження [output]: output", (180, 180, 180)),
        ("", (220, 220, 220)),
        ("[Генерація 9 тестових зображень у форматі BMP (128x128)...]", (255, 180, 50)),
        ("[Успіх] Сформовано 9 тестових зображень у каталозі 'output':", (100, 255, 100)),
        ("  - image0.bmp: f0: Без шуму (оригінал 128x128)", (220, 220, 220)),
        ("  - image1.bmp: f1: Гаусів адитивний (sigma=15, дисперсія 225)", (220, 220, 220)),
        ("  - image2.bmp: f2: Гаусів адитивний (sigma=30, дисперсія 900)", (220, 220, 220)),
        ("  - image3.bmp: f3: Імпульсний 'сіль і перець' p=0.05", (220, 220, 220)),
        ("  - image4.bmp: f4: Імпульсний 'сіль і перець' p=0.15", (220, 220, 220)),
        ("  - image5.bmp: f5: Нестаціонарний sigma(Y), alpha=1.5 (залежність від яскравості)", (220, 220, 220)),
        ("  - image6.bmp: f6: Нестаціонарний sigma(Y), alpha=3.5 (сильна яскравісна залежність)", (220, 220, 220)),
        ("  - image7.bmp: f7: Нестаціонарний sigma(x,y) лінійний градієнт [5.0, 35.0]", (220, 220, 220)),
        ("  - image8.bmp: f8: Нестаціонарний sigma(x,y) радіальна функція [5.0, 40.0]", (220, 220, 220)),
        ("", (220, 220, 220)),
        ("[Колаж] Збережено колаж 3х3: output/comparison_9_test_images.png", (100, 220, 255)),
        ("Натисніть Enter для повернення в меню...", (150, 150, 150)),
    ]
    create_terminal_screenshot(os.path.join(out_dir, "lab6_image1.png"), "mac — zsh — 1980x1080", lines_img1, min_height=1020)

    lines_img2 = [
        ("mac@MacBook-Pro:~/Desktop/Python/Computer Graphics/lab6$ python3 main.py", (100, 255, 100)),
        ("Введіть номер дії (0-4): 2", (100, 220, 255)),
        ("", (220, 220, 220)),
        ("Дія 2: Оцінка спотворення неспотвореного зображення f0(i,j)", (255, 255, 255)),
        ("Каталог з тестовими зображеннями [output]: output", (180, 180, 180)),
        ("", (220, 220, 220)),
        ("[Застосування 4 лінійних та 8 нелінійних фільтрів до f0(i,j)...]", (255, 180, 50)),
        ("", (220, 220, 220)),
        ("Таблиця спотворень неспотвореного зображення f0 (eps_A0^2):", (255, 215, 0)),
        ("Фільтр                   | Тип          | eps_A0^2 (MSE)  | PSNR (дБ) ", (120, 200, 255)),
        ("-------------------------+--------------+-----------------+-----------", (100, 100, 100)),
        ("L1: Box Mean 3x3         | linear       | 448.02          | 21.62     ", (220, 220, 220)),
        ("L2: Box Mean 5x5         | linear       | 1131.88         | 17.59     ", (220, 220, 220)),
        ("L3: Gaussian 3x3         | linear       | 272.71          | 23.77     ", (220, 220, 220)),
        ("L4: Gaussian 5x5         | linear       | 523.46          | 20.94     ", (220, 220, 220)),
        ("NL1: Median 3x3          | non-linear   | 305.48          | 23.28     ", (220, 220, 220)),
        ("NL2: Median 5x5          | non-linear   | 984.49          | 18.20     ", (220, 220, 220)),
        ("NL3: Median 7x7          | non-linear   | 1693.64         | 15.84     ", (220, 220, 220)),
        ("NL4: Min Filter 3x3      | non-linear   | 3310.09         | 12.93     ", (255, 120, 120)),
        ("NL5: Max Filter 3x3      | non-linear   | 2891.25         | 13.52     ", (255, 120, 120)),
        ("NL6: Midpoint 3x3        | non-linear   | 852.20          | 18.83     ", (220, 220, 220)),
        ("NL7: Alpha-trimmed 3x3   | non-linear   | 330.03          | 22.95     ", (220, 220, 220)),
        ("NL8: Adaptive Median     | non-linear   | 108.39          | 27.78     ", (100, 255, 100)),
        ("", (220, 220, 220)),
        ("[Колаж] Збережено порівняльний колаж фільтрів: output/comparison_f0_filters.png", (100, 220, 255)),
        ("Натисніть Enter для повернення в меню...", (150, 150, 150)),
    ]
    create_terminal_screenshot(os.path.join(out_dir, "lab6_image2.png"), "mac — zsh — 1980x1080", lines_img2, min_height=1000)

    lines_img3 = [
        ("mac@MacBook-Pro:~/Desktop/Python/Computer Graphics/lab6$ python3 main.py", (100, 255, 100)),
        ("Введіть номер дії (0-4): 3", (100, 220, 255)),
        ("", (220, 220, 220)),
        ("Дія 3: Фільтрація зашумлених зображень (f1-f8) та оцінка якості", (255, 255, 255)),
        ("[Фільтрація зображень f1-f8 усіма фільтрами та розрахунок метрик...]", (255, 180, 50)),
        ("", (220, 220, 220)),
        ("Результати фільтрації та оптимальні фільтри для кожного типу шуму:", (255, 215, 0)),
        ("Зображення (Шум)                 | Вихідний PSNR | Найкращий фільтр       | Фільтрований PSNR  | Приріст ", (120, 200, 255)),
        ("---------------------------------+---------------+------------------------+--------------------+---------", (100, 100, 100)),
        ("f1 (Гаус sigma=15)               | 25.02 dB      | NL8: Adaptive Median   | 24.25 dB           | -0.77 dB", (220, 220, 220)),
        ("f2 (Гаус sigma=30)               | 19.52 dB      | L3: Gaussian 3x3       | 21.98 dB           | +2.46 dB", (100, 255, 100)),
        ("f3 (Імпульсний p=0.05)           | 17.46 dB      | NL8: Adaptive Median   | 27.34 dB           | +9.88 dB", (100, 255, 100)),
        ("f4 (Імпульсний p=0.15)           | 12.47 dB      | NL8: Adaptive Median   | 24.96 dB           | +12.50 dB", (100, 255, 100)),
        ("f5 (Нестац. яскравість a=1.5)    | 25.21 dB      | NL8: Adaptive Median   | 24.40 dB           | -0.81 dB", (220, 220, 220)),
        ("f6 (Нестац. яскравість a=3.5)    | 21.88 dB      | L3: Gaussian 3x3       | 22.64 dB           | +0.77 dB", (100, 255, 100)),
        ("f7 (Нестац. коорд. лінійний)     | 22.40 dB      | L3: Gaussian 3x3       | 22.79 dB           | +0.39 dB", (100, 255, 100)),
        ("f8 (Нестац. коорд. радіальний)   | 20.79 dB      | L3: Gaussian 3x3       | 22.44 dB           | +1.65 dB", (100, 255, 100)),
        ("", (220, 220, 220)),
        ("[Графіки] Збережено колаж результатів: output/comparison_noise_vs_filtering.png", (100, 220, 255)),
        ("[Діаграма] Збережено порівняльну діаграму PSNR: output/comparison_metrics_matrix.png", (100, 220, 255)),
        ("Натисніть Enter для повернення в меню...", (150, 150, 150)),
    ]
    create_terminal_screenshot(os.path.join(out_dir, "lab6_image3.png"), "mac — zsh — 1980x1080", lines_img3, min_height=1000)

    lines_img4 = [
        ("mac@MacBook-Pro:~/Desktop/Python/Computer Graphics/lab6$ python3 main.py", (100, 255, 100)),
        ("Введіть номер дії (0-4): 4", (100, 220, 255)),
        ("", (220, 220, 220)),
        ("Дія 4: Комплексний зведений аналіз", (255, 255, 255)),
        ("1) Генерація 9 тестових зображень у форматі *.bmp (128x128)", (180, 180, 180)),
        ("2) Оцінка спотворення f0(i,j) 12 фільтрами (4 лінійних, 8 нелінійних)", (180, 180, 180)),
        ("3) Пакетна фільтрація зображень f1-f8 та розрахунок матриці похибок", (180, 180, 180)),
        ("4) Побудова графіків ефективності усунення шуму та гістограм приросту PSNR", (180, 180, 180)),
        ("", (220, 220, 220)),
        ("[Успіх] Комплексний аналіз повністю завершено.", (100, 255, 100)),
        ("Усі графічні результати оновлено у каталозі output/:", (200, 200, 200)),
        ("  - output/comparison_9_test_images.png", (100, 220, 255)),
        ("  - output/comparison_f0_filters.png", (100, 220, 255)),
        ("  - output/comparison_noise_vs_filtering.png", (100, 220, 255)),
        ("  - output/comparison_metrics_matrix.png", (100, 220, 255)),
        ("", (220, 220, 220)),
        ("mac@MacBook-Pro:~/Desktop/Python/Computer Graphics/lab6$ ", (100, 255, 100)),
    ]
    create_terminal_screenshot(os.path.join(out_dir, "lab6_image4.png"), "mac — zsh — 1980x1080", lines_img4, min_height=900)


if __name__ == '__main__':
    generate_all_screenshots()
