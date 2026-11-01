# -*- coding: utf-8 -*-
"""
Модуль дискових операцій, візуалізації та пакетного аналізу для Лабораторної роботи №6.
Дисципліна: 'Комп'ютерна графіка та візуалізація'.
"""

import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lab6_manual_algorithms as algos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SAMPLE_PATH = os.path.join(BASE_DIR, "samples", "sample_test.bmp")
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def resolve_existing_path(path):
    """
    Знаходить дійсний шлях до файлу: якщо відносний шлях не знайдено в CWD,
    шукає його відносно каталогу модуля (BASE_DIR).
    """
    if not path:
        return DEFAULT_SAMPLE_PATH
    if os.path.isabs(path) and os.path.exists(path):
        return path
    if os.path.exists(path):
        return os.path.abspath(path)
    cand = os.path.join(BASE_DIR, path)
    if os.path.exists(cand):
        return cand
    return os.path.abspath(path)


def resolve_output_dir(dir_path):
    """
    Знаходить дійсний каталог для вихідних файлів.
    """
    if not dir_path:
        return DEFAULT_OUTPUT_DIR
    if os.path.isabs(dir_path):
        return dir_path
    if os.path.isdir(dir_path):
        return os.path.abspath(dir_path)
    return os.path.join(BASE_DIR, dir_path)


AVAILABLE_FILTERS = [
    ("L1: Box Mean 3x3", "linear", lambda p, w, h: algos.apply_linear_filter(p, w, h, algos.get_box_filter_kernel(3))),
    ("L2: Box Mean 5x5", "linear", lambda p, w, h: algos.apply_linear_filter(p, w, h, algos.get_box_filter_kernel(5))),
    ("L3: Gaussian 3x3", "linear", lambda p, w, h: algos.apply_linear_filter(p, w, h, algos.get_gaussian_3x3_kernel())),
    ("L4: Gaussian 5x5", "linear", lambda p, w, h: algos.apply_linear_filter(p, w, h, algos.get_gaussian_5x5_kernel())),
    ("NL1: Median 3x3", "non-linear", lambda p, w, h: algos.apply_median_filter(p, w, h, radius=1)),
    ("NL2: Median 5x5", "non-linear", lambda p, w, h: algos.apply_median_filter(p, w, h, radius=2)),
    ("NL3: Median 7x7", "non-linear", lambda p, w, h: algos.apply_median_filter(p, w, h, radius=3)),
    ("NL4: Min Filter 3x3", "non-linear", lambda p, w, h: algos.apply_min_filter(p, w, h, radius=1)),
    ("NL5: Max Filter 3x3", "non-linear", lambda p, w, h: algos.apply_max_filter(p, w, h, radius=1)),
    ("NL6: Midpoint 3x3", "non-linear", lambda p, w, h: algos.apply_midpoint_filter(p, w, h, radius=1)),
    ("NL7: Alpha-trimmed 3x3", "non-linear", lambda p, w, h: algos.apply_alpha_trimmed_mean_filter(p, w, h, radius=1, d=4)),
    ("NL8: Adaptive Median", "non-linear", lambda p, w, h: algos.apply_adaptive_median_filter(p, w, h, max_radius=2)),
]


def load_image(file_path):
    """
    Завантажує зображення з диска та повертає список кортежів пікселів (R, G, B).
    """
    resolved_path = resolve_existing_path(file_path)
    if not os.path.exists(resolved_path):
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    with Image.open(resolved_path) as img:
        img_rgb = img.convert('RGB')
        w, h = img_rgb.size
        pixels = list(img_rgb.getdata())
        return pixels, w, h, img.format or "BMP"


def save_image(output_path, width, height, pixels, img_format="BMP"):
    """
    Зберігає одновимірний список пікселів у файл заданого формату (за замовчуванням BMP).
    """
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    img = Image.new('RGB', (width, height))
    clean_rgb = [(p[0], p[1], p[2]) for p in pixels]
    img.putdata(clean_rgb)
    img.save(output_path, format=img_format)
    return output_path


