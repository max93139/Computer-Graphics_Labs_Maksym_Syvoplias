# -*- coding: utf-8 -*-
"""
Головний файл консольного додатку для Лабораторної роботи №5.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Варіант 22: Застосування курсової маски схід (East compass / directional mask).
"""

import os
import lab5_operations as ops


def show_menu():
    print("\nЛАБОРАТОРНА РОБОТА №5 (Варіант 22)")
    print("1. Виведення первинного кольорового зображення")
    print("2. Фільтрація курсовою маскою 'Схід' (Prewitt East, 3x3)")
    print("3. Фільтрація курсовою маскою 'Схід' (Sobel East, 3x3)")
    print("4. Фільтрація курсовою маскою 'Схід' з підвищенням порогу яскравості (+100)")
    print("5. Фільтрація курсовою маскою 'Схід' з бінаризацією меж")
    print("6. Комплексне порівняння та формування колажу результатів")
    print("0. Вихід")


def handle_display():
    print("\nДія 1: Виведення первинного кольорового зображення")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    print("[Відкриття вікна зображення...]")
    ops.display_image(path, title="Первинне зображення")
    print(f"[Успіх] Зображення '{path}' відображено на екрані.")


def handle_east_prewitt():
    print("\nДія 2: Фільтрація курсовою маскою 'Схід' (Prewitt East)")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_file = input("Шлях для збереження [output/east_prewitt.png]: ").strip() or "output/east_prewitt.png"

    print("\n[Застосування курсової маски 'Схід' (Prewitt)...]")
    saved, w, h = ops.run_east_mask_filtering(path, output_path=out_file, kernel_type='prewitt', offset=0)
    print(f"[Успіх] Результат ({w}x{h}) успішно збережено в: {saved}")


def handle_east_sobel():
    print("\nДія 3: Фільтрація курсовою маскою 'Схід' (Sobel East)")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_file = input("Шлях для збереження [output/east_sobel.png]: ").strip() or "output/east_sobel.png"

    print("\n[Застосування курсової маски 'Схід' (Sobel)...]")
    saved, w, h = ops.run_east_mask_filtering(path, output_path=out_file, kernel_type='sobel', offset=0)
    print(f"[Успіх] Результат ({w}x{h}) успішно збережено в: {saved}")


def handle_east_offset():
    print("\nДія 4: Фільтрація курсовою маскою 'Схід' з підвищенням порогу яскравості (+100)")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    val_str = input("Величина зсуву яскравості [100]: ").strip() or "100"
    try:
        offset_val = int(val_str)
    except ValueError:
        offset_val = 100

    out_file = input(f"Шлях для збереження [output/east_offset_{offset_val}.png]: ").strip() or f"output/east_offset_{offset_val}.png"

    print(f"\n[Застосування курсової маски 'Схід' зі зсувом яскравості +{offset_val}...]")
    saved, w, h = ops.run_east_mask_filtering(path, output_path=out_file, kernel_type='prewitt', offset=offset_val)
    print(f"[Успіх] Результат ({w}x{h}) збережено в: {saved}")


def handle_east_threshold():
    print("\nДія 5: Фільтрація курсовою маскою 'Схід' з бінаризацією меж")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    th_str = input("Поріг бінаризації виділених меж (0..255) [60]: ").strip() or "60"
    try:
        threshold_val = int(th_str)
    except ValueError:
        threshold_val = 60

    out_file = input(f"Шлях для збереження [output/east_binarized_th{threshold_val}.png]: ").strip() or f"output/east_binarized_th{threshold_val}.png"

    print(f"\n[Застосування курсової маски з бінаризацією за порогом {threshold_val}...]")
    saved, w, h = ops.run_east_mask_filtering(path, output_path=out_file, kernel_type='prewitt', offset=0, threshold=threshold_val)
    print(f"[Успіх] Результат бінаризації меж збережено в: {saved}")


def handle_comparison():
    print("\nДія 6: Комплексне порівняння та формування колажу")
    path = input("Шлях до файлу [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_file = input("Шлях для збереження колажу [output/comparison_east_masks.png]: ").strip() or "output/comparison_east_masks.png"

    print("\n[Генерація порівняльної матриці фільтрації...]")
    saved = ops.compare_filtering_results(path, output_comparison_path=out_file, show=False)
    print(f"[Успіх] Порівняльний колаж збережено в: {saved}")


def main():
    while True:
        show_menu()
        choice = input("Введіть номер дії (0-6): ").strip()

        if choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        elif choice == "1":
            handle_display()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_east_prewitt()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            handle_east_sobel()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "4":
            handle_east_offset()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "5":
            handle_east_threshold()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "6":
            handle_comparison()
            input("\nНатисніть Enter для повернення в меню...")
        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()
