"""
Camera Manager for fetching and processing camera feeds
"""

import cv2
import numpy as np
import aiohttp
import asyncio
from typing import Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CameraManager:
    """Manages camera feeds and monitoring"""
    
    def __init__(self):
        self.monitoring_tasks: Dict[int, asyncio.Task] = {}
        self.camera_urls: Dict[int, str] = {}
    
    async def fetch_image(self, camera_url: str) -> Optional[np.ndarray]:
        """
        Fetch image from camera URL
        
        Args:
            camera_url: URL of the camera feed
            
        Returns:
            Image as numpy array or None if failed
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(camera_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        image_bytes = await response.read()
                        nparr = np.frombuffer(image_bytes, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        return img
                    else:
                        logger.error(f"Failed to fetch image: HTTP {response.status}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching image from {camera_url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching image: {e}")
            return None
    
    async def start_monitoring(
        self,
        parking_lot_id: int,
        camera_url: str,
        detector
    ):
        """
        Start continuous monitoring of a parking lot
        
        Args:
            parking_lot_id: ID of the parking lot
            camera_url: URL of the camera feed
            detector: ParkingSlotDetector instance
        """
        if parking_lot_id in self.monitoring_tasks:
            # Stop existing monitoring
            await self.stop_monitoring(parking_lot_id)
        
        self.camera_urls[parking_lot_id] = camera_url
        
        # Create monitoring task
        task = asyncio.create_task(
            self._monitor_loop(parking_lot_id, camera_url, detector)
        )
        self.monitoring_tasks[parking_lot_id] = task
        
        logger.info(f"Started monitoring parking lot {parking_lot_id}")
    
    async def stop_monitoring(self, parking_lot_id: int):
        """Stop monitoring a parking lot"""
        if parking_lot_id in self.monitoring_tasks:
            task = self.monitoring_tasks[parking_lot_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.monitoring_tasks[parking_lot_id]
            del self.camera_urls[parking_lot_id]
            logger.info(f"Stopped monitoring parking lot {parking_lot_id}")
    
    async def _monitor_loop(
        self,
        parking_lot_id: int,
        camera_url: str,
        detector,
        interval: int = 30
    ):
        """
        Monitoring loop that periodically detects parking slots
        
        Args:
            parking_lot_id: ID of the parking lot
            camera_url: URL of the camera feed
            detector: ParkingSlotDetector instance
            interval: Detection interval in seconds
        """
        while True:
            try:
                # Fetch image
                img = await self.fetch_image(camera_url)
                
                if img is not None:
                    # Detect slots
                    results = await detector.detect_slots(img, parking_lot_id)
                    
                    # Store results (would update backend/Redis here)
                    logger.info(
                        f"Parking lot {parking_lot_id}: "
                        f"{results.get('available_slots', 0)}/{results.get('total_slots', 0)} slots available"
                    )
                else:
                    logger.warning(f"Failed to fetch image for parking lot {parking_lot_id}")
                
                # Wait before next detection
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                logger.info(f"Monitoring cancelled for parking lot {parking_lot_id}")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(interval)

