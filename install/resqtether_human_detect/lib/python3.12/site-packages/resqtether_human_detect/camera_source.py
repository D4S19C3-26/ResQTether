import cv2
import urllib.request
import numpy as np

class CameraSource:
    def __init__(self, source_type, **kwargs):
        self.source_type = source_type
        self.cap = None
        self.url = None
        
        if self.source_type == 'usb':
            index = kwargs.get('camera_index', 0)
            self.cap = cv2.VideoCapture(index)
            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open USB camera at index {index}")
                
        elif self.source_type == 'ip':
            self.url = kwargs.get('camera_url', 'http://192.168.1.100:8080/shot.jpg')
            
        elif self.source_type == 'csi':
            sensor_id = kwargs.get('sensor_id', 0)
            width = kwargs.get('width', 1920)
            height = kwargs.get('height', 1080)
            framerate = kwargs.get('framerate', 30)
            
            # GStreamer pipeline for IMX335 on Jetson
            pipeline = (
                f"nvarguscamerasrc sensor-id={sensor_id} ! "
                f"video/x-raw(memory:NVMM), width={width}, height={height}, format=(string)NV12, framerate={framerate}/1 ! "
                f"nvvidconv ! video/x-raw, format=(string)BGRx ! "
                f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
            )
            self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open CSI camera with pipeline: {pipeline}")
                
        else:
            raise ValueError(f"Unknown camera source type: {source_type}")

    def read(self):
        """Returns (success, BGR image array)"""
        if self.source_type == 'ip':
            try:
                req = urllib.request.urlopen(self.url, timeout=2.0)
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)
                if img is not None:
                    return True, img
                return False, None
            except Exception as e:
                print(f"IP Camera error: {e}")
                return False, None
        else:
            if self.cap is not None:
                return self.cap.read()
            return False, None

    def release(self):
        if self.cap is not None:
            self.cap.release()
