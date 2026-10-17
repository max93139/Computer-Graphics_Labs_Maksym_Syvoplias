# -*- coding: utf-8 -*-
"""
Головний файл консольного додатку для Лабораторної роботи №3.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.

Містить виключно методи та завдання Лабораторної роботи №3:
  1. Об'єднання двох зображень (горизонтально / вертикально)
  2. Додавання текстового водяного знаку
  3. Слайд-шоу зображень
"""

import os
import glob
import lab3_operations as ops


def clear_console():
    print("\033c\033[2J\033[H\033[3J", end="", flush=True)
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    print("\n================ ЛАБОРАТОРНА РОБОТА №3 ================")
    print("1. Об'єднання двох зображень (горизонтально / вертикально)")
    print("2. Створення водяного знаку на зображенні")
    print("3. Створення та запуск слайд-шоу")
    print("0. Вихід")
    print("=======================================================")


def handle_merge():
    print("\n--- Завдання 1: Об'єднання зображень ---")
    p1 = input("Шлях до першого зображення [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"
    p2 = input("Шлях до другого зображення [samples/sample_palette.png]: ").strip() or "samples/sample_palette.png"

    if not os.path.exists(p1) or not os.path.exists(p2):
        print("[Помилка] Один із вказаних файлів не знайдено.")
        return

    print("Оберіть напрямок об'єднання:")
    print("  1. Горизонтально (пліч-о-пліч)")
    print("  2. Вертикально (одне під іншим)")
    dir_choice = input("Напрямок [1/2, за замовчуванням 1]: ").strip() or "1"
    direction = 'horizontal' if dir_choice == '1' else 'vertical'

    out = input(f"Шлях для збереження [output/merged_{direction}.png]: ").strip() or f"output/merged_{direction}.png"

    print("\n[Обробка попіксельного об'єднання...]")
    saved, out_w, out_h = ops.combine_two_images(p1, p2, direction=direction, output_path=out)
    print(f"[Успіх] Зображення успішно об'єднано!")
    print(f"  • Напрямок:   {direction}")
    print(f"  • Розмір:     {out_w}x{out_h} px")
    print(f"  • Збережено:  {saved}")


def handle_watermark():
    print("\n--- Завдання 2: Створення водяного знаку ---")
    base_file = input("Шлях до зображення [samples/sample_gradient.jpg]: ").strip() or "samples/sample_gradient.jpg"
    if not os.path.exists(base_file):
        print(f"[Помилка] Файл '{base_file}' не знайдено.")
        return

    text = input("Введіть текст водяного знаку [© Maksym Syvoplias 2026]: ").strip() or "© Maksym Syvoplias 2026"

    print("\nОберіть позицію водяного знаку:")
    print("  1. Знизу справа (bottom_right)")
    print("  2. По центру (center)")
    print("  3. Зверху зліва (top_left)")
    print("  4. Зверху справа (top_right)")
    print("  5. Знизу зліва (bottom_left)")
    print("  6. Власні координати X, Y")
    pos_choice = input("Позиція [1-6, за замовчуванням 1]: ").strip() or "1"

    pos_map = {
        "1": "bottom_right",
        "2": "center",
        "3": "top_left",
        "4": "top_right",
        "5": "bottom_left",
    }

    if pos_choice == "6":
        x = int(input("Координата X (px) [30]: ").strip() or "30")
        y = int(input("Координата Y (px) [30]: ").strip() or "30")
        position = (x, y)
    else:
        position = pos_map.get(pos_choice, "bottom_right")

    opacity = float(input("Прозорість (0.0 - невидимий, 1.0 - непрозорий) [0.4]: ").strip() or "0.4")
    font_size = int(input("Розмір шрифту [28]: ").strip() or "28")

    print("\nОберіть колір тексту:")
    print("  1. Білий (255, 255, 255)")
    print("  2. Чорний (0, 0, 0)")
    print("  3. Жовтий (255, 255, 0)")
    print("  4. Червоний (255, 0, 0)")
    c_choice = input("Колір [1-4, за замовчуванням 1]: ").strip() or "1"
    color_map = {
        "1": (255, 255, 255),
        "2": (0, 0, 0),
        "3": (255, 255, 0),
        "4": (255, 0, 0),
    }
    text_color = color_map.get(c_choice, (255, 255, 255))

    out = input("Шлях для збереження [output/watermarked.png]: ").strip() or "output/watermarked.png"

    print("\n[Накладання водяного знаку алгоритмом Alpha Blending...]")
    saved, pos = ops.add_text_watermark(
        base_file,
        text=text,
        position=position,
        opacity=opacity,
        font_size=font_size,
        text_color=text_color,
        output_path=out
    )
    print(f"[Успіх] Водяний знак нанесено!")
    print(f"  • Текст:       '{text}'")
    print(f"  • Позиція X,Y: {pos}")
    print(f"  • Прозорість:  {opacity}")
    print(f"  • Збережено:   {saved}")


def handle_slideshow():
    print("\n--- Завдання 3: Створення та запуск слайд-шоу ---")
    print("1. Відтворити зображення з папки output/")
    print("2. Відтворити зображення з папки samples/")
    print("3. Вказати власну папку")
    f_choice = input("Джерело [1-3, за замовчуванням 1]: ").strip() or "1"

    if f_choice == "2":
        folder = "samples"
    elif f_choice == "3":
        folder = input("Введіть шлях до папки: ").strip() or "output"
    else:
        folder = "output"

    images = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp'):
        images.extend(glob.glob(os.path.join(folder, ext)))
        images.extend(glob.glob(os.path.join(folder, "**", ext)))

    # Якщо папка порожня, додамо зразки
    if not images:
        images = glob.glob(os.path.join("samples", "*.*"))

    if not images:
        print(f"[Помилка] У папці '{folder}' не знайдено графічних файлів.")
        return

    delay = float(input(f"Затримка між слайдами у секундах [1.5]: ").strip() or "1.5")

    print(f"\n[Запуск слайд-шоу для {len(images)} зображень...]")
    print("(Вікно закриється автоматично після завершення або закрийте його вручну)")
    count = ops.play_slideshow(images, delay=delay)
    print(f"[Успіх] Слайд-шоу завершено (показано {count} слайдів).")


def main():
    while True:
        show_menu()
        choice = input("Введіть номер дії (0-3): ").strip()

        if choice == "0":
            print("\nРоботу програми завершено. До побачення!")
            break
        elif choice == "1":
            handle_merge()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "2":
            handle_watermark()
            input("\nНатисніть Enter для повернення в меню...")
        elif choice == "3":
            handle_slideshow()
            input("\nНатисніть Enter для повернення в меню...")
        else:
            print("[!] Невірний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()
