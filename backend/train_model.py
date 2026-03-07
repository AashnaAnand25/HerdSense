import torch
import torch.nn as nn
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import yaml
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score
import pandas as pd
from tqdm import tqdm
import os

class CBAM(nn.Module):
    """Convolutional Block Attention Module"""
    def __init__(self, channels, reduction=16):
        super(CBAM, self).__init__()
        self.channel_attention = ChannelAttention(channels, reduction)
        self.spatial_attention = SpatialAttention()

    def forward(self, x):
        x = self.channel_attention(x) * x
        x = self.spatial_attention(x) * x
        return x

class ChannelAttention(nn.Module):
    def __init__(self, channels, reduction=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Conv2d(channels, channels // reduction, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(channels // reduction, channels, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = avg_out + max_out
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size//2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv(x)
        return self.sigmoid(x)

class CowBehaviorTrainer:
    """Specialized trainer for cow behavior detection using CBVD dataset"""
    
    def __init__(self, dataset_path: str, model_size: str = "l"):
        self.dataset_path = Path(dataset_path)
        self.model_size = model_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize YOLOv8 model
        self.model = YOLO(f'yolov8{model_size}.pt')
        
        # Custom class names for cow behaviors
        self.class_names = [
            'cow_eating', 'cow_walking', 'cow_lying_down', 'cow_standing',
            'cow_socializing', 'cow_distress', 'cow_abnormal_movement',
            'piglet_nursing', 'piglet_fall_risk', 'birth_in_progress'
        ]
        
    def prepare_dataset(self, kaggle_dataset_path: str):
        """Prepare CBVD dataset for training"""
        print("📊 Preparing CBVD dataset...")
        
        # Create dataset structure
        dataset_dir = self.dataset_path / "cow_behavior_dataset"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # Create train/val/test splits (70/15/15)
        splits = {
            'train': 0.7,
            'val': 0.15,
            'test': 0.15
        }
        
        # Process videos and extract frames
        self._extract_frames_from_videos(kaggle_dataset_path, dataset_dir, splits)
        
        # Create YOLO dataset.yaml
        dataset_config = {
            'path': str(dataset_dir),
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'nc': len(self.class_names),
            'names': self.class_names
        }
        
        with open(dataset_dir / 'dataset.yaml', 'w') as f:
            yaml.dump(dataset_config, f)
        
        print(f"✅ Dataset prepared at {dataset_dir}")
        return dataset_dir / 'dataset.yaml'
    
    def _extract_frames_from_videos(self, video_path: str, output_dir: Path, splits: Dict):
        """Extract frames from CBVD videos and create annotations"""
        video_dir = Path(video_path)
        
        # Create output directories
        for split in splits.keys():
            (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
            (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)
        
        # Process each video file
        video_files = list(video_dir.glob('*.mp4')) + list(video_dir.glob('*.avi'))
        
        for video_file in tqdm(video_files, desc="Processing videos"):
            cap = cv2.VideoCapture(str(video_file))
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Extract every 30th frame (adjust as needed)
                if frame_count % 30 == 0:
                    # Determine split
                    rand = np.random.random()
                    if rand < splits['train']:
                        split = 'train'
                    elif rand < splits['train'] + splits['val']:
                        split = 'val'
                    else:
                        split = 'test'
                    
                    # Save frame
                    frame_filename = f"{video_file.stem}_frame_{frame_count}.jpg"
                    frame_path = output_dir / 'images' / split / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    
                    # Create label file (would need manual annotation or automated labeling)
                    label_path = output_dir / 'labels' / split / f"{frame_filename}.txt"
                    self._create_annotation(frame_path, label_path, frame)
                
                frame_count += 1
            
            cap.release()
    
    def _create_annotation(self, frame_path: Path, label_path: Path, frame: np.ndarray):
        """Create YOLO format annotations (simplified - would need proper labeling)"""
        # This is a placeholder - in reality, you'd need proper annotations
        # For demonstration, creating empty label files
        label_path.touch()
    
    def add_cbam_to_model(self):
        """Add CBAM attention mechanism to YOLOv8 model"""
        print("🔧 Adding CBAM attention mechanism...")
        
        # This would require modifying the YOLOv8 architecture
        # For now, we'll use the standard model and fine-tune it
        print("📝 Note: CBAM integration requires custom model architecture")
        print("🔄 Using standard YOLOv8 with fine-tuning for cow behaviors")
    
    def train_model(self, dataset_yaml: str, epochs: int = 100):
        """Train the cow behavior detection model"""
        print(f"🚀 Starting training for {epochs} epochs...")
        
        # Training parameters optimized for livestock detection
        training_args = {
            'data': dataset_yaml,
            'epochs': epochs,
            'imgsz': 640,
            'batch': 16,
            'optimizer': 'SGD',  # Better generalization as per research
            'lr0': 0.01,
            'lrf': 0.001,
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 3,
            'warmup_momentum': 0.8,
            'warmup_bias_lr': 0.1,
            'box': 0.05,
            'cls': 0.5,
            'cls_pw': 1.0,
            'obj': 1.0,
            'obj_pw': 1.0,
            'iou_t': 0.2,
            'anchor_t': 4.0,
            'fl_gamma': 0.0,
            'hsv_h': 0.015,
            'hsv_s': 0.7,
            'hsv_v': 0.4,
            'degrees': 0.0,
            'translate': 0.1,
            'scale': 0.5,
            'shear': 0.0,
            'perspective': 0.0,
            'flipud': 0.0,
            'fliplr': 0.5,
            'mosaic': 1.0,
            'mixup': 0.0,
            'copy_paste': 0.0,
            'device': str(self.device),
            'project': 'runs/train',
            'name': 'cow_behavior_detector',
            'exist_ok': True,
            'pretrained': True,
            'resume': False,
            'int8': False,
            'single_cls': False,
            'rect': False,
            'cos_lr': False,
            'close_mosaic': 10,
            'patience': 50,
            'save': True,
            'save_json': True,
            'save_hybrid': False,
            'conf': None,
            'iou': 0.7,
            'max_det': 1000,
            'plots': True,
            'source': None,
            'vid_stride': 1,
            'stream_buffer': False,
            'line_width': 3,
            'visualize': False,
            'augment': False,
            'agnostic_nms': False,
            'classes': None,
            'retina_masks': False,
            'embed': None,
            'show': False,
            'save_frames': False,
            'save_txt': True,
            'save_conf': False,
            'save_crop': False,
            'show_labels': True,
            'show_conf': True,
            'show_boxes': True,
            'color_threshold': 0.25,
            'max_det_threshold': 0.5,
            'vid_stride': 1,
            'line_thickness': 3,
            'font_size': None,
            'font': 'Arial.ttf',
            'text_color': 'white',
            'text_background_color': 'black',
            'text_alpha': 0.7,
            'text_thickness': 2,
            'text_padding': 2,
            'fps': 30,
            'width': None,
            'height': None,
            'fourcc': 'mp4v',
            'count': None,
            'hide_labels': False,
            'hide_conf': False,
            'half': False,
            'dnn': False,
        }
        
        # Start training
        results = self.model.train(**training_args)
        
        print("✅ Training completed!")
        return results
    
    def evaluate_model(self, test_images_path: str) -> Dict:
        """Evaluate model performance with mAP, precision, recall"""
        print("📊 Evaluating model performance...")
        
        # Run validation on test set
        results = self.model.val(data=test_images_path, split='test')
        
        # Extract metrics
        metrics = {
            'precision': results.results_dict['metrics/precision(B)'],
            'recall': results.results_dict['metrics/recall(B)'],
            'mAP50': results.results_dict['metrics/mAP50(B)'],
            'mAP50_95': results.results_dict['metrics/mAP50-95(B)'],
            'inference_time': results.speed['inference']
        }
        
        print(f"📈 Model Performance:")
        print(f"   Precision: {metrics['precision']:.3f}")
        print(f"   Recall: {metrics['recall']:.3f}")
        print(f"   mAP@0.5: {metrics['mAP50']:.3f}")
        print(f"   mAP@0.5:0.95: {metrics['mAP50_95']:.3f}")
        print(f"   Inference Time: {metrics['inference_time']:.2f}ms")
        
        return metrics
    
    def export_model(self, format: str = 'pt'):
        """Export trained model for deployment"""
        print(f"📦 Exporting model in {format} format...")
        
        # Export model
        exported_path = self.model.export(format=format, imgsz=640)
        
        print(f"✅ Model exported to {exported_path}")
        return exported_path
    
    def run_inference(self, image_path: str) -> Dict:
        """Run inference on a single image"""
        results = self.model(image_path)
        
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for i, box in enumerate(boxes):
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    detections.append({
                        'class': self.class_names[cls],
                        'confidence': float(conf),
                        'bbox': [float(x1), float(y1), float(x2), float(y2)]
                    })
        
        return {
            'detections': detections,
            'total_objects': len(detections),
            'image_path': image_path
        }

def main():
    """Main training pipeline"""
    # Initialize trainer
    trainer = CowBehaviorTrainer('./data', model_size='l')
    
    # Download and prepare dataset (would need Kaggle API)
    kaggle_dataset = './datasets/cbvd-cow-behavior-video-dataset'
    
    if not os.path.exists(kaggle_dataset):
        print("⚠️ Please download the CBVD dataset from Kaggle:")
        print("https://www.kaggle.com/datasets/fandaoerji/cbvd-5cow-behavior-video-dataset")
        print("And extract it to ./datasets/cbvd-cow-behavior-video-dataset")
        return
    
    # Prepare dataset
    dataset_yaml = trainer.prepare_dataset(kaggle_dataset)
    
    # Add CBAM attention
    trainer.add_cbam_to_model()
    
    # Train model
    training_results = trainer.train_model(dataset_yaml, epochs=100)
    
    # Evaluate model
    metrics = trainer.evaluate_model(dataset_yaml)
    
    # Export model
    trainer.export_model('pt')  # PyTorch format
    trainer.export_model('onnx')  # ONNX for faster inference
    
    print("🎉 Training pipeline completed!")
    print(f"Final model saved with mAP@0.5:0.95: {metrics['mAP50_95']:.3f}")

if __name__ == "__main__":
    main()
