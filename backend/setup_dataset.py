#!/usr/bin/env python3
"""
Dataset Download and Setup Script for CBVD Cow Behavior Video Dataset
This script downloads the Kaggle dataset and prepares it for training
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import subprocess
from typing import Optional

def check_kaggle_api():
    """Check if Kaggle API is properly configured"""
    try:
        result = subprocess.run(['kaggle', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Kaggle API found")
            return True
        else:
            print("❌ Kaggle API not found")
            return False
    except FileNotFoundError:
        print("❌ Kaggle CLI not installed")
        print("Please install with: pip install kaggle")
        return False

def setup_kaggle_credentials():
    """Guide user through Kaggle API setup"""
    print("\n🔧 Setting up Kaggle API credentials...")
    print("1. Go to https://www.kaggle.com/account")
    print("2. Click 'Create New API Token' under 'API' section")
    print("3. Download kaggle.json file")
    print("4. Place it in ~/.kaggle/ directory")
    
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    kaggle_json = kaggle_dir / 'kaggle.json'
    if not kaggle_json.exists():
        print(f"\n📁 Please copy your kaggle.json to: {kaggle_json}")
        input("Press Enter after you've placed kaggle.json in the directory...")
    
    # Set proper permissions
    if kaggle_json.exists():
        os.chmod(kaggle_json, 0o600)
        print("✅ Kaggle credentials configured")
        return True
    else:
        print("❌ kaggle.json not found")
        return False

def download_dataset(dataset_name: str, output_dir: Path) -> bool:
    """Download dataset from Kaggle"""
    try:
        print(f"📥 Downloading {dataset_name}...")
        
        cmd = ['kaggle', 'datasets', 'download', '-d', dataset_name, '-p', str(output_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dataset downloaded successfully")
            return True
        else:
            print(f"❌ Download failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Download error: {str(e)}")
        return False

def extract_dataset(zip_path: Path, extract_dir: Path) -> bool:
    """Extract dataset from zip file"""
    try:
        print(f"📂 Extracting {zip_path.name}...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        print("✅ Dataset extracted successfully")
        return True
        
    except Exception as e:
        print(f"❌ Extraction error: {str(e)}")
        return False

def organize_dataset(raw_dir: Path, organized_dir: Path) -> bool:
    """Organize dataset into YOLO format"""
    try:
        print("🗂️ Organizing dataset for YOLO training...")
        
        # Create organized directory structure
        organized_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (organized_dir / 'images' / 'train').mkdir(parents=True, exist_ok=True)
        (organized_dir / 'images' / 'val').mkdir(parents=True, exist_ok=True)
        (organized_dir / 'images' / 'test').mkdir(parents=True, exist_ok=True)
        (organized_dir / 'labels' / 'train').mkdir(parents=True, exist_ok=True)
        (organized_dir / 'labels' / 'val').mkdir(parents=True, exist_ok=True)
        (organized_dir / 'labels' / 'test').mkdir(parents=True, exist_ok=True)
        
        # Find video files
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(raw_dir.rglob(f'*{ext}'))
        
        print(f"🎥 Found {len(video_files)} video files")
        
        # Process videos (extract frames)
        import cv2
        import numpy as np
        from tqdm import tqdm
        
        frame_count = 0
        for video_file in tqdm(video_files, desc="Processing videos"):
            cap = cv2.VideoCapture(str(video_file))
            
            # Determine split (70% train, 15% val, 15% test)
            video_hash = hash(str(video_file)) % 100
            if video_hash < 70:
                split = 'train'
            elif video_hash < 85:
                split = 'val'
            else:
                split = 'test'
            
            video_frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Extract every 30th frame
                if video_frame_count % 30 == 0:
                    frame_filename = f"{video_file.stem}_frame_{frame_count:06d}.jpg"
                    frame_path = organized_dir / 'images' / split / frame_filename
                    
                    # Save frame
                    cv2.imwrite(str(frame_path), frame)
                    
                    # Create empty label file (would need manual annotation)
                    label_path = organized_dir / 'labels' / split / f"{frame_filename}.txt"
                    label_path.touch()
                    
                    frame_count += 1
                
                video_frame_count += 1
            
            cap.release()
        
        print(f"📸 Extracted {frame_count} frames")
        
        # Create dataset.yaml
        dataset_yaml = organized_dir / 'dataset.yaml'
        yaml_content = f"""
