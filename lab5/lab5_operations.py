# -*- coding: utf-8 -*-
"""
Операції вводу/виводу, застосування фільтрів та візуалізації для Лабораторної роботи №5.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import lab5_manual_algorithms as algos


def load_image(file_path):
    """
    Завантажує зображення з диска та повертає список кортежів пікселів (R, G, B).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    with Image.open(file_path) as img:
        img_rgb = img.convert('RGB')
        w, h = img_rgb.size
        pixels = list(img_rgb.getdata())
        return pixels, w, h, img.format or "PNG"


def save_image(output_path, width, height, pixels):
    """
    Зберігає одновимірний список пікселів у файл зображення.
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(output_path)
    return output_path


def display_image(image_path, title="Перегляд зображення"):
    """
    Відображає зображення у вікні перегляду за допомогою matplotlib.
    """
    img = Image.open(image_path)
    plt.figure(figsize=(7, 6))
    fig = plt.gcf()
    if hasattr(fig.canvas, 'manager') and fig.canvas.manager:
        fig.canvas.manager.set_window_title(title)
    plt.imshow(img)
    plt.title(f"{title}: {os.path.basename(image_path)}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def run_east_mask_filtering(input_path, output_path=None, kernel_type='prewitt', offset=0, threshold=None):
    """
    Виконує фільтрацію зображення курсовою маскою 'Схід'.
    """
    pixels, w, h, _ = load_image(input_path)

    if output_path is None:
        name_part = f"east_{kernel_type}"
        if offset != 0:
            name_part += f"_off{offset}"
        if threshold is not None:
            name_part += f"_th{threshold}"
        output_path = f"output/{name_part}.png"

    res_pixels = algos.apply_east_compass_mask(
        pixels, w, h,
        kernel_type=kernel_type,
        offset=offset,
        threshold=threshold
    )

    save_image(output_path, w, h, res_pixels)
    return output_path, w, h


def compare_filtering_results(input_path, output_comparison_path="output/comparison_east_masks.png", show=False):
    """
    Створює порівняльний колаж результатів застосування курсової маски:
    1. Оригінальне зображення
    2. Курсова маска Схід (Prewitt)
    3. Курсова маска Схід (Sobel)
    4. Курсова маска Схід з підвищенням порогу яскравості (+100)
    """
    pixels, w, h, _ = load_image(input_path)

    # 1. Prewitt East
    res_prewitt = algos.apply_east_compass_mask(pixels, w, h, kernel_type='prewitt', offset=0)
    # 2. Sobel East
    res_sobel = algos.apply_east_compass_mask(pixels, w, h, kernel_type='sobel', offset=0)
    # 3. Prewitt East + offset 100
    res_offset = algos.apply_east_compass_mask(pixels, w, h, kernel_type='prewitt', offset=100)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.canvas.manager.set_window_title("Порівняння фільтрації курсовою маскою 'Схід'")

    orig_img = Image.open(input_path).convert('RGB')
    axes[0, 0].imshow(orig_img)
    axes[0, 0].set_title("1. Первинне зображення")
    axes[0, 0].axis('off')

    img_prewitt = Image.new('RGB', (w, h))
    img_prewitt.putdata(res_prewitt)
    axes[0, 1].imshow(img_prewitt)
    axes[0, 1].set_title("2. Курсова маска 'Схід' (Prewitt, 3x3)")
    axes[0, 1].axis('off')

    img_sobel = Image.new('RGB', (w, h))
    img_sobel.putdata(res_sobel)
    axes[1, 0].imshow(img_sobel)
    axes[1, 0].set_title("3. Курсова маска 'Схід' (Sobel, 3x3)")
    axes[1, 0].axis('off')

    img_offset = Image.new('RGB', (w, h))
    img_offset.putdata(res_offset)
    axes[1, 1].imshow(img_offset)
    axes[1, 1].set_title("4. Курсова маска 'Схід' (зі зсувом +100)")
    axes[1, 1].axis('off')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_comparison_path) or '.', exist_ok=True)
    plt.savefig(output_comparison_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close()

    return output_comparison_path
