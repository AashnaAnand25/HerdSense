#!/usr/bin/env python3
"""
Convert archive CBVD-5 annotations (VIA format) to YOLO format for training.

Archive = real CBVD-5 cow behavior annotations (stand, lying down, foraging, etc.).
data/data/ = synthetically generated dataset (different classes).

Usage:
  1. Download CBVD-5 frames (or extract from Kaggle videos) into a folder, e.g.:
     backend/data/archive_frames/
  2. Run:
     cd backend/data && python convert_archive_to_yolo.py --images archive_frames
  3. Train:
     cd backend && python train_model.py --data data/archive_yolo/dataset.yaml

Output: backend/data/archive_yolo/ with images/train|val|test, labels/train|val|test, dataset.yaml
"""

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
import random

# CBVD-5 classes from archive/annotations/labelmap.txt (0-indexed in metadata)
ARCHIVE_CLASSES = ["stand", "lying_down", "foraging", "drinking_water", "rumination"]


def parse_csv_row(row):
    """Parse a VIA-export CSV row. Returns (filename, x, y, w, h, class_ids)."""
    if len(row) < 6:
        return None
    file_list_str = row[1].strip()
    spatial_str = row[4].strip()
    metadata_str = row[5].strip()
    # File list: ["618_00002.jpg"] -> 618_00002.jpg
    match = re.search(r'"([^"]+\.jpg)"', file_list_str)
    if not match:
        return None
    filename = match.group(1)
    # Spatial: [2, x, y, width, height]
    match = re.search(r"\[2,([\d.]+),([\d.]+),([\d.]+),([\d.]+)\]", spatial_str)
    if not match:
        return None
    x, y, w, h = float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4))
    # Metadata: {"1":"0,4"} -> first class id = 0
    match = re.search(r'"1"\s*:\s*"(\d+)', metadata_str)
    class_id = int(match.group(1)) if match else 0
    return (filename, x, y, w, h, class_id)


def get_image_size(images_dir: Path, filename: str):
    """Return (width, height) for image; fallback (1920, 1080) if not found."""
    try:
        import cv2
        path = images_dir / filename
        if path.exists():
            img = cv2.imread(str(path))
            if img is not None:
                h, w = img.shape[:2]
                return w, h
    except Exception:
        pass
    return 1920, 1080


def to_yolo_line(x, y, w, h, class_id, img_w, img_h):
    """Convert absolute bbox to YOLO normalized (class_id x_center y_center width height)."""
    x_center = x + w / 2
    y_center = y + h / 2
    xc_n = x_center / img_w
    yc_n = y_center / img_h
    wn = w / img_w
    hn = h / img_h
    return f"{class_id} {xc_n:.6f} {yc_n:.6f} {wn:.6f} {hn:.6f}"


def main():
    parser = argparse.ArgumentParser(description="Convert CBVD-5 archive annotations to YOLO")
    parser.add_argument(
        "--images",
        type=str,
        default="archive_frames",
        help="Directory containing CBVD frame images (e.g. 618_00002.jpg). Relative to backend/data/ or absolute.",
    )
    parser.add_argument("--csv", type=str, default=None, help="Path to CBVD-5.csv (default: backend/data/archive/CBVD-5.csv)")
    parser.add_argument("--out", type=str, default="archive_yolo", help="Output directory name under backend/data/")
    parser.add_argument("--split", type=str, default="0.7,0.15,0.15", help="Train,val,test fractions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for split")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    data_root = script_dir
    csv_path = Path(args.csv) if args.csv else data_root / "archive" / "CBVD-5.csv"
    images_dir = data_root / args.images if not Path(args.images).is_absolute() else Path(args.images)
    out_dir = data_root / args.out

    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        print("  Archive annotations are in backend/data/archive/CBVD-5.csv")
        return 1
    if not images_dir.exists():
        print(f"⚠️ Images directory not found: {images_dir}")
        print("  Download CBVD-5 from Kaggle and place frame images (e.g. 618_00002.jpg) there,")
        print("  or extract frames from videos and name them to match the CSV.")
        return 1

    train_r, val_r, test_r = [float(x) for x in args.split.split(",")]
    assert abs(train_r + val_r + test_r - 1.0) < 1e-6, "Split must sum to 1"

    # Parse CSV and group by image
    by_image = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            row = list(csv.reader([line]))[0]
            parsed = parse_csv_row(row)
            if parsed is None:
                continue
            filename, x, y, w, h, class_id = parsed
            if filename not in by_image:
                by_image[filename] = []
            by_image[filename].append((x, y, w, h, class_id))

    if not by_image:
        print("❌ No valid rows in CSV")
        return 1

    # Only include images that exist in the images dir
    names = [fn for fn in by_image.keys() if (images_dir / fn).exists()]
    missing = len(by_image) - len(names)
    if missing:
        print(f"⚠️ {missing} images from CSV not found in {images_dir} (skipped)")
    if not names:
        print("❌ No image files found; add CBVD frame images to the --images directory.")
        return 1

    # Split image names
    random.seed(args.seed)
    random.shuffle(names)
    n = len(names)
    n_train = int(n * train_r)
    n_val = int(n * val_r)
    n_test = n - n_train - n_val
    splits = {
        "train": names[: n_train],
        "val": names[n_train : n_train + n_val],
        "test": names[n_train + n_val :],
    }

    # Create output dirs
    for split in splits:
        (out_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (out_dir / "labels" / split).mkdir(parents=True, exist_ok=True)

    try:
        import cv2
        has_cv = True
    except ImportError:
        has_cv = False

    for split, filenames in splits.items():
        for fn in filenames:
            src = images_dir / fn
            dst_img = out_dir / "images" / split / fn
            dst_lbl = out_dir / "labels" / split / (Path(fn).stem + ".txt")
            shutil.copy2(src, dst_img)
            img_w, img_h = get_image_size(images_dir, fn) if has_cv else (1920, 1080)
            lines = []
            for (x, y, w, h, cid) in by_image[fn]:
                lines.append(to_yolo_line(x, y, w, h, cid, img_w, img_h))
            dst_lbl.write_text("\n".join(lines) + "\n" if lines else "")

    # dataset.yaml
    yaml_path = out_dir / "dataset.yaml"
    yaml_path.write_text(f"""# YOLO dataset from archive CBVD-5 annotations
path: {out_dir.resolve()}
train: images/train
val: images/val
test: images/test
nc: {len(ARCHIVE_CLASSES)}
names: {ARCHIVE_CLASSES}
""")

    print(f"✅ Converted {len(by_image)} images to YOLO at {out_dir}")
    print(f"   train={len(splits['train'])}, val={len(splits['val'])}, test={len(splits['test'])}")
    print(f"   dataset.yaml: {yaml_path}")
    print("   Train with: cd backend && python train_model.py --data data/archive_yolo/dataset.yaml")
    return 0


if __name__ == "__main__":
    exit(main())
