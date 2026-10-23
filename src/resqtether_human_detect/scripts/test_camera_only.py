#!/usr/bin/env python3
import sys
import os
import cv2
import argparse
import urllib.request
import numpy as np
import time

def test_camera(source, url=None, index=0, sensor_id=0):
    cap = None
    if source == 'ip':
        print(f"Testing IP Camera at {url}")
    elif source == 'usb':
        print(f"Testing USB Camera (index {index})...")
        cap = cv2.VideoCapture(index)
    elif source == 'csi':
        pipeline = (
            f"nvarguscamerasrc sensor-id={sensor_id} ! "
            f"video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=30/1 ! "
            f"nvvidconv ! video/x-raw, format=(string)BGRx ! "
            f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
        )
        print(f"Testing CSI Camera with pipeline:\n{pipeline}")
        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    has_display = bool(os.environ.get("DISPLAY"))
    start_time = time.time()
    frames = 0
    last_print = time.time()
    
    try:
        while True:
            frame = None
            if source == 'ip':
                try:
                    req = urllib.request.urlopen(url, timeout=2.0)
                    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                    frame = cv2.imdecode(arr, -1)
                except Exception as e:
                    print(f"IP Camera error: {e}")
            else:
                if cap is not None and cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        print("Failed to read from camera")
                        break

            if frame is not None:
                frames += 1
                fps = frames / max(time.time() - start_time, 0.001)
                
                # Print terminal summary every second
                if time.time() - last_print >= 1.0:
                    h, w = frame.shape[:2]
                    print(f"✅ Camera Active: Resolution {w}x{h} | Captured {frames} frames | Speed: {fps:.1f} FPS")
                    last_print = time.time()

                if has_display:
                    try:
                        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow("Camera Test", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    except Exception:
                        has_display = False
                
    except KeyboardInterrupt:
        print("\nStopping camera test...")
    finally:
        if cap is not None:
            cap.release()
        if has_display:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Camera Access")
    parser.add_argument('--source', type=str, choices=['ip', 'usb', 'csi'], default='usb', help="Camera source type")
    parser.add_argument('--url', type=str, default='http://192.168.1.100:8080/shot.jpg', help="IP camera URL")
    parser.add_argument('--index', type=int, default=0, help="USB camera index")
    parser.add_argument('--camera-index', type=int, dest='index', help="Alias for --index")
    parser.add_argument('--sensor', type=int, default=0, help="CSI sensor ID")
    
    args = parser.parse_args()
    test_camera(args.source, args.url, args.index, args.sensor)
