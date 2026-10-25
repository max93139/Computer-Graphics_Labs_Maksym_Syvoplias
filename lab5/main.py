# -*- coding: utf-8 -*-
"""
Головний файл консольного додатку для Лабораторної роботи №5.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Варіант 22: Застосування курсової маски схід.
"""

import os
import lab5_operations as ops


def show_menu():
    print("\nЛАБОРАТОРНА РОБОТА №5 (Варіант 22)")
    print("1. Зашумлення")
    print("2. Застосування маски «Схід»")
    print("0. Вихід")


def handle_noise():
    print("\nДія 1: Зашумлення зображення")
    path = input("Шлях до файлу [samples/sample_building.jpg]: ").strip() or "samples/sample_building.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    count_str = input("Кількість точок шуму [1000]: ").strip() or "1000"
    try:
        count = int(count_str)
    except ValueError:
        count = 1000

    out_file = input("Шлях для збереження [output/noisy_image.png]: ").strip() or "output/noisy_image.png"

    print("\n[Додавання імпульсного шуму до зображення...]")
    saved, w, h = ops.run_add_noise(path, output_path=out_file, count=count)
    print(f"[Успіх] Зашумлене зображення ({w}x{h}) збережено в: {saved}")


def handle_east_mask():
    print("\nДія 2: Застосування маски «Схід»")
    path = input("Шлях до файлу [samples/sample_building.jpg]: ").strip() or "samples/sample_building.jpg"

    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_file = input("Шлях для збереження [output/east_mask.png]: ").strip() or "output/east_mask.png"

    print("\n[Застосування курсової маски «Схід» (Prewitt East)...]")
    saved, w, h = ops.run_east_mask(path, output_path=out_file)
    print(f"[Успіх] Результат фільтрації ({w}x{h}) збережено в: {saved}")


def main():
    while True:
        show_menu()
        choice = input("Введіть номер дії (0-2): ").strip()

        if choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        elif choice == "1":
            handle_noise()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_east_mask()
            input("\nНатисніть Enter для повернення в меню...")
        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()
