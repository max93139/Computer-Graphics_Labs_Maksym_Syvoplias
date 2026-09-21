# -*- coding: utf-8 -*-
"""
Головний виконуваний файл консольного проєкту Lab 1.
Дисципліна: 'Комп'ютерна графіка та візуалізація'

Лабораторна робота №1
Тема: Розробка програми для обробки зображень:
      конвертація форматів, зміна розміру, перетворення кольорів
      та корекція колірного балансу (з власними алгоритмами).
"""

import os
import glob
from image_converter import (
    convert_format,
    batch_convert_formats,
    resize_image,
    batch_resize_images,
    replace_color,
    adjust_color_balance,
    auto_color_balance
)


def clear_console():
    print("\033c\033[2J\033[H\033[3J", end="", flush=True)
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    print(f"\n[{title}]")


def handle_format_conversion():
    print_header("ЗАВДАННЯ 1: КОНВЕРТАЦІЯ ФОРМАТІВ ЗОБРАЖЕНЬ")
    print("1. Конвертувати одне зображення")
    print("2. Конвертувати декілька зображень (пакетна обробка папки)")
    mode = input("Оберіть режим [1/2, за замовчуванням 1]: ").strip() or "1"

    print("\nОберіть бажаний вихідний формат:")
    print("  1. PNG")
    print("  2. JPEG")
    print("  3. BMP")
    print("  4. TIFF")
    print("  5. WEBP")
    fmt_choice = input("Формат [1-5, за замовчуванням 1]: ").strip() or "1"
    format_map = {
        "1": "PNG",
        "2": "JPEG",
        "3": "BMP",
        "4": "TIFF",
        "5": "WEBP",
        "PNG": "PNG",
        "JPEG": "JPEG",
        "JPG": "JPEG",
        "BMP": "BMP",
        "TIFF": "TIFF",
        "WEBP": "WEBP",
    }
    target_format = format_map.get(fmt_choice.upper(), "PNG")

    if mode == "1":
        default_in = "samples/sample_gradient.jpg"
        input_file = input(f"\nВведіть шлях до файлу [{default_in}]: ").strip() or default_in
        if not os.path.exists(input_file):
            print(f"[Помилка] Файл '{input_file}' не знайдено.")
            return

        ext = target_format.lower()
        if ext == 'jpeg':
            ext = 'jpg'
        file_stem = os.path.splitext(os.path.basename(input_file))[0]
        default_out = f"output/{file_stem}_converted.{ext}"
        out_file = input(f"Введіть шлях для збереження [{default_out}]: ").strip() or default_out
        print("\n[Обробка...]")
        res = convert_format(input_file, target_format, out_file)
        
        print("\n[Результат конвертації]:")
        print(f"  • Вхідний файл:   {res['input_path']} -> {res['initial_size_str']}")
        print(f"  • Вихідний файл:  {res['output_path']} -> {res['final_size_str']}")
        print(f"  • Формат:         {res['format']}")
        print(f"  • Зміна розміру:  {res['diff_percent']:+.2f}%")
    else:
        in_dir = input("\nВведіть вхідну папку [samples]: ").strip() or "samples"
        out_dir = input("Введіть вихідну папку [output/converted]: ").strip() or "output/converted"
        
        images = []
        for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp', '*.tiff'):
            images.extend(glob.glob(os.path.join(in_dir, ext)))

        if not images:
            print(f"[Помилка] У папці '{in_dir}' не знайдено зображень.")
            return

        print(f"\n[Обробка {len(images)} файлів...]")
        results = batch_convert_formats(images, target_format, out_dir)
        print("\n[Результати пакетної конвертації]:")
        for r in results:
            print(f"  • {os.path.basename(r['input_path'])} ({r['initial_size_str']}) -> {os.path.basename(r['output_path'])} ({r['final_size_str']}) [{r['diff_percent']:+.2f}%]")


