# -*- coding: utf-8 -*-
"""
Головний файл програми для Лабораторної роботи №2.
"""

import os
import lab2_operations as lab2_ops


def show_menu():
    print("\nГОЛОВНЕ МЕНЮ (Лабораторна робота №2)")
    print("1. Прозорість та накладання шарів")
    print("2. Кадрування та поділ зображення")
    print("3. Зміна контрастності (формула NewY = K*(OldY - AveY) + AveY)")
    print("0. Вихід")


def handle_lab2_transparency():
    print("\nЗавдання 1: Прозорість та накладання")
    print("1. Додати прозорість до одного зображення")
    print("2. Накласти одне зображення на інше (шари)")
    choice = input("Оберіть дію [1/2]: ").strip() or "1"

    if choice == "1":
        path = input("Шлях до файлу [samples/sample_palette.png]: ").strip() or "samples/sample_palette.png"
        alpha = int(input("Рівень непрозорості альфа (0..255) [128]: ").strip() or "128")
        out = input("Куди зберегти [output/transparent.png]: ").strip() or None

        res = lab2_ops.change_image_transparency(path, alpha, out)
        print(f"Зображення з прозорістю збережено в: {res}")
    else:
        base = input("Фонове зображення [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"
        over = input("Верхнє зображення [samples/sample_palette.png]: ").strip() or "samples/sample_palette.png"
        x = int(input("Координата X зміщення [50]: ").strip() or "50")
        y = int(input("Координата Y зміщення [50]: ").strip() or "50")
        factor = float(input("Коефіцієнт прозорості верхнього шару (0.0..1.0) [0.7]: ").strip() or "0.7")
        out = input("Куди зберегти [output/overlay.png]: ").strip() or None

        res = lab2_ops.overlay_two_images(base, over, x, y, factor, out)
        print(f"Результат накладання шарів збережено в: {res}")


def handle_lab2_cropping():
    print("\nЗавдання 2: Кадрування та поділ")
    print("1. Розбити зображення на N частин")
    print("2. Кадрувати (вилучити все за межами обраної області)")
    print("3. Вирізати область (вилучити обрану прямокутну частину)")
    choice = input("Оберіть дію [1-3]: ").strip() or "1"

    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if choice == "1":
        rows = int(input("Кількість частин по вертикалі (рядків) [2]: ").strip() or "2")
        cols = int(input("Кількість частин по горизонталі (колонок) [2]: ").strip() or "2")
        out_dir = input("Папка для збереження [output/split]: ").strip() or None

        files = lab2_ops.split_image_to_parts(path, rows, cols, out_dir)
        print(f"Створено {len(files)} частин:")
        for f in files:
            print(" ", f)
    elif choice == "2":
        x1 = int(input("X1 [50]: ").strip() or "50")
        y1 = int(input("Y1 [50]: ").strip() or "50")
        x2 = int(input("X2 [300]: ").strip() or "300")
        y2 = int(input("Y2 [200]: ").strip() or "200")
        out = input("Куди зберегти [output/cropped.png]: ").strip() or None

        saved, w, h = lab2_ops.crop_image_area(path, x1, y1, x2, y2, out)
        print(f"Кадроване зображення розміром {w}x{h} збережено в: {saved}")
    else:
        x1 = int(input("X1 [50]: ").strip() or "50")
        y1 = int(input("Y1 [50]: ").strip() or "50")
        x2 = int(input("X2 [250]: ").strip() or "250")
        y2 = int(input("Y2 [200]: ").strip() or "200")
        out = input("Куди зберегти [output/cutout.png]: ").strip() or None

        saved = lab2_ops.cut_out_image_area(path, x1, y1, x2, y2, fill_color=(255, 255, 255), output_path=out)
        print(f"Зображення з вилученою областю збережено в: {saved}")


def handle_lab2_contrast():
    print("\nЗавдання 3: Збільшення контрастності")
    print("Формула: NewY = K * (OldY - AveY) + AveY")
    print("  K > 1.0 — збільшення контрастності (наприклад, 1.5 або 2.0)")
    print("  K < 1.0 — зменшення контрастності (наприклад, 0.5)")

    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"
    k = float(input("Введіть коефіцієнт K [1.6]: ").strip() or "1.6")
    out = input(f"Куди зберегти [output/contrast_k{k}.png]: ").strip() or None

    saved, aves = lab2_ops.adjust_image_contrast(path, k, out)
    print(f"Зображення збережено в: {saved}")
    print(f"Середні значення каналів (R, G, B): {aves}")


def main():
    while True:
        show_menu()
        choice = input("Введіть номер дії (0-3): ").strip()

        if choice == "0":
            print("Вихід з програми.")
            break
        elif choice == "1":
            handle_lab2_transparency()
        elif choice == "2":
            handle_lab2_cropping()
        elif choice == "3":
            handle_lab2_contrast()
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()
