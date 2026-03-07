#!/usr/bin/env python3
"""
Synthetic Dataset Generator for Herd Health AI
Creates sample images and annotations for demonstration purposes
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json
from typing import List, Tuple
import random

class SyntheticDatasetGenerator:
    """Generate synthetic cow behavior dataset for demonstration"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.class_names = [
            'cow_eating', 'cow_walking', 'cow_lying_down', 'cow_standing',
            'cow_socializing', 'cow_distress', 'cow_abnormal_movement',
            'piglet_nursing', 'piglet_fall_risk', 'birth_in_progress'
        ]
        
        # Colors for different classes (for visualization)
        self.class_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (128, 128, 0), (128, 0, 128),
            (0, 128, 128), (255, 165, 0)
        ]
        
    def create_synthetic_image(self, width: int = 640, height: int = 480) -> np.ndarray:
        """Create a synthetic farm background image"""
        # Create gradient background (sky)
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sky gradient
        for i in range(height // 2):
            color_value = int(135 + (i / (height // 2)) * 50)  # Light blue to darker blue
            image[i, :] = [color_value, color_value + 20, 255]
        
        # Ground
        ground_color = [34, 139, 34]  # Forest green
        image[height // 2:, :] = ground_color
        
        # Add some texture/noise to ground
        noise = np.random.randint(-20, 20, (height // 2, width, 3), dtype=np.int16)
        image[height // 2:] = np.clip(image[height // 2:].astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add some random patches for variation
        for _ in range(random.randint(3, 8)):
            x = random.randint(0, width - 50)
            y = random.randint(height // 2, height - 50)
            w = random.randint(30, 80)
            h = random.randint(20, 60)
            
            patch_color = [
                random.randint(20, 60),
                random.randint(100, 180),
                random.randint(20, 60)
            ]
            cv2.rectangle(image, (x, y), (x + w, y + h), patch_color, -1)
        
        return image
    
    def draw_cow_shape(self, image: np.ndarray, x: int, y: int, width: int, height: int, 
                       class_id: int) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
        """Draw a synthetic cow shape and return YOLO format bbox"""
        
        # Body (ellipse)
        body_color = self.class_colors[class_id]
        
        # Main body
        cv2.ellipse(image, (x + width // 2, y + height // 2), 
                    (width // 2, height // 3), 0, 0, 360, body_color, -1)
        
        # Head
        head_size = min(width, height) // 4
        head_x = x + width - head_size // 2
        head_y = y + height // 2 - head_size // 2
        cv2.circle(image, (head_x, head_y), head_size // 2, body_color, -1)
        
        # Legs (rectangles)
        leg_width = width // 8
        leg_height = height // 3
        for i in range(4):
            leg_x = x + (i + 1) * width // 5 - leg_width // 2
            leg_y = y + height - leg_height
            cv2.rectangle(image, (leg_x, leg_y), 
                         (leg_x + leg_width, y + height), body_color, -1)
        
        # Add class-specific features
        if class_id == 0:  # cow_eating - add food bowl
            bowl_color = [139, 69, 19]  # Brown
            cv2.ellipse(image, (x + width // 2, y + height - 10), 
                       (width // 4, height // 8), 0, 0, 180, bowl_color, -1)
        
        elif class_id == 2:  # cow_lying_down - make body horizontal
            cv2.ellipse(image, (x + width // 2, y + height // 2), 
                       (width // 2, height // 6), 0, 0, 360, body_color, -1)
        
        elif class_id == 5:  # cow_distress - add red indicator
            cv2.circle(image, (head_x, head_y), head_size // 3, [0, 0, 255], 2)
        
        elif class_id == 7:  # piglet_nursing - smaller size
            cv2.ellipse(image, (x + width // 2, y + height // 2), 
                       (width // 3, height // 4), 0, 0, 360, [255, 192, 203], -1)
        
        elif class_id == 8:  # piglet_fall_risk - add warning triangle
            triangle_points = [
                (x + width // 2, y - 20),
                (x + width // 2 - 15, y),
                (x + width // 2 + 15, y)
            ]
            cv2.drawContours(image, [np.array(triangle_points)], 0, [255, 255, 0], -1)
        
        # Calculate YOLO format bbox (normalized)
        x_center = (x + width // 2) / image.shape[1]
        y_center = (y + height // 2) / image.shape[0]
        bbox_width = width / image.shape[1]
        bbox_height = height / image.shape[0]
        
        return image, (x_center, y_center, bbox_width, bbox_height)
    
    def generate_annotation_file(self, label_path: Path, annotations: List[Tuple[int, float, float, float, float]]):
        """Generate YOLO format annotation file"""
        with open(label_path, 'w') as f:
            for class_id, x_center, y_center, width, height in annotations:
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    def generate_dataset(self, num_train: int = 42, num_val: int = 9, num_test: int = 9):
        """Generate complete synthetic dataset"""
        print("🎨 Generating synthetic dataset...")
        
        # Create directory structure
        for split in ['train', 'val', 'test']:
            (self.output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
            (self.output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)
        
        # Generate images for each split
        splits = [
            ('train', num_train),
            ('val', num_val),
            ('test', num_test)
        ]
        
        image_counter = 0
        
        for split_name, num_images in splits:
            print(f"  Generating {num_images} {split_name} images...")
            
            for i in range(num_images):
                # Create synthetic image
                image = self.create_synthetic_image(640, 480)
                
                # Add random number of animals (1-3)
                annotations = []
                num_animals = random.randint(1, 3)
                
                for _ in range(num_animals):
                    # Random position and size
                    x = random.randint(50, 400)
                    y = random.randint(100, 350)
                    width = random.randint(80, 150)
                    height = random.randint(60, 100)
                    
                    # Random class (with bias towards common behaviors)
                    class_weights = [0.2, 0.15, 0.15, 0.15, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05]
                    class_id = random.choices(range(len(self.class_names)), weights=class_weights)[0]
                    
                    # Draw animal and get annotation
                    image, bbox = self.draw_cow_shape(image, x, y, width, height, class_id)
                    
                    # Add to annotations
                    annotations.append((class_id, *bbox))
                
                # Save image
                image_filename = f"synthetic_{split_name}_{image_counter:04d}.jpg"
                image_path = self.output_dir / 'images' / split_name / image_filename
                cv2.imwrite(str(image_path), image)
                
                # Save annotation
                label_filename = f"synthetic_{split_name}_{image_counter:04d}.txt"
                label_path = self.output_dir / 'labels' / split_name / label_filename
                self.generate_annotation_file(label_path, annotations)
                
                image_counter += 1
        
        print(f"✅ Generated {image_counter} synthetic images")
        
        # Generate dataset statistics
        stats = {
            'total_images': image_counter,
            'train_images': num_train,
            'val_images': num_val,
            'test_images': num_test,
            'classes': self.class_names,
            'image_size': [640, 480],
            'format': 'YOLO',
            'synthetic': True,
            'purpose': 'Demonstration and testing'
        }
        
        with open(self.output_dir / 'dataset_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print("📊 Dataset statistics saved to dataset_stats.json")
        
        # Create sample annotation viewer
        self.create_annotation_samples()
        
        return stats
    
    def create_annotation_samples(self):
        """Create a few sample images with visible bounding boxes for demonstration"""
        print("🎯 Creating annotation samples...")
        
        sample_dir = self.output_dir / 'samples'
        sample_dir.mkdir(exist_ok=True)
        
        for class_id, class_name in enumerate(self.class_names[:5]):  # First 5 classes
            # Create image
            image = self.create_synthetic_image(640, 480)
            
            # Add single animal
            x, y = 200, 200
            width, height = 120, 80
            
            image, bbox = self.draw_cow_shape(image, x, y, width, height, class_id)
            
            # Draw bounding box
            x1 = int((bbox[0] - bbox[2] / 2) * image.shape[1])
            y1 = int((bbox[1] - bbox[3] / 2) * image.shape[0])
            x2 = int((bbox[0] + bbox[2] / 2) * image.shape[1])
            y2 = int((bbox[1] + bbox[3] / 2) * image.shape[0])
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            # Add label
            label = f"{class_name} ({class_id})"
            cv2.putText(image, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Save sample
            sample_path = sample_dir / f"sample_{class_name}.jpg"
            cv2.imwrite(str(sample_path), image)
        
        print("✅ Annotation samples created in /samples directory")

def main():
    """Main function to generate the synthetic dataset"""
    # Set up paths
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Initialize generator
    generator = SyntheticDatasetGenerator(data_dir)
    
    # Generate dataset
    stats = generator.generate_dataset(num_train=42, num_val=9, num_test=9)
    
    print("\n🎉 Synthetic dataset generation completed!")
    print(f"📁 Dataset location: {data_dir}")
    print(f"📊 Total images: {stats['total_images']}")
    print(f"🏷️  Classes: {len(stats['classes'])}")
    print("\n📋 Dataset structure:")
    print("data/")
    print("├── dataset.yaml")
    print("├── dataset_stats.json")
    print("├── images/")
    print("│   ├── train/ (42 images)")
    print("│   ├── val/ (9 images)")
    print("│   └── test/ (9 images)")
    print("├── labels/")
    print("│   ├── train/ (42 labels)")
    print("│   ├── val/ (9 labels)")
    print("│   └── test/ (9 labels)")
    print("└── samples/ (5 annotated samples)")
    
    print("\n🚀 Ready for training!")
    print("Run: python train_model.py")

if __name__ == "__main__":
    main()
