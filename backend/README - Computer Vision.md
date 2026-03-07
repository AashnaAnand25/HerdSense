# Computer Vision Backend for Herd Health AI

## Overview
This Python backend provides computer vision capabilities for livestock health monitoring using state-of-the-art deep learning models.

## Features
- Real-time cow behavior detection using YOLOv8-CBAM
- Before/after footage comparison
- Piglet birth monitoring and fall detection
- Vaccination timing warnings
- Health alert system with confidence scoring
- Support for CBVD cow behavior dataset

## Recommended Models (Based on Research)
1. **YOLOv8l-CBAM** - Best overall performance (95.2% precision, 82.6% mAP@0.5:0.95)
2. **YOLOv8x** - Highest accuracy (96.0% mAP@0.5, 81.0% mAP@0.95) 
3. **Mask R-CNN** - For instance segmentation tasks
4. **EfficientNet** - For classification of specific behaviors

## Architecture
- FastAPI backend for real-time inference
- PyTorch/Ultralytics for model training
- OpenCV for video processing
- Redis for real-time alerts
- PostgreSQL for historical data

## Dataset Integration
- CBVD Cow Behavior Video Dataset from Kaggle
- Custom data augmentation for farm environments
- Train/test/val split (70/15/15)

## Performance Metrics
- Precision, Recall, F1-score
- mAP@0.5 and mAP@0.5:0.95
- Inference time (target: <2ms per frame)
- Confidence scoring system

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
