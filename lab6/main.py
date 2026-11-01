# -*- coding: utf-8 -*-
"""
Головний файл консольного додатку для Лабораторної роботи №6 (Варіант 22).
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Тема: Оцінка якості фільтрації зображень за допомогою лінійних та нелінійних фільтрів.
"""

import os
import sys
import lab6_operations as ops


def show_menu():
    print("\nЛАБОРАТОРНА РОБОТА №6 (Варіант 22)")
    print("1. Підготовка набору 9 тестових зображень (128x128 BMP)")
    print("2. Оцінка спотворення f0(i,j) лінійними та нелінійними фільтрами (eps_A0^2)")
    print("3. Фільтрація зашумлених зображень (f1-f8) та оцінка якості (eps_Ak^2, MSE, PSNR)")
    print("4. Комплексний аналіз та генерація колажів/графіків")
    print("0. Вихід")


def handle_prepare_images():
    print("\nДія 1: Підготовка набору 9 тестових зображень (128x128 BMP)")
    path = input("Шлях до вихідного зображення [samples/sample_test.bmp]: ").strip() or "samples/sample_test.bmp"
    if not os.path.exists(path):
        print(f"[Помилка] Файл '{path}' не знайдено.")
        return

    out_dir = input("Каталог збереження [output]: ").strip() or "output"
    print("\n[Генерація 9 тестових зображень у форматі BMP (128x128)...]")
    saved_paths, collage_path = ops.prepare_9_test_images(source_path=path, output_dir=out_dir)

    print(f"[Успіх] Сформовано {len(saved_paths)} тестових зображень у каталозі '{out_dir}':")
    for file_path, title, _ in saved_paths:
        print(f"  - {os.path.basename(file_path)}: {title}")
    print(f"[Колаж] Збережено колаж 3х3: {collage_path}")


def handle_f0_distortion():
    print("\nДія 2: Оцінка спотворення неспотвореного зображення f0(i,j)")
    out_dir = input("Каталог з тестовими зображеннями [output]: ").strip() or "output"
    f0_file = os.path.join(out_dir, "image0.bmp")
    if not os.path.exists(f0_file):
        print(f"[Помилка] Файл '{f0_file}' не знайдено. Спочатку виконайте Дію 1.")
        return

    print("\n[Застосування 4 лінійних та 8 нелінійних фільтрів до f0(i,j)...]")
    results, collage_path = ops.evaluate_f0_distortion(output_dir=out_dir)

    print("\nТаблиця спотворень неспотвореного зображення f0:")
    print(f"{'Фільтр':<24} | {'Тип':<12} | {'eps_A0^2 (MSE)':<15} | {'PSNR (дБ)':<10}")
    for item in results:
        print(f"{item['name']:<24} | {item['type']:<12} | {item['distortion']:<15.2f} | {item['psnr']:<10.2f}")
    print(f"\n[Колаж] Збережено порівняльний колаж фільтрів: {collage_path}")


def handle_noisy_filtering():
    print("\nДія 3: Фільтрація зашумлених зображень (f1-f8) та оцінка якості")
    out_dir = input("Каталог з тестовими зображеннями [output]: ").strip() or "output"
    f0_file = os.path.join(out_dir, "image0.bmp")
    if not os.path.exists(f0_file):
        print(f"[Помилка] Файл '{f0_file}' не знайдено. Спочатку виконайте Дію 1.")
        return

    print("\n[Фільтрація зображень f1-f8 усіма фільтрами та розрахунок метрик...]")
    all_eval, grid_path, chart_path = ops.evaluate_all_noisy_images(output_dir=out_dir)

    print("\nРезультати фільтрації та оптимальні фільтри для кожного шуму:")
    print(f"{'Зображення (Шум)':<32} | {'Вихідний PSNR':<14} | {'Найкращий фільтр':<22} | {'Фільтрований PSNR':<18} | {'Приріст':<8}")
    for k in sorted(all_eval.keys()):
        item = all_eval[k]
        best = item["best_filter"]
        gain = best["psnr_to_f0"] - item["raw_psnr"]
        print(f"{item['label']:<32} | {item['raw_psnr']:<14.2f} | {best['filter_name']:<22} | {best['psnr_to_f0']:<18.2f} | {gain:+6.2f} dB")

    print(f"\n[Графіки] Збережено колаж результатів: {grid_path}")
    print(f"[Діаграма] Збережено порівняльну діаграму PSNR: {chart_path}")


def handle_full_pipeline():
    print("\nДія 4: Комплексний зведений аналіз")
    print("1) Генерація 9 тестових зображень")
    ops.prepare_9_test_images()
    print("2) Оцінка спотворення f0")
    ops.evaluate_f0_distortion()
    print("3) Пакетна фільтрація зашумлених зображень та побудова графіків")
    ops.evaluate_all_noisy_images()
    print("\n[Успіх] Комплексний аналіз повністю завершено. Усі файли оновлено в каталозі output/")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        handle_full_pipeline()
        return

    while True:
        show_menu()
        choice = input("Введіть номер дії (0-4): ").strip()

        if choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        elif choice == "1":
            handle_prepare_images()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_f0_distortion()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            handle_noisy_filtering()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "4":
            handle_full_pipeline()
            input("\nНатисніть Enter для повернення в меню...")
        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()
