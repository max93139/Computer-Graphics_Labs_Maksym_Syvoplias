# -*- coding: utf-8 -*-
"""
Модуль для виконання завдань лабораторної роботи №1
з дисципліни 'Комп'ютерна графіка та візуалізація'.
Поєднує завантаження/збереження зображень та виклики власних алгоритмів.
"""

import os
from PIL import Image
import manual_algorithms as ma


def get_file_size_info(filepath: str) -> str:
    """Повертає розмір файлу у зручному текстовому форматі."""
    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024.0
    return f"{size_bytes} байт ({size_kb:.2f} КБ)"


def load_image_pixels(filepath: str) -> tuple[list[tuple[int, int, int]], int, int]:
    """
    Зчитує зображення та повертає список кортежів (R, G, B), ширину та висоту.
    """
    with Image.open(filepath) as img:
        rgb_img = img.convert('RGB')
        width, height = rgb_img.size
        pixels = list(rgb_img.getdata())
        return pixels, width, height


def resolve_output_path(output_path: str, default_filename: str) -> str:
    """
    Якщо output_path не вказано, є директорією або закінчується на слеш,
    повертає шлях до файлу всередині цієї директорії з ім'ям default_filename.
    """
    if not output_path:
        return os.path.join('output', default_filename)
    if os.path.isdir(output_path) or output_path.endswith('/') or output_path.endswith('\\'):
        return os.path.join(output_path, default_filename)
    return output_path


def save_pixels_to_image(filepath: str, width: int, height: int, pixels: list[tuple[int, int, int]], format_name: str = None):
    """
    Зберігає масив пікселів у файл заданого формату.
    """
    if os.path.isdir(filepath) or filepath.endswith('/') or filepath.endswith('\\'):
        ext = (format_name or 'png').lower()
        if ext == 'jpeg':
            ext = 'jpg'
        filepath = os.path.join(filepath, f"output.{ext}")

    out_img = Image.new('RGB', (width, height))
    out_img.putdata(pixels)
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    out_img.save(filepath, format=format_name)


# ЗАВДАННЯ 1: КОНВЕРТАЦІЯ ФОРМАТІВ


def convert_format(input_path: str, output_format: str, output_path: str = None) -> dict:
    """
    Конвертує зображення з одного формату в інший та розраховує зміну розміру.
    """
    target_format = output_format.strip().upper()
    if target_format == 'JPG':
        target_format = 'JPEG'

    pixels, w, h = load_image_pixels(input_path)

    file_name = os.path.splitext(os.path.basename(input_path))[0]
    ext = target_format.lower()
    if ext == 'jpeg':
        ext = 'jpg'
    default_filename = f"{file_name}_converted.{ext}"

    output_path = resolve_output_path(output_path, default_filename)
    save_pixels_to_image(output_path, w, h, pixels, format_name=target_format)

    initial_bytes = os.path.getsize(input_path)
    final_bytes = os.path.getsize(output_path)
    diff_percent = ((final_bytes - initial_bytes) / initial_bytes) * 100.0 if initial_bytes > 0 else 0.0

    return {
        "input_path": input_path,
        "output_path": output_path,
        "format": target_format,
        "initial_bytes": initial_bytes,
        "final_bytes": final_bytes,
        "initial_size_str": get_file_size_info(input_path),
        "final_size_str": get_file_size_info(output_path),
        "diff_percent": diff_percent
    }


def batch_convert_formats(input_paths: list[str], output_format: str, output_directory: str = 'output/converted') -> list[dict]:
    """Пакетна конвертація декількох зображень за один запуск."""
    os.makedirs(output_directory, exist_ok=True)
    results = []
    ext = output_format.strip().lower()
    if ext == 'jpeg':
        ext = 'jpg'

    for path in input_paths:
        file_name = os.path.splitext(os.path.basename(path))[0]
        out_file = os.path.join(output_directory, f"{file_name}_converted.{ext}")
        res = convert_format(path, output_format, out_file)
        results.append(res)
    return results


# ЗАВДАННЯ 2: ЗМІНА РОЗМІРУ ЗОБРАЖЕНЬ


