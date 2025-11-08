"""
Parking Slot Detector using YOLOv8
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import asyncio
from datetime import datetime

# Optional imports - AI dependencies
try:
    from ultralytics import YOLO
    import torch
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    YOLO = None


class ParkingSlotDetector:
    """AI-powered parking slot detector"""
    
    def __init__(self):
        self.model: Optional[YOLO] = None
        self.model_loaded = False
        self.model_path = Path("models/parking_slot_detector.pt")
        self.confidence_threshold = 0.5
        
    async def load_model(self):
        """Load YOLOv8 model for parking slot detection"""
        if not AI_AVAILABLE:
            print("⚠️  AI dependencies not installed. Install with: pip install ultralytics torch")
            print("⚠️  AI features will be disabled")
            self.model_loaded = False
            return
        
        try:
            # Try to load custom trained model
            if self.model_path.exists():
                self.model = YOLO(str(self.model_path))
                print(f"✅ Loaded custom model from {self.model_path}")
            else:
                # Use pre-trained YOLOv8 model as fallback
                # In production, you'd train a custom model for parking slots
                self.model = YOLO("yolov8n.pt")  # nano version for speed
                print("⚠️  Using pre-trained YOLOv8 model (custom model not found)")
                print("💡 Train a custom model for better parking slot detection")
            
            self.model_loaded = True
            print("✅ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model_loaded = False
            raise
    
    async def detect_slots(self, image: np.ndarray, parking_lot_id: int) -> Dict:
        """
        Detect parking slots in an image
        
        Args:
            image: Input image (BGR format)
            parking_lot_id: ID of the parking lot
            
        Returns:
            Dictionary with detection results
        """
        if not AI_AVAILABLE:
            return {
                "parking_lot_id": parking_lot_id,
                "timestamp": datetime.now().isoformat(),
                "error": "AI dependencies not installed. Install with: pip install ultralytics torch",
                "total_slots": 0,
                "available_slots": 0,
                "occupied_slots": 0
            }
        
        if not self.model_loaded:
            await self.load_model()
        
        if not self.model_loaded:
            return {
                "parking_lot_id": parking_lot_id,
                "timestamp": datetime.now().isoformat(),
                "error": "Model not loaded",
                "total_slots": 0,
                "available_slots": 0,
                "occupied_slots": 0
            }
        
        try:
            # Run detection
            results = self.model(image, conf=self.confidence_threshold)
            
            # Process results
            detections = []
            available_slots = 0
            occupied_slots = 0
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.model.names[class_id]
                    
                    # Filter for vehicles (car, truck, bus, motorcycle)
                    vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'van']
                    if class_name.lower() in vehicle_classes:
                        occupied_slots += 1
                        detections.append({
                            "bbox": [float(x1), float(y1), float(x2), float(y2)],
                            "confidence": confidence,
                            "class": class_name,
                            "status": "occupied"
                        })
            
            # Calculate available slots
            # In a real implementation, you'd have predefined slot regions
            # For now, we estimate based on parking lot size
            total_slots = self._estimate_total_slots(image, occupied_slots)
            available_slots = max(0, total_slots - occupied_slots)
            
            return {
                "parking_lot_id": parking_lot_id,
                "timestamp": datetime.now().isoformat(),
                "total_slots": total_slots,
                "available_slots": available_slots,
                "occupied_slots": occupied_slots,
                "occupancy_rate": occupied_slots / total_slots if total_slots > 0 else 0,
                "detections": detections,
                "image_shape": list(image.shape)
            }
            
        except Exception as e:
            print(f"Detection error: {e}")
            return {
                "parking_lot_id": parking_lot_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "total_slots": 0,
                "available_slots": 0,
                "occupied_slots": 0
            }
    
    def _estimate_total_slots(self, image: np.ndarray, occupied_count: int) -> int:
        """
        Estimate total parking slots based on image analysis
        In production, this would use predefined slot regions
        """
        # Simple heuristic: estimate based on image size and occupied vehicles
        height, width = image.shape[:2]
        
        # Rough estimation: assume each vehicle takes ~50x100 pixels
        # and parking spaces are ~60x120 pixels
        vehicle_area = 50 * 100
        slot_area = 60 * 120
        
        # Estimate based on image area
        image_area = height * width
        estimated_slots = int((image_area * 0.3) / slot_area)  # Assume 30% of image is parking
        
        # Ensure we have at least as many slots as occupied vehicles
        return max(occupied_count, estimated_slots)
    
    async def analyze_safety(self, parking_lot_id: int) -> float:
        """
        Analyze safety score for a parking lot based on AI detection
        
        Returns:
            Safety score from 0.0 to 5.0
        """
        # This would analyze various factors:
        # - Lighting conditions
        # - Security camera coverage
        # - Obstruction visibility
        # - Emergency access
        # For now, return a placeholder score
        
        # In production, this would:
        # 1. Analyze recent camera feeds
        # 2. Detect lighting conditions
        # 3. Check for security features
        # 4. Analyze user feedback patterns
        
        base_score = 4.0  # Base safety score
        
        # Add some variation based on parking lot ID (placeholder)
        variation = (parking_lot_id % 10) / 10.0
        score = base_score + variation
        
        return min(5.0, max(0.0, score))
    
    def draw_detections(self, image: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Draw detection boxes on image for visualization
        """
        result_image = image.copy()
        
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            confidence = detection["confidence"]
            class_name = detection["class"]
            status = detection["status"]
            
            # Draw bounding box
            color = (0, 0, 255) if status == "occupied" else (0, 255, 0)
            cv2.rectangle(result_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            
            # Draw label
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(
                result_image,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        
        return result_image