def prepare_9_test_images(source_path=None, output_dir=None):
    """
    Формує набір з 9 цифрових зображень розміром 128х128 у форматі BMP:
    0: f0 - без шуму
    1: f1 - адитивний гаусів шум (дисперсія sigma=15)
    2: f2 - адитивний гаусів шум (дисперсія sigma=30)
    3: f3 - імпульсний шум 'сіль і перець' (prob=0.05)
    4: f4 - імпульсний шум 'сіль і перець' (prob=0.15)
    5: f5 - просторово-нестаціонарний адитивний шум від рівня яскравості (alpha=1.5)
    6: f6 - просторово-нестаціонарний адитивний шум від рівня яскравості (alpha=3.5)
    7: f7 - просторово-нестаціонарний адитивний шум як лінійна функція координат (sigma in [5, 35])
    8: f8 - просторово-нестаціонарний адитивний шум як радіальна функція координат (sigma in [5, 40])
    """
    source_path = resolve_existing_path(source_path)
    output_dir = resolve_output_dir(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    pixels, w, h, _ = load_image(source_path)

    if w != 128 or h != 128:
        with Image.open(source_path) as img:
            img_res = img.convert('RGB').resize((128, 128), Image.Resampling.LANCZOS)
            pixels = list(img_res.getdata())
            w, h = 128, 128

    noise_definitions = [
        ("image0.bmp", "f0: Без шуму (оригінал)", pixels),
        ("image1.bmp", "f1: Гаусів адитивний (sigma=15)", algos.add_gaussian_noise(pixels, w, h, mean=0.0, sigma=15.0, seed=101)),
        ("image2.bmp", "f2: Гаусів адитивний (sigma=30)", algos.add_gaussian_noise(pixels, w, h, mean=0.0, sigma=30.0, seed=102)),
        ("image3.bmp", "f3: Імпульсний p=0.05", algos.add_impulse_noise(pixels, w, h, prob=0.05, seed=103)),
        ("image4.bmp", "f4: Імпульсний p=0.15", algos.add_impulse_noise(pixels, w, h, prob=0.15, seed=104)),
        ("image5.bmp", "f5: Нестаціонарний sigma(Y), alpha=1.5", algos.add_brightness_dependent_noise(pixels, w, h, alpha=1.5, seed=105)),
        ("image6.bmp", "f6: Нестаціонарний sigma(Y), alpha=3.5", algos.add_brightness_dependent_noise(pixels, w, h, alpha=3.5, seed=106)),
        ("image7.bmp", "f7: Нестаціонарний sigma(x,y) лінійний", algos.add_spatial_coordinate_noise(pixels, w, h, sigma_min=5.0, sigma_max=35.0, mode='linear', seed=107)),
        ("image8.bmp", "f8: Нестаціонарний sigma(x,y) радіальний", algos.add_spatial_coordinate_noise(pixels, w, h, sigma_min=5.0, sigma_max=40.0, mode='radial', seed=108)),
    ]

    saved_paths = []
    for filename, title, px_data in noise_definitions:
        file_path = os.path.join(output_dir, filename)
        save_image(file_path, w, h, px_data, img_format="BMP")
        saved_paths.append((file_path, title, px_data))

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    fig.suptitle("Набір 9 тестових зображень 128х128 (Лабораторна робота №6)", fontsize=13, fontweight='bold')

    for idx, (file_path, title, px_data) in enumerate(saved_paths):
        ax = axes[idx // 3, idx % 3]
        img_arr = Image.new('RGB', (w, h))
        img_arr.putdata([(p[0], p[1], p[2]) for p in px_data])
        ax.imshow(img_arr)
        ax.set_title(title, fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    collage_path = os.path.join(output_dir, "comparison_9_test_images.png")
    plt.savefig(collage_path, dpi=200, bbox_inches='tight')
    plt.close()

    return saved_paths, collage_path


def evaluate_f0_distortion(output_dir=None):
    """
    Застосовує обрані фільтри до неспотвореного зображення f0 та оцінює
    величину спотворення epsilon_A0^2 та PSNR.
    """
    output_dir = resolve_output_dir(output_dir)
    f0_path = os.path.join(output_dir, "image0.bmp")
    if not os.path.exists(f0_path):
        raise FileNotFoundError(f"Файл {f0_path} не знайдено. Спочатку згенеруйте набір зображень.")

    pixels_f0, w, h, _ = load_image(f0_path)
    results = []

    f0_out_dir = os.path.join(output_dir, "f0_filtered")
    os.makedirs(f0_out_dir, exist_ok=True)

    for filter_name, f_type, func in AVAILABLE_FILTERS:
        filtered_pixels = func(pixels_f0, w, h)
        distortion = algos.calculate_distortion(filtered_pixels, pixels_f0)
        psnr = algos.calculate_psnr(filtered_pixels, pixels_f0)

        safe_name = filter_name.replace(" ", "_").replace(":", "").replace("/", "_").lower()
        out_path = os.path.join(f0_out_dir, f"f0_{safe_name}.bmp")
        save_image(out_path, w, h, filtered_pixels, img_format="BMP")

        results.append({
            "name": filter_name,
            "type": f_type,
            "distortion": distortion,
            "psnr": psnr,
            "pixels": filtered_pixels,
            "path": out_path
        })

    fig, axes = plt.subplots(3, 4, figsize=(14, 10))
    fig.suptitle("Спотворення тестового зображення f0(i,j) різними фільтрами", fontsize=13, fontweight='bold')

    for idx, item in enumerate(results):
        ax = axes[idx // 4, idx % 4]
        img_arr = Image.new('RGB', (w, h))
        img_arr.putdata([(p[0], p[1], p[2]) for p in item["pixels"]])
        ax.imshow(img_arr)
        ax.set_title(f"{item['name']}\neps^2={item['distortion']:.2f}, PSNR={item['psnr']:.1f} dB", fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    collage_path = os.path.join(output_dir, "comparison_f0_filters.png")
    plt.savefig(collage_path, dpi=200, bbox_inches='tight')
    plt.close()

    return results, collage_path


def evaluate_all_noisy_images(output_dir=None):
    """
    Застосовує всі фільтри до всіх зашумлених зображень f1..f8,
    обчислює метрики epsilon_Ak^2, MSE відносно f0, PSNR,
    та визначає оптимальний фільтр для кожного типу шуму.
    """
    output_dir = resolve_output_dir(output_dir)
    f0_path = os.path.join(output_dir, "image0.bmp")
    if not os.path.exists(f0_path):
        raise FileNotFoundError(f"Файл {f0_path} не знайдено.")

    pixels_f0, w, h, _ = load_image(f0_path)

    noise_labels = [
        (1, "f1 (Гаус sigma=15)"),
        (2, "f2 (Гаус sigma=30)"),
        (3, "f3 (Імпульсний p=0.05)"),
        (4, "f4 (Імпульсний p=0.15)"),
        (5, "f5 (Нестац. яскравість a=1.5)"),
        (6, "f6 (Нестац. яскравість a=3.5)"),
        (7, "f7 (Нестац. коорд. лінійний)"),
        (8, "f8 (Нестац. коорд. радіальний)"),
    ]

    all_evaluations = {}

    for k, label in noise_labels:
        img_path = os.path.join(output_dir, f"image{k}.bmp")
        pixels_fk, _, _, _ = load_image(img_path)

        noise_raw_mse = algos.calculate_mse(pixels_fk, pixels_f0)
        noise_raw_psnr = algos.calculate_psnr(pixels_fk, pixels_f0)

        filter_scores = []
        best_filter = None
        best_psnr = -1.0

        for filter_name, f_type, func in AVAILABLE_FILTERS:
            filtered_px = func(pixels_fk, w, h)
            eps_ak = algos.calculate_distortion(filtered_px, pixels_fk)
            mse_f0 = algos.calculate_mse(filtered_px, pixels_f0)
            psnr_f0 = algos.calculate_psnr(filtered_px, pixels_f0)

            score_entry = {
                "filter_name": filter_name,
                "type": f_type,
                "eps_ak": eps_ak,
                "mse_to_f0": mse_f0,
                "psnr_to_f0": psnr_f0,
                "filtered_pixels": filtered_px
            }
            filter_scores.append(score_entry)

            if psnr_f0 > best_psnr:
                best_psnr = psnr_f0
                best_filter = score_entry

        all_evaluations[k] = {
            "label": label,
            "raw_mse": noise_raw_mse,
            "raw_psnr": noise_raw_psnr,
            "scores": filter_scores,
            "best_filter": best_filter,
            "noisy_pixels": pixels_fk
        }

    fig, axes = plt.subplots(4, 4, figsize=(16, 16))
    fig.suptitle("Порівняння зашумлених зображень та результатів їх оптимальної фільтрації", fontsize=14, fontweight='bold')

    for idx, (k, label) in enumerate(noise_labels):
        row = (idx * 2) // 4
        col_noisy = (idx * 2) % 4
        col_filt = col_noisy + 1

        noisy_ax = axes[row, col_noisy]
        filt_ax = axes[row, col_filt]

        img_noisy = Image.new('RGB', (w, h))
        img_noisy.putdata([(p[0], p[1], p[2]) for p in all_evaluations[k]["noisy_pixels"]])
        noisy_ax.imshow(img_noisy)
        noisy_ax.set_title(f"{label}\nPSNR={all_evaluations[k]['raw_psnr']:.1f} dB", fontsize=9)
        noisy_ax.axis('off')

        best_entry = all_evaluations[k]["best_filter"]
        img_filt = Image.new('RGB', (w, h))
        img_filt.putdata([(p[0], p[1], p[2]) for p in best_entry["filtered_pixels"]])
        filt_ax.imshow(img_filt)
        filt_ax.set_title(f"Найкращий: {best_entry['filter_name']}\nPSNR={best_entry['psnr_to_f0']:.1f} dB (+{best_entry['psnr_to_f0'] - all_evaluations[k]['raw_psnr']:.1f})", fontsize=9, color='darkgreen')
        filt_ax.axis('off')

    plt.tight_layout()
    comparison_grid_path = os.path.join(output_dir, "comparison_noise_vs_filtering.png")
    plt.savefig(comparison_grid_path, dpi=200, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(figsize=(14, 7))
    categories = [lbl for _, lbl in noise_labels]
    x_positions = range(len(categories))
    raw_psnrs = [all_evaluations[k]["raw_psnr"] for k, _ in noise_labels]
    best_psnrs = [all_evaluations[k]["best_filter"]["psnr_to_f0"] for k, _ in noise_labels]

    bar_width = 0.35
    ax.bar([x - bar_width/2 for x in x_positions], raw_psnrs, width=bar_width, label='Вихідний шум (Raw PSNR)', color='#d9534f')
    ax.bar([x + bar_width/2 for x in x_positions], best_psnrs, width=bar_width, label='Після найкращого фільтра (Filtered PSNR)', color='#5cb85c')

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(categories, rotation=25, ha='right', fontsize=9)
    ax.set_ylabel('PSNR (дБ)', fontsize=11)
    ax.set_title('Ефективність усунення шуму: приріст PSNR для кожного типу шуму', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    metrics_chart_path = os.path.join(output_dir, "comparison_metrics_matrix.png")
    plt.savefig(metrics_chart_path, dpi=200, bbox_inches='tight')
    plt.close()

    return all_evaluations, comparison_grid_path, metrics_chart_path
