#!/usr/bin/env python3
import cv2
import argparse
import time

try:
    from ultralytics import YOLO
except ImportError:
    print("ultralytics is not installed. Please install it first.")
    exit(1)

def main():
    parser = argparse.ArgumentParser(description="Test YOLOv8 Detection on static image")
    parser.add_argument('--image', type=str, required=True, help="Path to input image")
    parser.add_argument('--model', type=str, default='yolov8n.pt', help="YOLO model path/name")
    args = parser.parse_args()

    print(f"Loading model {args.model}...")
    model = YOLO(args.model)
    
    print(f"Loading image {args.image}...")
    img = cv2.imread(args.image)
    if img is None:
        print(f"Could not read image: {args.image}")
        exit(1)

    print("Running inference...")
    start_time = time.time()
    results = model.predict(source=img, classes=[0], conf=0.5, verbose=False) # class 0 is person
    end_time = time.time()
    
    print(f"Inference took {(end_time - start_time)*1000:.2f} ms")
    
    annotated_img = img.copy()
    
    count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0].cpu().numpy())
            
            count += 1
            cv2.rectangle(annotated_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(annotated_img, f"Person {conf:.2f}", (int(x1), int(y1)-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
    print(f"Detected {count} persons.")
    
    cv2.imshow("Detection Result", annotated_img)
    print("Press any key to exit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
