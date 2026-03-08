#!/usr/bin/env python3
"""
Quick training script for Mac M4 Pro - uses existing synthetic data for fast demo.
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 Quick Training Demo - Mac M4 Pro Optimized")
    print("=" * 50)
    
    # Check if we have YOLO installed
    try:
        from ultralytics import YOLO
        print("✅ YOLO available")
    except ImportError:
        print("❌ YOLO not installed. Try: pip install ultralytics")
        return 1
    
    # Check device
    try:
        import torch
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        print(f"🍎 Using device: {device}")
    except:
        device = 'cpu'
        print("🖥️ Using CPU")
    
    # Use existing synthetic data (already available)
    dataset_path = "data/dataset.yaml"
    if not Path(dataset_path).exists():
        print("❌ Synthetic dataset not found")
        print("💡 Run: python data/generate_synthetic_dataset.py")
        return 1
    
    print(f"📊 Using dataset: {dataset_path}")
    
    # Initialize smallest model for speed
    model = YOLO('yolov8n.pt')
    
    # Quick training parameters
    print("🏃‍♂️ Starting quick training (5 epochs)...")
    
    try:
        results = model.train(
            data=dataset_path,
            epochs=5,           # Very few epochs for speed
            imgsz=320,          # Small images
            batch=4,             # Small batch
            device=device,
            optimizer='AdamW',
            lr0=0.001,
            patience=5,            # Early stopping
            save_period=1,        # Save frequently
            verbose=False,         # Less output
            plots=False,           # Skip plots for speed
            cache=False,           # Save memory
            workers=2,            # Fewer workers
            project='runs/train',
            name='quick_demo',
            exist_ok=True
        )
        
        print("✅ Training completed!")
        print(f"📦 Model saved to: runs/train/quick_demo/weights/best.pt")
        
        # Test quick inference
        print("🔍 Testing model...")
        test_results = model.val(data=dataset_path, device=device)
        print(f"📈 mAP@0.5: {test_results.box.map50:.3f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
