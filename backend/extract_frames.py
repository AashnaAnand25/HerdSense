#!/usr/bin/env python3
"""
Extract frames from CBVD-5 videos efficiently for Mac M4 Pro.
Optimized to prevent overheating and handle large video files.
"""

import cv2
import os
from pathlib import Path
import pandas as pd
import subprocess
import time
from tqdm import tqdm
import psutil

class FrameExtractor:
    """Efficient frame extractor optimized for Mac M4 Pro"""
    
    def __init__(self):
        self.check_system_status()
        
    def check_system_status(self):
        """Check if system can handle video processing"""
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            print("⚠️ High memory usage detected")
            return False
        return True
    
    def get_video_list(self):
        """Get list of videos from CBVD-5 CSV"""
        csv_path = Path("data/archive/CBVD-5.csv")
        video_dir = Path("data/archive/videos/videos")
        
        if not csv_path.exists():
            print("❌ CBVD-5.csv not found")
            return []
        
        # Read CSV to get required frame names
        frame_names = set()
        try:
            with open(csv_path, 'r') as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    # Extract frame name from CSV
                    if '.jpg' in line:
                        start = line.find('"') + 1
                        end = line.find('.jpg"') + 4
                        if start > 0 and end > start:
                            frame_name = line[start:end]
                            frame_names.add(frame_name)
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return []
        
        print(f"📊 Found {len(frame_names)} unique frames needed")
        
        # Find corresponding videos
        videos = []
        for video_file in video_dir.glob('*.mp4'):
            videos.append(video_file)
        
        print(f"🎥 Found {len(videos)} videos")
        return videos
    
    def extract_frames_efficient(self, video_path, output_dir, max_frames=1000):
        """Extract frames efficiently with system monitoring"""
        
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return 0
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"🎥 Processing: {video_path.name}")
        print(f"   Duration: {duration:.1f}s, FPS: {fps:.1f}, Total frames: {total_frames}")
        
        # Calculate frame interval (extract every Nth frame)
        interval = max(1, total_frames // max_frames)
        
        frame_count = 0
        extracted_count = 0
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with tqdm(total=min(max_frames, total_frames), desc=f"Extracting {video_path.stem}") as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Extract every Nth frame
                if frame_count % interval == 0:
                    # Generate frame name to match CSV format
                    # CBVD-5 format: [video_id]_[frame_number].jpg
                    frame_name = f"{video_path.stem}_{frame_count:06d}.jpg"
                    frame_path = output_dir / frame_name
                    
                    # Save frame
                    cv2.imwrite(str(frame_path), frame)
                    extracted_count += 1
                    
                    # Check system status every 50 frames
                    if extracted_count % 50 == 0:
                        if not self.check_system_status():
                            print("⚠️ System stress detected - pausing extraction")
                            cap.release()
                            return extracted_count
                
                frame_count += 1
                pbar.update(1)
                
                # Stop if we've extracted enough frames
                if extracted_count >= max_frames:
                    break
        
        cap.release()
        print(f"✅ Extracted {extracted_count} frames from {video_path.name}")
        return extracted_count
    
    def extract_all_videos(self, frames_per_video=500):
        """Extract frames from all videos"""
        print("🚀 Starting frame extraction...")
        
        # Create output directory
        output_dir = Path("data/archive_frames")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        videos = self.get_video_list()
        if not videos:
            print("❌ No videos found")
            return 0
        
        total_extracted = 0
        
        # Process first few videos (to avoid overheating)
        max_videos = min(5, len(videos))  # Limit to prevent overheating
        
        for i, video in enumerate(videos[:max_videos]):
            print(f"\n📹 Video {i+1}/{max_videos}")
            
            # Extract frames
            extracted = self.extract_frames_efficient(
                video, 
                output_dir, 
                max_frames=frames_per_video
            )
            total_extracted += extracted
            
            # Cool down period between videos
            if i < max_videos - 1:
                print("😴 Cooling down for 30 seconds...")
                time.sleep(30)
        
        print(f"\n🎉 Total frames extracted: {total_extracted}")
        print(f"📁 Saved to: {output_dir}")
        
        return total_extracted

def main():
    """Main extraction pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract frames from CBVD-5 videos")
    parser.add_argument("--max-frames", type=int, default=500, help="Max frames per video")
    parser.add_argument("--max-videos", type=int, default=3, help="Max videos to process")
    args = parser.parse_args()
    
    print("🐄 CBVD-5 Frame Extractor - Mac M4 Pro Optimized")
    print("=" * 60)
    
    extractor = FrameExtractor()
    
    # Extract frames
    total_frames = extractor.extract_all_videos(frames_per_video=args.max_frames)
    
    if total_frames > 0:
        print("\n✅ Frame extraction completed!")
        print("🚀 Now you can run:")
        print("   python setup_training.py")
        print("   python train_optimized.py --epochs 30")
    else:
        print("\n❌ No frames extracted")

if __name__ == "__main__":
    exit(main())
