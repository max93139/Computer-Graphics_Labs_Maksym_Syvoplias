# -*- coding: utf-8 -*-
"""
Операції вводу/виводу та обробки для Лабораторної роботи №5.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.
"""

import os
from PIL import Image
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


def run_add_noise(input_path, output_path="output/noisy_image.png", count=1000):
    """
    Додає штучний імпульсний шум до зображення та зберігає файл.
    """
    pixels, w, h, _ = load_image(input_path)
    noisy_pixels = algos.add_noise(pixels, w, h, count=count, noise_color=(0, 0, 0))
    save_image(output_path, w, h, noisy_pixels)
    return output_path, w, h


def run_east_mask(input_path, output_path="output/east_mask.png"):
    """
    Застосовує курсову маску 'Схід' до зображення та зберігає файл.
    """
    pixels, w, h, _ = load_image(input_path)
    res_pixels = algos.apply_east_compass_mask(pixels, w, h)
    save_image(output_path, w, h, res_pixels)
    return output_path, w, h
