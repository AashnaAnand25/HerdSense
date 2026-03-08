#!/usr/bin/env python3
"""
Create a test video for lameness detection testing
"""

import cv2
import numpy as np

def create_test_video():
    """Create a synthetic test video with cow-like movement"""
    
    # Video settings
    width, height = 640, 480
    fps = 20
    duration = 5  # 5 seconds
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_lameness_video.mp4', fourcc, fps, (width, height))
    
    print(f"🎬 Creating test video: {total_frames} frames at {fps} FPS")
    
    for frame_num in range(total_frames):
        # Create frame with cow-like movement
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = [34, 139, 34]  # Green background
        
        # Add moving cow shape (simulating walking)
        x_pos = int(width * 0.3 + np.sin(frame_num * 0.1) * 100)
        y_pos = int(height * 0.5)
        
        # Draw cow body
        cv2.ellipse(frame, (x_pos, y_pos), (80, 50), 0, 0, 360, [50, 50, 50], -1)
        cv2.circle(frame, (x_pos, y_pos - 30), 20, [0, 0, 0], -1)  # Head
        
        # Add some texture
        noise = np.random.randint(0, 30, (height, width, 3))
        frame = frame + noise
        
        # Add timestamp
        cv2.putText(frame, f'Frame {frame_num}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        out.write(frame)
        
        if frame_num % 20 == 0:
            print(f"🎬 Processed {frame_num}/{total_frames} frames")
    
    out.release()
    print(f"✅ Test video created: test_lameness_video.mp4")
    print(f"📊 Duration: {duration}s, FPS: {fps}, Total frames: {total_frames}")
    
    return 'test_lameness_video.mp4'

if __name__ == "__main__":
    video_file = create_test_video()
    print(f"🎯 Ready to test: {video_file}")
    print("📋 Upload this video to test lameness detection!")