def resize_image(
    input_path: str,
    output_path: str = None,
    width: int = None,
    height: int = None,
    scale_percent: float = None,
    keep_aspect_ratio: bool = True,
    method: str = 'bilinear'
) -> dict:
    """
    Змінює розмір зображення за допомогою власноруч написаних алгоритмів інтерполяції.
    """
    pixels, orig_w, orig_h = load_image_pixels(input_path)

    if scale_percent is not None and scale_percent > 0:
        factor = scale_percent / 100.0
        new_w = max(1, int(orig_w * factor))
        new_h = max(1, int(orig_h * factor))
    elif keep_aspect_ratio:
        if width is not None and height is None:
            new_w = width
            new_h = max(1, int(orig_h * (width / orig_w)))
        elif height is not None and width is None:
            new_h = height
            new_w = max(1, int(orig_w * (height / orig_h)))
        elif width is not None and height is not None:
            ratio = min(width / orig_w, height / orig_h)
            new_w = max(1, int(orig_w * ratio))
            new_h = max(1, int(orig_h * ratio))
        else:
            raise ValueError("Вкажіть ширину, висоту або відсоток.")
    else:
        if width is None or height is None:
            raise ValueError("Вкажіть точні ширину та висоту.")
        new_w = width
        new_h = height

    if method == 'nearest':
        resized_pixels = ma.resize_nearest_neighbor(pixels, orig_w, orig_h, new_w, new_h)
    else:
        resized_pixels = ma.resize_bilinear(pixels, orig_w, orig_h, new_w, new_h)

    file_name = os.path.basename(input_path)
    default_filename = f"resized_{file_name}"
    output_path = resolve_output_path(output_path, default_filename)
    save_pixels_to_image(output_path, new_w, new_h, resized_pixels)

    return {
        "input_path": input_path,
        "output_path": output_path,
        "orig_size": (orig_w, orig_h),
        "new_size": (new_w, new_h),
        "method": method,
        "initial_size_str": get_file_size_info(input_path),
        "final_size_str": get_file_size_info(output_path)
    }


def batch_resize_images(
    input_paths: list[str],
    output_directory: str = 'output/resized',
    width: int = None,
    height: int = None,
    scale_percent: float = None,
    keep_aspect_ratio: bool = True,
    method: str = 'bilinear'
) -> list[dict]:
    """Пакетна зміна розміру декількох зображень за один запуск."""
    os.makedirs(output_directory, exist_ok=True)
    results = []
    for path in input_paths:
        file_name = os.path.basename(path)
        out_file = os.path.join(output_directory, f"resized_{file_name}")
        res = resize_image(
            input_path=path,
            output_path=out_file,
            width=width,
            height=height,
            scale_percent=scale_percent,
            keep_aspect_ratio=keep_aspect_ratio,
            method=method
        )
        results.append(res)
    return results


# ЗАВДАННЯ 3: ПЕРЕТВОРЕННЯ КОЛЬОРІВ


def replace_color(
    input_path: str,
    output_path: str = None,
    target_color: tuple[int, int, int] = (255, 0, 0),
    new_color: tuple[int, int, int] = (128, 0, 128),
    tolerance: int = 15
) -> dict:
    """Замінює всі пікселі цільового кольору за допомогою власної функції."""
    pixels, w, h = load_image_pixels(input_path)
    new_pixels, replaced_count = ma.replace_pixels_color(pixels, target_color, new_color, tolerance)
    output_path = resolve_output_path(output_path, "color_replaced.png")
    save_pixels_to_image(output_path, w, h, new_pixels)

    total_pixels = len(pixels)
    percent = (replaced_count / total_pixels) * 100.0 if total_pixels > 0 else 0.0

    return {
        "input_path": input_path,
        "output_path": output_path,
        "target_color": target_color,
        "new_color": new_color,
        "replaced_pixels": replaced_count,
        "total_pixels": total_pixels,
        "replaced_percent": percent
    }


# ЗАВДАННЯ 4: КОРЕКЦІЯ КОЛІРНОГО БАЛАНСУ


def adjust_color_balance(
    input_path: str,
    output_path: str = None,
    r_factor: float = 1.0,
    g_factor: float = 1.0,
    b_factor: float = 1.0,
    r_delta: int = 0,
    g_delta: int = 0,
    b_delta: int = 0
) -> dict:
    """Ручна корекція колірного балансу."""
    pixels, w, h = load_image_pixels(input_path)
    new_pixels = ma.apply_color_balance(
        pixels,
        r_factor=r_factor,
        g_factor=g_factor,
        b_factor=b_factor,
        r_delta=r_delta,
        g_delta=g_delta,
        b_delta=b_delta
    )
    output_path = resolve_output_path(output_path, "balance_manual.jpg")
    save_pixels_to_image(output_path, w, h, new_pixels)

    return {
        "input_path": input_path,
        "output_path": output_path,
        "r_factor": r_factor,
        "g_factor": g_factor,
        "b_factor": b_factor,
        "r_delta": r_delta,
        "g_delta": g_delta,
        "b_delta": b_delta
    }


def auto_color_balance(input_path: str, output_path: str = None, target_mean: float = 128.0) -> dict:
    """Автоматична корекція балансу за формулою з методички."""
    pixels, w, h = load_image_pixels(input_path)
    new_pixels, stats = ma.apply_auto_color_balance(pixels, target_mean=target_mean)
    output_path = resolve_output_path(output_path, "balance_auto.jpg")
    save_pixels_to_image(output_path, w, h, new_pixels)

    return {
        "input_path": input_path,
        "output_path": output_path,
        "initial_means": stats.get("means"),
        "shifts": stats.get("shifts"),
        "target_mean": target_mean
    }