def handle_resize():
    print_header("ЗАВДАННЯ 2: ЗМІНА РОЗМІРУ ЗОБРАЖЕНЬ (ВЛАСНА ІНТЕРПОЛЯЦІЯ)")
    print("1. Змінити розмір одного зображення")
    print("2. Змінити розмір декількох зображень (пакетна обробка папки)")
    mode = input("Оберіть режим [1/2, за замовчуванням 1]: ").strip() or "1"

    print("\nОберіть алгоритм інтерполяції:")
    print("  1. Білінійна інтерполяція (Bilinear) - плавна якість")
    print("  2. Інтерполяція найближчого сусіда (Nearest Neighbor) - швидка піксельна")
    algo_choice = input("Алгоритм [1/2, за замовчуванням 1]: ").strip() or "1"
    method = 'bilinear' if algo_choice == '1' else 'nearest'

    print("\nТипи зміни розміру:")
    print("  A. За відсотком масштабування (наприклад, 50%)")
    print("  B. За шириною (висота обчислюється автоматично для збереження пропорцій)")
    print("  C. За висотою (ширина обчислюється автоматично для збереження пропорцій)")
    print("  D. Точні ширина і висота (без збереження пропорцій)")
    resize_type = input("Оберіть тип [A/B/C/D, за замовчуванням A]: ").strip().upper() or "A"

    width, height, scale, keep_ratio = None, None, None, True

    if resize_type == "A":
        scale = float(input("Введіть відсоток масштабування [50]: ").strip() or "50")
    elif resize_type == "B":
        width = int(input("Введіть нову ширину (px) [200]: ").strip() or "200")
    elif resize_type == "C":
        height = int(input("Введіть нову висоту (px) [150]: ").strip() or "150")
    elif resize_type == "D":
        width = int(input("Введіть ширину (px) [300]: ").strip() or "300")
        height = int(input("Введіть висоту (px) [200]: ").strip() or "200")
        keep_ratio = False

    if mode == "1":
        default_in = "samples/sample_palette.png"
        input_file = input(f"\nВведіть шлях до файлу [{default_in}]: ").strip() or default_in
        if not os.path.exists(input_file):
            print(f"[Помилка] Файл '{input_file}' не знайдено.")
            return

        out_file = input("Введіть вихідний шлях [output/resized_sample.png]: ").strip() or "output/resized_sample.png"
        print("\n[Обробка власним алгоритмом...]")
        res = resize_image(input_file, out_file, width=width, height=height, scale_percent=scale, keep_aspect_ratio=keep_ratio, method=method)
        
        print("\n[Результат зміни розміру]:")
        print(f"  • Алгоритм:            {res['method'].upper()}")
        print(f"  • Оригінальний розмір: {res['orig_size'][0]}x{res['orig_size'][1]} px ({res['initial_size_str']})")
        print(f"  • Новий розмір:        {res['new_size'][0]}x{res['new_size'][1]} px ({res['final_size_str']})")
        print(f"  • Збережено у:         {res['output_path']}")
    else:
        in_dir = input("\nВведіть вхідну папку [samples]: ").strip() or "samples"
        out_dir = input("Введіть вихідну папку [output/resized]: ").strip() or "output/resized"
        
        images = []
        for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'):
            images.extend(glob.glob(os.path.join(in_dir, ext)))

        if not images:
            print(f"[Помилка] У папці '{in_dir}' не знайдено зображень.")
            return

        print(f"\n[Обробка {len(images)} файлів...]")
        results = batch_resize_images(images, out_dir, width=width, height=height, scale_percent=scale, keep_aspect_ratio=keep_ratio, method=method)
        print("\n[Результати пакетної зміни розміру]:")
        for r in results:
            print(f"  • {os.path.basename(r['input_path'])} ({r['orig_size'][0]}x{r['orig_size'][1]}) -> ({r['new_size'][0]}x{r['new_size'][1]})")


