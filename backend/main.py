from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import torch
from ultralytics import YOLO
import redis
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import base64
import io
from PIL import Image
from pydantic import BaseModel
import uuid

app = FastAPI(title="Herd Health AI - Computer Vision Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis client for real-time alerts
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
except:
    redis_client = None
    print("⚠️ Redis connection failed - alerts will be limited")

# Load YOLOv8 model with CBAM attention mechanism
try:
    model = YOLO('yolov8l.pt')  # Will be replaced with custom trained model
    print("✅ YOLOv8 model loaded successfully")
except Exception as e:
    print(f"⚠️ Model loading failed: {e}")
    model = None

class DetectionResult(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]
    timestamp: datetime

class HealthAlert(BaseModel):
    animal_id: str
    alert_type: str
    severity: str
    confidence: float
    timestamp: datetime
    description: str

class BehaviorAnalysis(BaseModel):
    behavior_type: str
    confidence: float
    duration: float
    animal_count: int
    health_indicators: Dict[str, float]

@app.on_event("startup")
async def startup_event():
    """Initialize the computer vision models and connections"""
    print("🤖 Herd Health AI CV Backend starting up...")
    
    # Load custom trained model if available
    try:
        custom_model = YOLO('models/cow_behavior_detector.pt')
        model = custom_model
        print("✅ Custom cow behavior model loaded")
    except:
        print("⚠️ Using default YOLOv8 model - custom model not found")
    
    # Test Redis connection
    try:
        redis_client.ping()
        print("✅ Redis connection established")
    except:
        print("⚠️ Redis connection failed - alerts will be limited")

@app.get("/")
async def root():
    return {"message": "Herd Health AI Computer Vision Backend", "status": "active"}

@app.post("/detect/lameness")
async def detect_lameness(file: UploadFile = File(...)):
    """
    Detect lameness in cows with confidence scoring
    """
    try:
        contents = await file.read()
        image_bytes = await file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        print(f"📊 Image bytes received: {len(image_bytes)}")
        
        # Handle OpenCV version compatibility
        try:
            # Try with flags first (newer versions)
            image = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
            print(f"✅ Image decoded with flags: {image.shape if image is not None else 'None'}")
        except Exception as primary_error:
            print(f"⚠️ Primary decode failed: {primary_error}")
            try:
                # Fallback without flags (older versions)
                image = cv2.imdecode(nparr)
                print(f"🔄 Fallback decode without flags: {image.shape if image is not None else 'None'}")
            except Exception as fallback_error:
                print(f"❌ All decode methods failed: {fallback_error}")
                raise HTTPException(status_code=500, detail=f"Image processing failed: {str(fallback_error)}")
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Run YOLO detection
        results = model(image)
        
        detections = []
        health_score = 100.0
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    # Map class to lameness detection
                    class_name = LAMENESS_CLASSES.get(cls, 'unknown')
                    
                    detection = DetectionResult(
                        class_name=class_name,
                        confidence=float(conf),
                        bbox=[float(x) for x in box.xyxy[0].cpu().numpy()],
                        timestamp=datetime.now()
                    )
                    detections.append(detection)
                    
                    # Adjust health score based on lameness
                    if 'lameness' in class_name.lower():
                        if 'severe' in class_name.lower():
                            health_score -= (conf * 30)
                        elif 'mild' in class_name.lower():
                            health_score -= (conf * 15)
        
        return {
            "detections": detections,
            "health_score": health_score,
            "total_animals": len(detections),
            "image_info": {
                "width": image.shape[1],
                "height": image.shape[0],
                "channels": image.shape[2] if len(image.shape) > 2 else 1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lameness detection failed: {str(e)}")

@app.post("/analyze/lameness")
async def analyze_lameness(file: UploadFile = File(...)):
    """
    Analyze lameness patterns for health monitoring
    """
    try:
        # Read and process image
        contents = await file.read()
        image_bytes = await file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Run YOLO detection
        results = model(image)
        
        behaviors = []
        health_score = 100.0
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    # Map class to lameness detection
                    class_name = LAMENESS_CLASSES.get(cls, 'unknown')
                    
                    # Analyze specific behaviors
                    behavior_analysis = analyze_specific_behavior(class_name, conf, image)
                    if behavior_analysis:
                        behaviors.append(behavior_analysis)
                        
                        # Adjust health score based on lameness
                        if 'lameness' in class_name.lower():
                            if 'severe' in class_name.lower():
                                health_score -= (conf * 30)
                            elif 'mild' in class_name.lower():
                                health_score -= (conf * 15)
        
        return {
            "behaviors": behaviors,
            "health_score": max(0, health_score),
            "total_animals": len(behaviors),
            "recommendations": generate_health_recommendations(behaviors, health_score)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lameness analysis failed: {str(e)}")

@app.post("/analyze/behavior")
async def analyze_behavior(file: UploadFile = File(...)):
    """
    Analyze cow behavior patterns for health monitoring
    Focuses on: eating, walking, lying down, social interactions, signs of distress
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Run behavior detection
        results = model(image)
        
        behaviors = []
        health_score = 100.0
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    class_name = LAMENESS_CLASSES.get(cls, 'unknown')
                    
                    # Analyze specific behaviors
                    behavior_analysis = analyze_specific_behavior(class_name, conf, image)
                    if behavior_analysis:
                        behaviors.append(behavior_analysis)
                        # Adjust health score based on behaviors
                        if "distress" in class_name.lower() or "abnormal" in class_name.lower():
                            health_score -= (conf * 20)
        
        return {
            "success": True,
            "behaviors": behaviors,
            "overall_health_score": max(0, health_score),
            "recommendations": generate_health_recommendations(behaviors),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavior analysis failed: {str(e)}")

@app.post("/piglet/birth-monitor")
async def piglet_birth_monitor(file: UploadFile = File(...)):
    """
    Monitor piglet births and detect falls/dangers
    Critical for preventing piglet mortality after birth
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Specialized detection for piglet birth scenarios
        results = model(image)
        
        piglets_detected = 0
        fall_dangers = []
        birth_alerts = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    class_name = LAMENESS_CLASSES.get(cls, 'unknown')
                    
                    if "piglet" in class_name.lower():
                        piglets_detected += 1
                        
                        # Check for fall dangers
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        danger = analyze_fall_danger([x1, y1, x2, y2], image, conf)
                        if danger:
                            fall_dangers.append(danger)
                    
                    elif "birth" in class_name.lower():
                        birth_alerts.append({
                            "alert_type": "birth_in_progress",
                            "confidence": float(conf),
                            "timestamp": datetime.now(),
                            "action_required": "Monitor for piglet falls"
                        })
        
        return {
            "success": True,
            "piglets_detected": piglets_detected,
            "fall_dangers": fall_dangers,
            "birth_alerts": birth_alerts,
            "critical_alerts": len(fall_dangers) > 0,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Piglet monitoring failed: {str(e)}")

@app.post("/vaccination/timing")
async def vaccination_timing_check(file: UploadFile = File(...)):
    """
    Analyze optimal vaccination timing based on animal behavior and health status
    """
    try:
        # Get current animal health data
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Analyze current health state
        behavior_results = await analyze_behavior(file)
        
        # Generate vaccination recommendations
        recommendations = generate_vaccination_recommendations(behavior_results)
        
        return {
            "success": True,
            "current_health_score": behavior_results["overall_health_score"],
            "vaccination_recommendations": recommendations,
            "optimal_timing": calculate_optimal_vaccination_time(behavior_results),
            "warnings": generate_vaccination_warnings(behavior_results),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vaccination analysis failed: {str(e)}")

@app.post("/compare/before-after")
async def compare_before_after(
    before_file: UploadFile = File(...),
    after_file: UploadFile = File(...)
):
    """
    Compare before and after footage to assess treatment effectiveness
    """
    try:
        # Process both images
        before_contents = await before_file.read()
        after_contents = await after_file.read()
        
        before_nparr = np.frombuffer(before_contents, np.uint8)
        after_nparr = np.frombuffer(after_contents, np.uint8)
        
        before_image = cv2.imdecode(before_nparr, cv2.IMREAD_COLOR)
        after_image = cv2.imdecode(after_nparr, cv2.IMREAD_COLOR)
        
        # Analyze both images
        before_results = model(before_image)
        after_results = model(after_image)
        
        # Compare metrics
        comparison = analyze_treatment_effectiveness(before_results, after_results)
        
        return {
            "success": True,
            "comparison": comparison,
            "improvement_score": comparison["improvement_percentage"],
            "recommendations": comparison["recommendations"],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@app.get("/alerts/active")
async def get_active_alerts():
    """Get all active health alerts from Redis"""
    try:
        alerts = []
        for key in redis_client.scan_iter("alert:*"):
            alert_data = redis_client.get(key)
            if alert_data:
                alerts.append(json.loads(alert_data))
        
        return {
            "success": True,
            "alerts": alerts,
            "total_count": len(alerts)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Helper functions
def analyze_cow_behavior(class_name: str, confidence: float, bbox: List[float], image: np.ndarray) -> Optional[HealthAlert]:
    """Analyze cow detection for health alerts"""
    if confidence < 0.7:
        return None
    
    # Check for various health indicators
    if "lying" in class_name.lower() and confidence > 0.8:
        return HealthAlert(
            animal_id=f"cow_{uuid.uuid4().hex[:8]}",
            alert_type="excessive_lying",
            severity="medium",
            confidence=confidence,
            timestamp=datetime.now(),
            description="Cow showing excessive lying behavior - possible health issue"
        )
    
    return None

def analyze_specific_behavior(class_name: str, confidence: float, image: np.ndarray) -> Optional[Dict]:
    """Analyze specific lameness behaviors for health monitoring"""
    behavior_analysis = {
        'behavior_type': class_name,
        'confidence': confidence,
        'timestamp': datetime.now().isoformat()
    }
    
    # Add lameness-specific analysis
    if 'lameness' in class_name.lower():
        if 'severe' in class_name.lower():
            behavior_analysis['severity'] = 'severe'
            behavior_analysis['recommendation'] = 'Immediate veterinary attention required'
            behavior_analysis['action'] = 'isolate_animal'
        elif 'mild' in class_name.lower():
            behavior_analysis['severity'] = 'mild'
            behavior_analysis['recommendation'] = 'Schedule veterinary examination within 1-2 weeks'
            behavior_analysis['action'] = 'increase_monitoring'
    
    elif class_name == 'cow_normal_walking':
        behavior_analysis['severity'] = 'normal'
        behavior_analysis['recommendation'] = 'Continue regular monitoring'
        behavior_analysis['action'] = 'maintain_current_regimen'
    
    elif class_name == 'cow_lying_down':
        behavior_analysis['severity'] = 'normal'
        behavior_analysis['recommendation'] = 'Monitor duration and position'
        behavior_analysis['action'] = 'check_for_other_behaviors'
    
    elif class_name == 'cow_standing':
        behavior_analysis['severity'] = 'normal'
        behavior_analysis['recommendation'] = 'Normal standing behavior'
        behavior_analysis['action'] = 'continue_monitoring'
    
    elif class_name == 'cow_eating':
        behavior_analysis['severity'] = 'normal'
        behavior_analysis['recommendation'] = 'Good appetite and health indicators'
        behavior_analysis['action'] = 'continue_monitoring'
    
    return behavior_analysis

def analyze_fall_danger(bbox: List[float], image: np.ndarray, confidence: float) -> Optional[Dict]:
    """Analyze piglet fall dangers"""
    x1, y1, x2, y2 = bbox
    height = y2 - y1
    width = x2 - x1
    
    # Check if piglet is near edge or dangerous area
    image_height, image_width = image.shape[:2]
    
    if y1 < 50 or y2 > image_height - 50:  # Near top/bottom edge
        return {
            "danger_type": "fall_risk",
            "confidence": confidence,
            "location": bbox,
            "severity": "high",
            "action": "Immediate intervention required"
        }
    
    return None

LAMENESS_CLASSES = {
    0: 'cow_normal_walking',
    1: 'cow_lameness_mild',
    2: 'cow_lameness_severe', 
    3: 'cow_lying_down',
    4: 'cow_standing',
    5: 'cow_eating'
}

HEALTH_RECOMMENDATIONS = {
    'cow_normal_walking': {
        'status': 'healthy',
        'priority': 'low',
        'action': 'Continue monitoring',
        'recommendation': 'Normal walking pattern detected. Continue regular health monitoring.'
    },
    'cow_lameness_mild': {
        'status': 'attention',
        'priority': 'medium',
        'action': 'Schedule veterinary check',
        'recommendation': 'Mild lameness detected. Consider scheduling a veterinary examination within 1-2 weeks.'
    },
    'cow_lameness_severe': {
        'status': 'critical',
        'priority': 'high',
        'action': 'Immediate veterinary attention',
        'recommendation': 'Severe lameness detected! Immediate veterinary attention required. Isolate from herd if possible.'
    },
    'cow_lying_down': {
        'status': 'normal',
        'priority': 'low',
        'action': 'Monitor duration',
        'recommendation': 'Cow is lying down. Monitor duration and contact with other behaviors.'
    },
    'cow_standing': {
        'status': 'normal',
        'priority': 'low',
        'action': 'Continue monitoring',
        'recommendation': 'Normal standing behavior. Continue regular monitoring.'
    },
    'cow_eating': {
        'status': 'normal',
        'priority': 'low',
        'action': 'Continue monitoring',
        'recommendation': 'Normal eating behavior detected. Good appetite and health indicators.'
    }
}

def generate_health_recommendations(behaviors: List[BehaviorAnalysis]) -> List[str]:
    """Generate health recommendations based on behavior analysis"""
    recommendations = []
    
    for behavior in behaviors:
        if "distress" in behavior.behavior_type:
            recommendations.append("Immediate veterinary examination recommended")
        elif behavior.confidence < 0.5:
            recommendations.append("Monitor animal closely for changes")
    
    if not recommendations:
        recommendations.append("All behaviors appear normal - continue regular monitoring")
    
    return recommendations

def generate_vaccination_recommendations(behavior_results: Dict) -> Dict:
    """Generate vaccination timing recommendations"""
    health_score = behavior_results.get("overall_health_score", 100)
    
    if health_score > 80:
        return {
            "recommendation": "Optimal timing for vaccination",
            "confidence": 0.9,
            "reason": "Animal shows good health indicators"
        }
    elif health_score > 60:
        return {
            "recommendation": "Proceed with vaccination but monitor closely",
            "confidence": 0.7,
            "reason": "Animal health is acceptable but requires monitoring"
        }
    else:
        return {
            "recommendation": "Delay vaccination until health improves",
            "confidence": 0.8,
            "reason": "Animal shows signs of stress or illness"
        }

def calculate_optimal_vaccination_time(behavior_results: Dict) -> str:
    """Calculate optimal vaccination time based on behavior analysis"""
    health_score = behavior_results.get("overall_health_score", 100)
    
    if health_score > 85:
        return "Immediate (within 24 hours)"
    elif health_score > 70:
        return "Within 2-3 days"
    else:
        return "Wait until health improves"

def generate_vaccination_warnings(behavior_results: Dict) -> List[str]:
    """Generate warnings for vaccination timing"""
    warnings = []
    health_score = behavior_results.get("overall_health_score", 100)
    
    if health_score < 60:
        warnings.append("Animal shows signs of stress - vaccination may be risky")
    
    for behavior in behavior_results.get("behaviors", []):
        if "distress" in behavior.behavior_type and behavior.confidence > 0.7:
            warnings.append("High distress detected - postpone vaccination")
    
    return warnings

def analyze_treatment_effectiveness(before_results, after_results) -> Dict:
    """Compare before and after treatment results"""
    # Simplified comparison - would be more sophisticated in production
    before_detections = len(before_results[0].boxes) if before_results[0].boxes else 0
    after_detections = len(after_results[0].boxes) if after_results[0].boxes else 0
    
    improvement_percentage = ((after_detections - before_detections) / max(before_detections, 1)) * 100
    
    return {
        "before_treatment": {
            "detections": before_detections,
            "health_indicators": "baseline"
        },
        "after_treatment": {
            "detections": after_detections,
            "health_indicators": "improved" if improvement_percentage > 0 else "stable"
        },
        "improvement_percentage": improvement_percentage,
        "recommendations": [
            "Continue monitoring" if improvement_percentage > 0 else "Reassess treatment plan"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Find available port
    port = 8001  # Start with different port
    
    print(f"🚀 Starting Herd Health AI Backend on port {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
