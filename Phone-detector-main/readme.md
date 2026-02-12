#  AI Phone Detection & Alert System

This Python app uses YOLOv8 to detect mobile phones from a webcam feed and plays an alarm while a phone is visible.

##  Requirements
- Windows 10/11
- Python 3.8+ installed (https://www.python.org/downloads/)
- A working webcam

##  Project Files (Must Be Together)
Make sure these files are inside the same folder:
- `app.py`
- `yolov8n.pt`
- `audio.mp3`

##  First-Time Setup (On Any New PC)
Open PowerShell in the project folder and run:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install opencv-python ultralytics pygame
```

##  Run the App
From the same folder:

```bash
python app.py
```

Press `q` to quit.

##  Common Errors
**1) "No module named 'cv2'"**

Install dependencies again:

```bash
pip install opencv-python ultralytics pygame
```

**2) "audio.mp3 file nahi mili"**

Make sure `audio.mp3` is in the same folder as `app.py`.

**3) Webcam not opening**

Close other apps using the camera (Zoom, Teams, etc.) and run again.

##  Notes
- If you run from a parent folder, use:
  `python Phone-detector-main\app.py`
- The detection model file `yolov8n.pt` must stay in the same folder as `app.py`.
