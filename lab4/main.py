# -*- coding: utf-8 -*-
"""
Головний файл консольного додатку для Лабораторної роботи №4.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Містить виключно методи та завдання Лабораторної роботи №4:
  1. Виведення первинного кольорового зображення на екран
  2. Виведення на екран матриці значень яскравості зображення
  3. Побудова гістограми яскравості кольорового зображення
  4. Зміна кольоровості (бінаризація, відтінки сірого, негатив, гістограма сірого)
"""

import os
import lab4_operations as ops


def clear_console():
    print("\033c\033[2J\033[H\033[3J", end="", flush=True)
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    print("\nЛАБОРАТОРНА РОБОТА №4")
    print("1. Виведення первинного кольорового зображення")
    print("2. Виведення матриці значень яскравості зображення")
    print("3. Побудова гістограми яскравості кольорового зображення")
    print("4. Зміна кольоровості (бінаризація, відтінки сірого, негатив, гістограма сірого)")
    print("0. Вихід")


def handle_display():
    print("\nЗавдання 1: Виведення первинного кольорового зображення")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    print("[Відкриття вікна зображення...]")
    ops.display_image(path)
    print(f"[Успіх] Зображення '{path}' відображено на екрані.")


def handle_brightness_matrix():
    print("\nЗавдання 2: Матриця значень яскравості зображення")
    path = input("Шлях до файлу [samples/sample_palette.png]: ").strip() or "samples/sample_palette.png"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_txt = input("Шлях для збереження матриці [output/brightness_matrix.txt]: ").strip() or "output/brightness_matrix.txt"

    print("\n[Розрахунок матриці яскравості Y = 0.299*R + 0.587*G + 0.114*B...]")
    res = ops.get_brightness_matrix_info(path, output_txt_path=out_txt, sample_rows=10, sample_cols=10)

    print(f"[Успіх] Повну матрицю ({res['height']} рядків x {res['width']} колонок) збережено в: {res['txt_path']}")
    print(f"\nФрагмент матриці значень яскравості ({res['actual_rows']}x{res['actual_cols']} верхній лівий кут):")
    for r in res['sample_preview']:
        print("  " + " ".join(f"{val:3d}" for val in r))


def handle_color_histogram():
    print("\nЗавдання 3: Побудова гістограми яскравості кольорового зображення")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_hist = input("Шлях для збереження графіку [output/histogram_color.png]: ").strip() or "output/histogram_color.png"

    print("\n[Побудова гістограм для каналів R, G, B та сумарної яскравості Y...]")
    saved = ops.plot_color_histogram(path, output_plot_path=out_hist, show=True)
    print(f"[Успіх] Гістограму успішно збережено в: {saved}")


def show_color_transformations_menu():
    print("\nЗавдання 4: Зміна кольоровості")
    print("1. Бінаризація (перехід до чорно-білого)")
    print("2. Перехід до відтінків сірого")
    print("3. Негатив")
    print("4. Побудова гістограми зображення в градаціях сірого")
    print("5. Виконати всі 4 операції разом")
    print("0. Назад у головне меню")


def handle_color_transformations():
    default_img = "samples/sample_gradient.jpg"

    while True:
        show_color_transformations_menu()
        sub_choice = input("Оберіть підпункт (0-5): ").strip()

        if sub_choice == "0":
            break

        path = input(f"Шлях до файлу [{default_img}]: ").strip() or default_img
        if not os.path.exists(path):
            print(f"[Помилка] Файл '{path}' не знайдено.")
            continue

        if sub_choice == "1":
            p_str = input("Поріг бінаризації P від 0 до 255 [128]: ").strip() or "128"
            try:
                threshold = int(p_str)
            except ValueError:
                threshold = 128
            out_file = f"output/binarized_p{threshold}.png"
            res = ops.run_binarize(path, threshold=threshold, output_path=out_file)
            print(f"[Успіх] Бінаризоване зображення збережено в: {res}")
            input("\nНатисніть Enter для продовження...")

        elif sub_choice == "2":
            out_file = "output/grayscale.png"
            res = ops.run_grayscale(path, output_path=out_file)
            print(f"[Успіх] Зображення у відтінках сірого збережено в: {res}")
            input("\nНатисніть Enter для продовження...")

        elif sub_choice == "3":
            out_file = "output/negative.png"
            res = ops.run_negative(path, output_path=out_file)
            print(f"[Успіх] Негатив зображення збережено в: {res}")
            input("\nНатисніть Enter для продовження...")

        elif sub_choice == "4":
            out_hist = "output/histogram_gray.png"
            res = ops.plot_grayscale_histogram(path, output_plot_path=out_hist, show=True)
            print(f"[Успіх] Гістограму зображення збережено в: {res}")
            input("\nНатисніть Enter для продовження...")

        elif sub_choice == "5":
            p_str = input("Поріг бінаризації P від 0 до 255 [128]: ").strip() or "128"
            try:
                threshold = int(p_str)
            except ValueError:
                threshold = 128
            print("\n[Виконання комплексу перетворень кольоровості...]")
            res = ops.apply_color_transformations(path, output_dir="output", threshold=threshold)
            print("[Успіх] Всі операції зміни кольоровості успішно виконано:")
            print(f"  • Перехід до відтінків сірого:      {res['gray_path']}")
            print(f"  • Бінаризація (поріг {res['threshold']}):            {res['bin_path']}")
            print(f"  • Фотографічний негатив:           {res['neg_path']}")
            print(f"  • Гістограма для сірого зображення: {res['hist_path']}")
            input("\nНатисніть Enter для продовження...")

        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


def main():
    while True:
        show_menu()
        choice = input("Введіть номер дії (0-4): ").strip()

        if choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        elif choice == "1":
            handle_display()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_brightness_matrix()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            handle_color_histogram()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "4":
            handle_color_transformations()
        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()