# Cow Behavior Dataset Configuration
path: {organized_dir.absolute()}
train: images/train
val: images/val
test: images/test

# Classes
nc: 10
names: ['cow_eating', 'cow_walking', 'cow_lying_down', 'cow_standing', 
        'cow_socializing', 'cow_distress', 'cow_abnormal_movement',
        'piglet_nursing', 'piglet_fall_risk', 'birth_in_progress']
"""
        
        with open(dataset_yaml, 'w') as f:
            f.write(yaml_content.strip())
        
        print("✅ Dataset organized for YOLO training")
        return True
        
    except Exception as e:
        print(f"❌ Organization error: {str(e)}")
        return False

def create_annotation_guidelines(output_dir: Path):
    """Create annotation guidelines for manual labeling"""
    guidelines = """
# Cow Behavior Dataset Annotation Guidelines

## Classes and Descriptions

1. **cow_eating** - Cow actively eating or feeding
2. **cow_walking** - Cow moving or walking normally
3. **cow_lying_down** - Cow resting or lying down (normal)
4. **cow_standing** - Cow standing still (normal posture)
5. **cow_socializing** - Cow interacting with other animals
6. **cow_distress** - Cow showing signs of distress or illness
7. **cow_abnormal_movement** - Cow moving erratically or with difficulty
8. **piglet_nursing** - Piglet nursing from mother
9. **piglet_fall_risk** - Piglet in dangerous position (near edges, height)
10. **birth_in_progress** - Animal giving birth

## Annotation Format

Use YOLO format: <class_id> <x_center> <y_center> <width> <height>

All values normalized between 0 and 1.

## Quality Guidelines

- Only annotate clearly visible animals
- Bounding boxes should tightly fit the animal
- Minimum confidence: 70% visibility
- occlusion < 30%

## Tools Recommended

- LabelImg (https://github.com/heartexlabs/labelImg)
- CVAT (https://github.com/cvat-ai/cvat)
- Roboflow (https://roboflow.com/)

## Health Indicators to Watch

- Lying down excessively (>70% of observation time)
- Abnormal movement patterns
- Signs of distress (vocalizations, restlessness)
- Isolation from herd
- Changes in eating patterns

## Emergency Detection Priority

1. Piglet fall risks (CRITICAL)
2. Birth complications (HIGH)
3. Signs of severe distress (HIGH)
4. Abnormal movement (MEDIUM)
5. Social isolation (LOW)
"""
    
    guidelines_file = output_dir / 'ANNOTATION_GUIDELINES.md'
    with open(guidelines_file, 'w') as f:
        f.write(guidelines.strip())
    
    print(f"📝 Annotation guidelines created: {guidelines_file}")

def main():
    """Main setup process"""
    print("🐄 Herd Health AI - Dataset Setup")
    print("=" * 50)
    
    # Configuration
    dataset_name = "fandaoerji/cbvd-5cow-behavior-video-dataset"
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    raw_dir = data_dir / 'raw'
    organized_dir = data_dir / 'organized'
    
    # Create directories
    data_dir.mkdir(exist_ok=True)
    raw_dir.mkdir(exist_ok=True)
    organized_dir.mkdir(exist_ok=True)
    
    # Step 1: Check Kaggle API
    if not check_kaggle_api():
        print("\n❌ Please install Kaggle CLI first:")
        print("pip install kaggle")
        return False
    
    # Step 2: Setup credentials
    if not setup_kaggle_credentials():
        return False
    
    # Step 3: Download dataset
    if not download_dataset(dataset_name, raw_dir):
        return False
    
    # Step 4: Extract dataset
    zip_files = list(raw_dir.glob('*.zip'))
    if not zip_files:
        print("❌ No zip file found after download")
        return False
    
    zip_file = zip_files[0]  # Assume first zip file
    if not extract_dataset(zip_file, raw_dir):
        return False
    
    # Step 5: Organize dataset
    if not organize_dataset(raw_dir, organized_dir):
        return False
    
    # Step 6: Create guidelines
    create_annotation_guidelines(organized_dir)
    
    print("\n🎉 Dataset setup completed!")
    print(f"📁 Dataset location: {organized_dir}")
    print("\n📋 Next Steps:")
    print("1. Manually annotate the extracted frames")
    print("2. Run training: python train_model.py")
    print("3. Start the backend: python main.py")
    print("4. Access camera monitoring: http://localhost:3000/camera")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
