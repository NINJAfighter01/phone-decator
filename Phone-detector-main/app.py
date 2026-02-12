import cv2
from ultralytics import YOLO
import pygame
import time
import os

# --- CONFIGURATION ---
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE = os.path.join(SCRIPT_DIR, "audio.mp3")
CONFIDENCE_LEVEL = 0.3    # Lower confidence for better detection
FRAME_SKIP = 2  # Har 2nd frame check karega
DETECTION_TIMEOUT = 2.0  # 2 seconds tak phone nahi dikhe to hi stop kare
# ---------------------

if not os.path.exists(AUDIO_FILE):
    print(f"ERROR: '{AUDIO_FILE}' file nahi mili!")
    exit()

# Audio pehle hi load kar lo (Loop ke bahar) - Ye fast karega
pygame.mixer.init()
try:
    pygame.mixer.music.load(AUDIO_FILE)
    print(f"✓ Audio loaded successfully: {AUDIO_FILE}")
except Exception as e:
    print(f"Audio Error: {e}")

print("Loading Fast AI Model...")
model = YOLO(os.path.join(SCRIPT_DIR, 'yolov8n.pt'))

cap = cv2.VideoCapture(0)

# Resolution High rakhna hai
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

frame_count = 0
last_phone_seen_time = 0  # Jab last time phone dikha tha
phone_currently_visible = False  # Abhi phone visible hai ya nahi
boxes_to_draw = [] # Boxes save karne ke liye

print("System Ready. Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1

    # --- SPEED TRICK: FRAME SKIPPING ---
    # Sirf har 'FRAME_SKIP' frame par hi AI run karega
    # Baaki time purana result dikhayega (Video smooth rahegi)
    if frame_count % FRAME_SKIP == 0:
        # imgsz=640 se processing fast hogi bhale hi camera 1024 ho
        results = model(frame, stream=True, verbose=False, conf=CONFIDENCE_LEVEL, imgsz=640)
        
        phone_detected_now = False
        boxes_to_draw = [] # List clear karo

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                confidence = float(box.conf[0])
                
                # Debug: Print all detections
                if frame_count % 30 == 0:  # Print every 30 frames
                    print(f"Detected: {class_name} (confidence: {confidence:.2f})")

                if class_name == 'cell phone':
                    phone_detected_now = True
                    last_phone_seen_time = time.time()  # Update last seen time
                    print(f"📱 PHONE DETECTED! Confidence: {confidence:.2f}")
                    # Coordinates save kar lo draw karne ke liye
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    boxes_to_draw.append((x1, y1, x2, y2))
        
        # Update visibility status based on timeout
        current_time = time.time()
        if phone_detected_now:
            phone_currently_visible = True
        elif current_time - last_phone_seen_time > DETECTION_TIMEOUT:
            # Phone DETECTION_TIMEOUT seconds se nahi dikha
            phone_currently_visible = False
    
    # --- DRAWING (Har frame pe draw karo taaki flicker na ho) ---
    if phone_currently_visible:
        for (x1, y1, x2, y2) in boxes_to_draw:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, "PHONE RAKHHHH NEECHE!", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Audio Logic - Jab tak phone visible hai, sound play hota rahe
        # Agar sound currently nahi chal raha (get_busy() = False), to play karo
        if not pygame.mixer.music.get_busy():
            print("🔊 >>> Playing Sound (Phone Visible)...")
            try:
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Sound play error: {e}")
    else:
        # Agar phone timeout se zyada time se nahi dikha to sound stop kar do
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("✓ Phone removed, sound stopped.")

    cv2.imshow('No Phone Zone', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()