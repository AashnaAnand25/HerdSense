#!/usr/bin/env python3
"""
Optimized YOLOv8 training for Mac M4 Pro using CBVD-5 archive data.
- Uses MPS (Metal Performance Shaders) acceleration
- Small model (YOLOv8n) to prevent overheating
- Efficient data loading and preprocessing
- Early stopping to prevent overtraining
"""

import torch
import torch.nn as nn
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import yaml
import os
import time
import psutil
import subprocess
from typing import Dict, List

class MacOptimizedTrainer:
    """YOLOv8 trainer optimized for Mac M4 Pro with CBVD-5 data"""
    
    def __init__(self):
        # Check for MPS (Apple Silicon) support
        self.device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
        print(f"🍎 Using device: {self.device}")
        
        # Use smallest model to prevent overheating
        self.model = YOLO('yolov8n.pt')
        
        # CBVD-5 behavior classes (real dataset has 5 classes)
        self.class_names = [
            'standing',      # 0 - stand
            'lying_down',    # 1 - lying_down  
            'grazing',       # 2 - foraging
            'drinking',      # 3 - drinking_water
            'ruminating'     # 4 - rumination
        ]
        
        # Monitoring
        self.start_time = None
        self.max_temp = 75  # Max temp threshold in Celsius
        
    def check_system_status(self):
        """Check system temperature and memory usage"""
        try:
            # Get CPU temperature (macOS specific)
            result = subprocess.run(['sudo', 'powermetrics', '--samplers', 'cpu_power', '-i', '1000'], 
                                capture_output=True, text=True, timeout=2)
            # Parse temperature from powermetrics output
            temp_line = [line for line in result.stdout.split('\n') if 'CPU temperature' in line]
            if temp_line:
                temp = float(temp_line[0].split()[-2])
                if temp > self.max_temp:
                    print(f"🌡️ High temperature detected: {temp}°C - Consider pausing")
                    return False, temp
        except:
            pass
        
        # Check memory usage
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            print(f"💾 High memory usage: {memory.percent:.1f}%")
            return False, None
            
        return True, None
    
    def prepare_archive_dataset(self):
        """Convert CBVD-5 archive data to YOLO format if needed"""
        archive_yaml = Path("data/archive_yolo/dataset.yaml")
        
        if not archive_yaml.exists():
            print("📊 Converting CBVD-5 archive data to YOLO format...")
            
            # Check if we have the frames
            frames_dir = Path("data/archive_frames")
            if not frames_dir.exists():
                print("❌ Archive frames not found in data/archive_frames/")
                print("💡 You need to:")
                print("   1. Download CBVD-5 dataset from Kaggle")
                print("   2. Extract frames to data/archive_frames/")
                print("   3. Run: python data/convert_archive_to_yolo.py --images archive_frames")
                return None
            
            # Run conversion
            try:
                import subprocess
                result = subprocess.run([
                    'python', 'data/convert_archive_to_yolo.py', 
                    '--images', 'archive_frames'
                ], capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    print("✅ Archive data converted successfully")
                    return archive_yaml
                else:
                    print(f"❌ Conversion failed: {result.stderr}")
                    return None
            except Exception as e:
                print(f"❌ Conversion error: {e}")
                return None
        else:
            print("✅ Archive YOLO dataset already exists")
            return archive_yaml
    
    def train_optimized(self, dataset_yaml: str, epochs: int = 50):
        """Train with Mac M4 Pro optimizations"""
        print(f"🚀 Starting optimized training for {epochs} epochs...")
        self.start_time = time.time()
        
        # Optimized training parameters for Mac M4 Pro
        training_args = {
            'data': dataset_yaml,
            'epochs': epochs,
            'imgsz': 416,  # Smaller images = faster training
            'batch': 8,    # Smaller batch for memory efficiency
            'optimizer': 'AdamW',  # Better for small datasets
            'lr0': 0.001,   # Lower learning rate for stability
            'lrf': 0.0001,
            'momentum': 0.9,
            'weight_decay': 0.0005,
            'warmup_epochs': 3,
            'warmup_momentum': 0.8,
            'warmup_bias_lr': 0.1,
            'box': 0.05,
            'cls': 0.5,
            'iou': 0.7,
            'hsv_h': 0.015,
            'hsv_s': 0.5,    # Less augmentation for faster training
            'hsv_v': 0.3,
            'degrees': 5.0,    # Less rotation
            'translate': 0.05,  # Less translation
            'scale': 0.3,      # Less scaling
            'shear': 0.0,
            'perspective': 0.0,
            'flipud': 0.0,
            'fliplr': 0.5,
            'mosaic': 0.5,    # Less mosaic augmentation
            'mixup': 0.0,
            'copy_paste': 0.0,
            'device': str(self.device),
            'project': 'runs/train',
            'name': 'cow_behavior_optimized',
            'exist_ok': True,
            'pretrained': True,
            'resume': False,
            'patience': 15,    # Early stopping
            'save': True,
            'plots': True,
            'close_mosaic': 5,
            'workers': 2,      # Fewer workers for Mac
            'cache': False,     # Don't cache to save memory
        }

        # Start training with monitoring
        epoch_times = []
        for epoch in range(epochs):
            epoch_start = time.time()
            
            # Check system status
            status_ok, temp = self.check_system_status()
            if not status_ok:
                print(f"⚠️ System stress detected at epoch {epoch+1}")
                print("💡 Consider taking a break to let your Mac cool down")
                break
            
            print(f"📚 Epoch {epoch+1}/{epochs}")
            
            # Train one epoch (this is simplified - in reality YOLO handles epochs internally)
            if epoch == 0:
                # Start training
                results = self.model.train(**training_args)
                break  # YOLO handles all epochs internally
            else:
                break
        
        total_time = time.time() - self.start_time
        print(f"✅ Training completed in {total_time/60:.1f} minutes")
        
        return results if 'results' in locals() else None
    
    def evaluate_lightweight(self, dataset_yaml: str):
        """Lightweight evaluation to save resources"""
        print("📊 Running lightweight evaluation...")
        
        try:
            # Run validation with minimal settings
            results = self.model.val(
                data=dataset_yaml,
                split='val',
                imgsz=416,
                batch=8,
                device=str(self.device),
                save_json=False,
                save_hybrid=False,
                plots=False  # Skip plots to save time/memory
            )
            
            # Extract key metrics
            metrics = {
                'precision': float(results.box.mp),
                'recall': float(results.box.mr),
                'mAP50': float(results.box.map50),
                'mAP50_95': float(results.box.map),
                'inference_time': float(results.speed['inference'])
            }
            
            print(f"📈 Performance:")
            print(f"   Precision: {metrics['precision']:.3f}")
            print(f"   Recall: {metrics['recall']:.3f}")
            print(f"   mAP@0.5: {metrics['mAP50']:.3f}")
            print(f"   Inference: {metrics['inference_time']:.1f}ms")
            
            return metrics
        except Exception as e:
            print(f"⚠️ Evaluation failed: {e}")
            return {}
    
    def export_for_vision(self):
        """Export model optimized for vision server"""
        print("📦 Exporting model for vision server...")
        
        try:
            # Export to ONNX for faster inference
            exported_path = self.model.export(
                format='onnx',
                imgsz=416,
                simplify=True,
                opset=12
            )
            
            # Also save PyTorch version as backup
            self.model.save('runs/train/cow_behavior_optimized/weights/best.pt')
            
            print(f"✅ Model exported to {exported_path}")
            return exported_path
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None

def main():
    """Main training pipeline optimized for Mac M4 Pro"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimized YOLOv8 training for Mac M4 Pro")
    parser.add_argument("--epochs", type=int, default=30, help="Training epochs (default: 30)")
    parser.add_argument("--quick", action='store_true', help="Quick training (10 epochs)")
    args = parser.parse_args()
    
    epochs = 10 if args.quick else args.epochs
    
    print("🍎 Mac M4 Pro Optimized Training")
    print("=" * 50)
    
    trainer = MacOptimizedTrainer()
    
    # Prepare dataset
    dataset_yaml = trainer.prepare_archive_dataset()
    if not dataset_yaml:
        print("❌ Dataset preparation failed")
        return 1
    
    # Train model
    results = trainer.train_optimized(str(dataset_yaml), epochs=epochs)
    if not results:
        print("❌ Training failed")
        return 1
    
    # Evaluate
    metrics = trainer.evaluate_lightweight(str(dataset_yaml))
    
    # Export for vision server
    trainer.export_for_vision()
    
    print("\n🎉 Training completed!")
    print(f"   Model saved to: runs/train/cow_behavior_optimized/weights/best.pt")
    print(f"   Copy this model to backend/ to use with vision server")
    
    return 0

if __name__ == "__main__":
    exit(main())