def handle_color_replacement():
    print_header("ЗАВДАННЯ 3: ПЕРЕТВОРЕННЯ КОЛЬОРІВ (ЗАМІНА КОЛЬОРУ)")
    default_in = "samples/sample_palette.png"
    input_file = input(f"Введіть шлях до файлу [{default_in}]: ").strip() or default_in
    if not os.path.exists(input_file):
        print(f"[Помилка] Файл '{input_file}' не знайдено.")
        return

    print("\nВведіть значення кольору, який треба замінити (R, G, B від 0 до 255): ")
    print("Підказка для зразка: Червоний = 255 0 0, Зелений = 0 255 0, Синій = 0 0 255, Жовтий = 255 255 0")
    t_str = input("Цільовий колір R G B [255 0 0]: ").strip() or "255 0 0"
    target_color = tuple(map(int, t_str.split()))

    print("\nВведіть значення нового кольору (R, G, B від 0 до 255): ")
    print("Підказка: Фіолетовий = 128 0 128, Бірюзовий = 0 255 255, Чорний = 0 0 0, Білий = 255 255 255")
    n_str = input("Новий колір R G B [128 0 128]: ").strip() or "128 0 128"
    new_color = tuple(map(int, n_str.split()))

    tolerance_val = int(input("Похибка порівняння tolerance (0 - точний збіг) [15]: ").strip() or "15")
    out_file = input("Введіть вихідний шлях [output/color_replaced.png]: ").strip() or "output/color_replaced.png"

    print("\n[Обробка власним попіксельним перебором...]")
    res = replace_color(input_file, out_file, target_color, new_color, tolerance_val)
    print("\n[Результат заміни кольорів]:")
    print(f"  • Замінено пікселів: {res['replaced_pixels']} з {res['total_pixels']} ({res['replaced_percent']:.2f}% зображення)")
    print(f"  • Збережено у:        {res['output_path']}")


def handle_color_balance():
    print_header("ЗАВДАННЯ 4: КОРЕКЦІЯ КОЛІРНОГО БАЛАНСУ")
    default_in = "samples/sample_gradient.jpg"
    input_file = input(f"Введіть шлях до файлу [{default_in}]: ").strip() or default_in
    if not os.path.exists(input_file):
        print(f"[Помилка] Файл '{input_file}' не знайдено.")
        return

    print("1. Ручне налаштування каналів (збільшити/зменшити R, G, B)")
    print("2. Автоматична загальна корекція (до цільового середнього 128 за формулою з методички)")
    mode = input("Оберіть режим [1/2, за замовчуванням 1]: ").strip() or "1"

    if mode == "1":
        print("\nВведіть коефіцієнти множення каналів (1.0 = без змін, >1.0 збільшити, <1.0 зменшити):")
        rf = float(input("Червоний коефіцієнт (R factor) [1.3]: ").strip() or "1.3")
        gf = float(input("Зелений коефіцієнт (G factor) [1.0]: ").strip() or "1.0")
        bf = float(input("Синій коефіцієнт (B factor) [0.8]: ").strip() or "0.8")

        out_file = input("Введіть вихідний шлях [output/balance_manual.jpg]: ").strip() or "output/balance_manual.jpg"
        print("\n[Обробка попіксельним розрахунком...]")
        res = adjust_color_balance(input_file, out_file, r_factor=rf, g_factor=gf, b_factor=bf)
        print("\n[Результат ручної корекції балансу]:")
        print(f"  • Коефіцієнти R/G/B: {res['r_factor']} / {res['g_factor']} / {res['b_factor']}")
        print(f"  • Збережено у:       {res['output_path']}")

    else:
        out_file = input("Введіть вихідний шлях [output/balance_auto.jpg]: ").strip() or "output/balance_auto.jpg"
        print("\n[Обробка автоматичним розрахунком зсувів...]")
        res = auto_color_balance(input_file, out_file)
        print("\n[Результат автоматичного балансу]:")
        print(f"  • Початкові середні яскравості (R, G, B): {res['initial_means']}")
        print(f"  • Розраховані зміщення каналів (shifts):  {res['shifts']}")
        print(f"  • Збережено у:                           {res['output_path']}")


def main():
    while True:
        clear_console()
        print_header("КОМП'ЮТЕРНА ГРАФІКА ТА ВІЗУАЛІЗАЦІЯ | ЛАБОРАТОРНА РОБОТА №1")
        print("1. Конвертація форматів зображень")
        print("2. Зміна розміру зображень (Nearest Neighbor / Bilinear)")
        print("3. Перетворення кольорів (заміна пікселів певного кольору)")
        print("4. Корекція колірного балансу (ручна та автобаланс)")
        print("0. Вихід\n")

        choice = input("Введіть номер дії (0-4): ").strip()

        if choice == "1":
            handle_format_conversion()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_resize()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            handle_color_replacement()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "4":
            handle_color_balance()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        else:
            print("\n[!] Невірний вибір. Спробуйте ще раз.")
            input("\nНатисніть Enter для продовження...")


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nРоботу програми перервано. До побачення!")
