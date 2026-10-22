# -*- coding: utf-8 -*-
"""
Модуль високорівневих операцій для Лабораторної роботи №4:
1. Відображення первинного кольорового зображення.
2. Розрахунок та експорт матриці яскравості (зріз у консоль + повний файл).
3. Побудова гістограми яскравості кольорового зображення (поканально та сумарно).
4. Зміна кольоровості (бінаризація, відтінки сірого, негатив, гістограма сірого).
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import lab4_manual_algorithms as algos


def load_image(filepath):
    """Зчитує зображення та повертає список пікселів, ширину та висоту."""
    with Image.open(filepath) as img:
        mode = 'RGBA' if img.mode in ('RGBA', 'LA') else 'RGB'
        converted = img.convert(mode)
        w, h = converted.size
        return list(converted.getdata()), w, h, mode


def save_image(filepath, width, height, pixels):
    """Зберігає масив пікселів у файл."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    mode = 'RGBA' if len(pixels[0]) == 4 else 'RGB'

    out_img = Image.new(mode, (width, height))
    out_img.putdata(pixels)

    if filepath.lower().endswith(('.jpg', '.jpeg')) and mode == 'RGBA':
        out_img = out_img.convert('RGB')

    out_img.save(filepath)


def display_image(filepath):
    """Відображає кольорове зображення у вікні перегляду."""
    img = Image.open(filepath)
    plt.figure("Первинне зображення")
    plt.imshow(img)
    plt.title(f"Зображення: {os.path.basename(filepath)} ({img.width}x{img.height})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def get_brightness_matrix_info(input_path, output_txt_path="output/brightness_matrix.txt", sample_rows=10, sample_cols=10):
    """
    Обчислює повну матрицю значень яскравості, зберігає її у текстовий файл
    та повертає невеликий зріз sample_rows x sample_cols для наочного показу.
    """
    pixels, w, h, _ = load_image(input_path)
    matrix = algos.calculate_brightness_matrix(pixels, w, h)

    os.makedirs(os.path.dirname(output_txt_path) or '.', exist_ok=True)
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Матриця значень яскравості зображення: {input_path}\n")
        f.write(f"Розмірність: {h} рядків x {w} колонок (значення в діапазоні 0..255)\n\n")
        for row in matrix:
            f.write(" ".join(f"{val:3d}" for val in row) + "\n")

    actual_rows = min(h, sample_rows)
    actual_cols = min(w, sample_cols)
    sample_preview = [matrix[y][:actual_cols] for y in range(actual_rows)]

    return {
        "width": w,
        "height": h,
        "txt_path": output_txt_path,
        "sample_preview": sample_preview,
        "actual_rows": actual_rows,
        "actual_cols": actual_cols
    }


def plot_color_histogram(input_path, output_plot_path="output/histogram_color.png", show=False):
    """
    Будує гістограми розподілу яскравості для кольорового зображення:
    окремо по каналах R, G, B та сумарної яскравості Y.
    """
    pixels, w, h, _ = load_image(input_path)

    r_vals = [p[0] for p in pixels]
    g_vals = [p[1] for p in pixels]
    b_vals = [p[2] for p in pixels]
    y_vals = [algos.calculate_pixel_brightness(p[0], p[1], p[2]) for p in pixels]

    hist_r = algos.build_histogram(r_vals)
    hist_g = algos.build_histogram(g_vals)
    hist_b = algos.build_histogram(b_vals)
    hist_y = algos.build_histogram(y_vals)

    x_levels = list(range(256))

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    fig.canvas.manager.set_window_title("Гістограми розподілу кольорів та яскравості")

    axes[0, 0].bar(x_levels, hist_r, color='red', width=1.0)
    axes[0, 0].set_title("Червоний канал (Red)")
    axes[0, 0].set_xlim(0, 255)

    axes[0, 1].bar(x_levels, hist_g, color='green', width=1.0)
    axes[0, 1].set_title("Зелений канал (Green)")
    axes[0, 1].set_xlim(0, 255)

    axes[1, 0].bar(x_levels, hist_b, color='blue', width=1.0)
    axes[1, 0].set_title("Синій канал (Blue)")
    axes[1, 0].set_xlim(0, 255)

    axes[1, 1].bar(x_levels, hist_y, color='dimgray', width=1.0)
    axes[1, 1].set_title("Яскравість (Luminance Y = 0.299R+0.587G+0.114B)")
    axes[1, 1].set_xlim(0, 255)

    for ax in axes.flat:
        ax.set_xlabel("Рівень інтенсивності (0..255)")
        ax.set_ylabel("Кількість пікселів")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_plot_path) or '.', exist_ok=True)
    plt.savefig(output_plot_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close()

    return output_plot_path


def plot_grayscale_histogram(input_path, output_plot_path="output/histogram_gray.png", show=False):
    """
    Будує гістограму яскравості для монохромного зображення у градаціях сірого.
    """
    pixels, w, h, _ = load_image(input_path)
    gray_vals = [p[0] for p in pixels]
    hist_gray = algos.build_histogram(gray_vals)

    x_levels = list(range(256))
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.canvas.manager.set_window_title("Гістограма відтінків сірого")

    ax.bar(x_levels, hist_gray, color='black', width=1.0)
    ax.set_title(f"Гістограма зображення у градаціях сірого: {os.path.basename(input_path)}")
    ax.set_xlabel("Рівень сірого (0..255)")
    ax.set_ylabel("Кількість пікселів")
    ax.set_xlim(0, 255)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_plot_path) or '.', exist_ok=True)
    plt.savefig(output_plot_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close()

    return output_plot_path


def run_grayscale(input_path, output_path="output/grayscale.png"):
    """
    Виконує перетворення у відтінки сірого та зберігає зображення.
    """
    pixels, w, h, _ = load_image(input_path)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    gray_pixels = algos.to_grayscale(pixels)
    save_image(output_path, w, h, gray_pixels)
    return output_path


def run_binarize(input_path, threshold=128, output_path=None):
    """
    Виконує порогову бінаризацію зображення за порогом P.
    """
    pixels, w, h, _ = load_image(input_path)
    if output_path is None:
        output_path = f"output/binarized_p{threshold}.png"
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    bin_pixels = algos.binarize(pixels, threshold=threshold)
    save_image(output_path, w, h, bin_pixels)
    return output_path


def run_negative(input_path, output_path="output/negative.png"):
    """
    Створює негатив зображення та зберігає файл.
    """
    pixels, w, h, _ = load_image(input_path)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    neg_pixels = algos.to_negative(pixels)
    save_image(output_path, w, h, neg_pixels)
    return output_path


def apply_color_transformations(input_path, output_dir="output", threshold=128):
    """
    Виконує всі 4 підзавдання зі зміни кольоровості:
    - Перехід до відтінків сірого
    - Бінаризація за заданим порогом
    - Створення фотографічного негативу
    - Побудова гістограми сірого зображення
    """
    pixels, w, h, _ = load_image(input_path)
    os.makedirs(output_dir, exist_ok=True)

    gray_file = os.path.join(output_dir, "grayscale.png")
    run_grayscale(input_path, gray_file)

    bin_file = os.path.join(output_dir, f"binarized_p{threshold}.png")
    run_binarize(input_path, threshold=threshold, output_path=bin_file)

    neg_file = os.path.join(output_dir, "negative.png")
    run_negative(input_path, neg_file)

    hist_gray_file = os.path.join(output_dir, "histogram_gray.png")
    plot_grayscale_histogram(gray_file, hist_gray_file, show=False)

    return {
        "gray_path": gray_file,
        "bin_path": bin_file,
        "neg_path": neg_file,
        "hist_path": hist_gray_file,
        "threshold": threshold,
        "dimensions": (w, h)
    }

