# -*- coding: utf-8 -*-
"""
Модуль високорівневих операцій для Лабораторної роботи №3:
1. Об'єднання двох зображень (горизонтально / вертикально).
2. Накладання текстового водяного знаку.
3. Відтворення слайд-шоу.
"""

import os
import time
from PIL import Image, ImageDraw, ImageFont
import lab3_manual_algorithms as algos


def load_image(filepath):
    """Зчитує зображення та повертає список пікселів (RGB), ширину і висоту."""
    with Image.open(filepath) as img:
        rgb_img = img.convert('RGB')
        w, h = rgb_img.size
        return list(rgb_img.getdata()), w, h


def save_image(filepath, width, height, pixels):
    """Зберігає масив пікселів у файл."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(filepath)


def combine_two_images(path1, path2, direction='horizontal', bg_color=(255, 255, 255), output_path='output/merged.png'):
    """
    Об'єднує два зображення горизонтально або вертикально.
    """
    pixels1, w1, h1 = load_image(path1)
    pixels2, w2, h2 = load_image(path2)

    if direction == 'horizontal':
        res_pixels, out_w, out_h = algos.merge_horizontal(pixels1, w1, h1, pixels2, w2, h2, bg_color)
    else:
        res_pixels, out_w, out_h = algos.merge_vertical(pixels1, w1, h1, pixels2, w2, h2, bg_color)

    save_image(output_path, out_w, out_h, res_pixels)
    return output_path, out_w, out_h


def add_text_watermark(
    base_path,
    text="Watermark",
    position="bottom_right",
    opacity=0.5,
    font_size=36,
    text_color=(255, 255, 255),
    output_path="output/watermarked.png"
):
    """
    Накладає напівпрозорий текстовий водяний знак на зображення.
    position: 'center', 'top_left', 'top_right', 'bottom_left', 'bottom_right' або кортеж (x, y)
    opacity: від 0.0 (невидимий) до 1.0 (повністю непрозорий)
    """
    base_pixels, w, h = load_image(base_path)

    # Створюємо прозорий шар для тексту того ж розміру
    text_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    # Спроба завантажити моноширинний або системний шрифт
    font = None
    possible_fonts = [
        '/System/Library/Fonts/Monaco.ttf',
        '/System/Library/Fonts/SFMono-Regular.otf',
        '/System/Library/Fonts/Menlo.ttc',
        '/System/Library/Fonts/Helvetica.ttc',
        '/Library/Fonts/Arial.ttf'
    ]
    for p in possible_fonts:
        if os.path.exists(p):
            try:
                font = ImageFont.truetype(p, font_size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    # Розрахунок габаритів тексту
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Визначення координат
    margin = 20
    if isinstance(position, tuple) or isinstance(position, list):
        pos_x, pos_y = position[0], position[1]
    elif position == 'center':
        pos_x = (w - text_w) // 2
        pos_y = (h - text_h) // 2
    elif position == 'top_left':
        pos_x = margin
        pos_y = margin
    elif position == 'top_right':
        pos_x = max(0, w - text_w - margin)
        pos_y = margin
    elif position == 'bottom_left':
        pos_x = margin
        pos_y = max(0, h - text_h - margin)
    else:  # bottom_right
        pos_x = max(0, w - text_w - margin)
        pos_y = max(0, h - text_h - margin)

    # Малюємо непрозорий текст на прозорому шарі (R, G, B, 255)
    r, g, b = text_color
    draw.text((pos_x, pos_y), text, font=font, fill=(r, g, b, 255))

    # Витягуємо пікселі текстового шару
    mark_pixels = list(text_layer.getdata())

    # Власне змішування за допомогою нашого алгоритму
    blended_pixels = algos.blend_watermark(base_pixels, w, h, mark_pixels, opacity)

    save_image(output_path, w, h, blended_pixels)
    return output_path, (pos_x, pos_y)


def play_slideshow(image_paths, delay=2.0):
    """
    Відтворює послідовно зображення за допомогою matplotlib.
    """
    valid_paths = [p for p in image_paths if os.path.exists(p)]
    if not valid_paths:
        raise ValueError("Список зображень для слайд-шоу порожній або файли не існують.")

    import matplotlib.pyplot as plt

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.canvas.manager.set_window_title("Слайд-шоу | Лабораторна робота №3")

    for i, path in enumerate(valid_paths):
        img = Image.open(path)
        ax.clear()
        ax.imshow(img)
        ax.set_title(f"Слайд {i + 1} / {len(valid_paths)}: {os.path.basename(path)}")
        ax.axis('off')
        plt.tight_layout()
        plt.draw()
        plt.pause(delay)

    plt.ioff()
    plt.close()
    return len(valid_paths)
