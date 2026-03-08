#!/usr/bin/env python3
"""
Quick setup script to check and prepare CBVD-5 data for training.
"""

import os
from pathlib import Path
import subprocess

def check_dataset_status():
    """Check what data we have available"""
    print("🔍 Checking dataset status...")
    
    # Check archive data
    archive_csv = Path("data/archive/CBVD-5.csv")
    archive_frames = Path("data/archive_frames")
    archive_yolo = Path("data/archive_yolo/dataset.yaml")
    
    print(f"📄 CBVD-5 CSV: {'✅' if archive_csv.exists() else '❌'} {archive_csv}")
    print(f"🖼️  Archive frames: {'✅' if archive_frames.exists() else '❌'} {archive_frames}")
    print(f"📋 YOLO dataset: {'✅' if archive_yolo.exists() else '❌'} {archive_yolo}")
    
    if archive_csv.exists():
        # Count annotations
        try:
            with open(archive_csv, 'r') as f:
                lines = f.readlines()
                annotations = len([l for l in lines if not l.startswith('#') and l.strip()])
            print(f"📊 Total annotations: {annotations}")
        except:
            pass
    
    if archive_frames.exists():
        # Count images
        images = list(archive_frames.glob('*.jpg')) + list(archive_frames.glob('*.png'))
        print(f"🖼️  Total images: {len(images)}")
        if images:
            print(f"   Sample images: {[img.name for img in images[:3]]}")
    
    return archive_csv.exists(), archive_frames.exists(), archive_yolo.exists()

def setup_training():
    """Setup training with available data"""
    csv_ok, frames_ok, yolo_ok = check_dataset_status()
    
    print("\n" + "="*50)
    
    if yolo_ok:
        print("✅ YOLO dataset ready! You can start training:")
        print("   python train_optimized.py --epochs 30")
        return True
    
    elif csv_ok and not frames_ok:
        print("⚠️  You have annotations but no frame images.")
        print("💡 To fix this:")
        print("   1. Download CBVD-5 from: https://www.kaggle.com/datasets/fandaoerji/cbvd-5cow-behavior-video-dataset")
        print("   2. Extract video frames to: data/archive_frames/")
        print("   3. Make sure frame names match the CSV (e.g., 618_00002.jpg)")
        return False
    
    elif csv_ok and frames_ok:
        print("✅ You have both CSV and frames! Converting to YOLO format...")
        try:
            result = subprocess.run([
                'python', 'data/convert_archive_to_yolo.py',
                '--images', 'archive_frames'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Conversion successful! You can now train:")
                print("   python train_optimized.py --epochs 30")
                return True
            else:
                print(f"❌ Conversion failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    else:
        print("❌ No CBVD-5 data found.")
        print("💡 To get started:")
        print("   1. Download CBVD-5 dataset from Kaggle")
        print("   2. Place CBVD-5.csv in: data/archive/")
        print("   3. Extract frames to: data/archive_frames/")
        print("   4. Run this script again")
        return False

def main():
    print("🐄 HerdSense AI - Training Setup")
    print("=" * 50)
    
    ready = setup_training()
    
    if ready:
        print("\n🚀 Ready to train! Choose your training mode:")
        print("   Quick test (10 epochs): python train_optimized.py --quick")
        print("   Full training (30 epochs): python train_optimized.py --epochs 30")
        print("   Custom epochs: python train_optimized.py --epochs 50")
    else:
        print("\n❌ Setup incomplete. Please follow the steps above.")

if __name__ == "__main__":
    main()
