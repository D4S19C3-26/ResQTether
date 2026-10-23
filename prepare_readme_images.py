#!/usr/bin/env python3
import os
import cv2
import numpy as np

out_dir = '/home/dsc/resqtether_ws/docs/images'
os.makedirs(out_dir, exist_ok=True)

# 1. Rover Hardware Photo (No face to blur)
bot_src = '/home/dsc/.gemini/antigravity/brain/2225ba08-dc5a-4058-95dc-2730dec081d6/.user_uploaded/media_1792747865715.png'
if os.path.exists(bot_src):
    img = cv2.imread(bot_src)
    if img is not None:
        cv2.imwrite(os.path.join(out_dir, 'rover_hardware.png'), img)
        print("✅ Saved rover_hardware.png")

# Helper function to detect & heavily blur any face
def process_and_blur(src_file, dst_name, manual_face_box=None):
    if not os.path.exists(src_file):
        print(f"File {src_file} does not exist")
        return
    img = cv2.imread(src_file)
    if img is None:
        return

    # Haar face detector
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=3, minSize=(25, 25))

    for (fx, fy, fw, fh) in faces:
        pad = int(fw * 0.25)
        y1 = max(0, fy - pad)
        y2 = min(img.shape[0], fy + fh + pad)
        x1 = max(0, fx - pad)
        x2 = min(img.shape[1], fx + fw + pad)
        # Apply heavy Gaussian blur + pixelation
        sub = img[y1:y2, x1:x2]
        small = cv2.resize(sub, (8, 8), interpolation=cv2.INTER_LINEAR)
        blurred = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        img[y1:y2, x1:x2] = blurred

    # Also apply manual face box fallback if specified (for camera feed inset)
    if manual_face_box is not None:
        for (x1, y1, x2, y2) in manual_face_box:
            sub = img[y1:y2, x1:x2]
            small = cv2.resize(sub, (8, 8), interpolation=cv2.INTER_LINEAR)
            blurred = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
            img[y1:y2, x1:x2] = blurred

    out_path = os.path.join(out_dir, dst_name)
    cv2.imwrite(out_path, img)
    print(f"✅ Saved blurred image: {out_path}")

# Process the 4 screenshots:
# 1. Victim Localization with 3D Pin & Camera feed (media_1792747788050.png)
process_and_blur(
    '/home/dsc/.gemini/antigravity/brain/2225ba08-dc5a-4058-95dc-2730dec081d6/.user_uploaded/media_1792747788050.png',
    'victim_localization_rviz.png',
    manual_face_box=[(80, 205, 160, 310)]
)

# 2. Live Dark Mode RSSI Telemetry (media_1792747805508.png)
process_and_blur(
    '/home/dsc/.gemini/antigravity/brain/2225ba08-dc5a-4058-95dc-2730dec081d6/.user_uploaded/media_1792747805508.png',
    'live_rssi_telemetry.png',
    manual_face_box=[(80, 205, 140, 310)]
)

# 3. Terminal confirmation alert (media_1792747818855.png)
process_and_blur(
    '/home/dsc/.gemini/antigravity/brain/2225ba08-dc5a-4058-95dc-2730dec081d6/.user_uploaded/media_1792747818855.png',
    'terminal_victim_confirmed.png'
)

# 4. Multi-Human Detection SLAM view (media_1792747831209.png)
process_and_blur(
    '/home/dsc/.gemini/antigravity/brain/2225ba08-dc5a-4058-95dc-2730dec081d6/.user_uploaded/media_1792747831209.png',
    'multihuman_slam_mapping.png',
    manual_face_box=[(80, 240, 140, 315), (130, 220, 175, 290)]
)

print("All images processed and saved to docs/images!")
