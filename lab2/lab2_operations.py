# -*- coding: utf-8 -*-
"""
Модуль операцій для Лабораторної роботи №2:
Завантаження, збереження та виклики власних алгоритмів.
"""

import os
from PIL import Image
import lab2_manual_algorithms as algos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def resolve_input_path(filepath):
    """
    Знаходить реальний шлях до вхідного файлу:
    - Перевіряє прямий шлях та шлях відносно BASE_DIR.
    - Коригує випадки, коли вказано префікс 'lab2/' під час запуску зсередини директорії lab2.
    - Перевіряє розташування у папці samples або батьківській директорії.
    """
    if not filepath:
        raise ValueError("Шлях до вхідного файлу не може бути порожнім.")

    clean_path = str(filepath).strip()
    candidates = [
        clean_path,
        os.path.join(BASE_DIR, clean_path),
    ]

    if clean_path.startswith("lab2/") or clean_path.startswith("lab2\\"):
        without_prefix = clean_path[5:]
        candidates.append(os.path.join(BASE_DIR, without_prefix))
        candidates.append(without_prefix)

    candidates.append(os.path.join(BASE_DIR, "samples", os.path.basename(clean_path)))
    parent_dir = os.path.dirname(BASE_DIR)
    candidates.append(os.path.join(parent_dir, clean_path))

    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

    return clean_path


def resolve_output_path(output_path=None, default_filename="result.png"):
    """
    Повертає абсолютний шлях до файлу збереження в lab2/output:
    - Якщо output_path порожній або None -> lab2/output/{default_filename}
    - Якщо вказано відносний шлях (наприклад, 'output/file.png') -> lab2/output/{file.png}
    - Якщо вказано директорію -> {директорія}/{default_filename}
    - Якщо вказано абсолютний шлях -> повертає його без змін.
    """
    if not output_path or not str(output_path).strip():
        return os.path.join(DEFAULT_OUTPUT_DIR, default_filename)

    path = str(output_path).strip()

    if os.path.isabs(path):
        if os.path.isdir(path) or path.endswith('/') or path.endswith('\\'):
            return os.path.join(path, default_filename)
        return path

    if path.startswith("lab2/output/") or path.startswith("lab2\\output\\"):
        path = path[12:]
        return os.path.join(DEFAULT_OUTPUT_DIR, path)

    if path.startswith("output/") or path.startswith("output\\"):
        path = path[7:]
        return os.path.join(DEFAULT_OUTPUT_DIR, path)

    if path.startswith("lab2/") or path.startswith("lab2\\"):
        path = path[5:]
        return os.path.join(BASE_DIR, path)

    if path.endswith('/') or path.endswith('\\'):
        return os.path.join(DEFAULT_OUTPUT_DIR, path, default_filename)

    return os.path.join(DEFAULT_OUTPUT_DIR, path)


def resolve_output_dir(output_dir=None, default_dirname="split"):
    """
    Повертає абсолютний шлях до директорії збереження всередині lab2/output.
    """
    if not output_dir or not str(output_dir).strip():
        return os.path.join(DEFAULT_OUTPUT_DIR, default_dirname)

    path = str(output_dir).strip()
    if os.path.isabs(path):
        return path

    if path.startswith("lab2/output/") or path.startswith("lab2\\output\\"):
        path = path[12:]
        return os.path.join(DEFAULT_OUTPUT_DIR, path)

    if path.startswith("output/") or path.startswith("output\\"):
        path = path[7:]
        return os.path.join(DEFAULT_OUTPUT_DIR, path)

    return os.path.join(DEFAULT_OUTPUT_DIR, path)


def load_image(filepath):
    """Зчитує зображення та повертає список пікселів, ширину та висоту."""
    real_path = resolve_input_path(filepath)
    img = Image.open(real_path)
    mode = 'RGBA' if img.mode in ('RGBA', 'LA') else 'RGB'
    img = img.convert(mode)
    width, height = img.size
    pixels = list(img.getdata())
    return pixels, width, height


def save_image(filepath, width, height, pixels):
    """Створює зображення з масиву пікселів та зберігає у файл."""
    full_path = resolve_output_path(filepath, "output.png")
    os.makedirs(os.path.dirname(full_path) or '.', exist_ok=True)
    mode = 'RGBA' if len(pixels[0]) == 4 else 'RGB'

    img = Image.new(mode, (width, height))
    img.putdata(pixels)

    if full_path.lower().endswith(('.jpg', '.jpeg')) and mode == 'RGBA':
        img = img.convert('RGB')

    img.save(full_path)
    return full_path


def change_image_transparency(input_path, alpha, output_path=None):
    """Змінює рівень прозорості зображення."""
    target_path = resolve_output_path(output_path, "transparent.png")
    pixels, w, h = load_image(input_path)
    new_pixels = algos.set_transparency(pixels, alpha)
    return save_image(target_path, w, h, new_pixels)


def overlay_two_images(base_path, overlay_path, x=0, y=0, alpha_factor=1.0, output_path=None):
    """Накладає одне зображення поверх іншого."""
    target_path = resolve_output_path(output_path, "overlay.png")
    base_pixels, bw, bh = load_image(base_path)
    over_pixels, ow, oh = load_image(overlay_path)

    blended = algos.overlay_layers(base_pixels, bw, bh, over_pixels, ow, oh, x, y, alpha_factor)
    return save_image(target_path, bw, bh, blended)


def split_image_to_parts(input_path, rows, cols, output_dir=None):
    """Розбиває зображення на кілька частин."""
    target_dir = resolve_output_dir(output_dir, "split")
    pixels, w, h = load_image(input_path)
    parts = algos.split_image(pixels, w, h, rows, cols)

    os.makedirs(target_dir, exist_ok=True)
    saved_files = []

    for p in parts:
        filename = os.path.join(target_dir, f"part_{p['index']}.png")
        save_image(filename, p['width'], p['height'], p['pixels'])
        saved_files.append(filename)

    return saved_files


def crop_image_area(input_path, x1, y1, x2, y2, output_path=None):
    """Кадрує зображення (залишає тільки обрану область)."""
    target_path = resolve_output_path(output_path, "cropped.png")
    pixels, w, h = load_image(input_path)
    cropped_pixels, new_w, new_h = algos.crop_area(pixels, w, h, x1, y1, x2, y2)
    save_image(target_path, new_w, new_h, cropped_pixels)
    return target_path, new_w, new_h


def cut_out_image_area(input_path, x1, y1, x2, y2, fill_color=(255, 255, 255), output_path=None):
    """Вилучає обрану область (замальовує кольором)."""
    target_path = resolve_output_path(output_path, "cutout.png")
    pixels, w, h = load_image(input_path)
    result_pixels = algos.remove_area(pixels, w, h, x1, y1, x2, y2, fill_color)
    return save_image(target_path, w, h, result_pixels)


def adjust_image_contrast(input_path, k, output_path=None):
    """Змінює контрастність зображення за формулою."""
    default_name = f"contrast_k{k}.png"
    target_path = resolve_output_path(output_path, default_name)
    pixels, w, h = load_image(input_path)
    new_pixels, averages = algos.change_contrast(pixels, k)
    save_image(target_path, w, h, new_pixels)
    return target_path, averages
