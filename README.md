# Fire & Smoke Detection System 🔥🚨

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-orange)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A real-time fire and smoke detection system with GUI alerts, powered by YOLO object detection.

## Features ✨

- Real-time fire/smoke detection with YOLOv8
- Interactive PyQt5 interface with dark theme
- Visual bounding boxes and confidence scores
- Audio alarm system (pygame)
- Video recording capability
- Cross-platform support (Windows/Linux/macOS)

## Installation 🛠️

```bash
git clone https://github.com/yourusername/fire-detection-system.git
cd fire-detection-system
pip install -r requirements.txt
```

## Usage 🚀

```bash
python fire_detection_gui.py
```

**Controls:**
- 🟢 Start Camera: Begin live detection
- 🔴 Start Recording: Save footage (selects save directory)
- 🔊 Audio alerts auto-trigger on detection

## Project Structure 📂

```
fire-detection/
├── fire_detection_gui.py   # Main application
├── best.pt                # YOLOv8 model weights
├── alarm.wav              # Alert sound file
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── README.md             # Documentation
```

## Requirements 📋

```markdown
# requirements.txt
PyQt5==5.15.9
opencv-python==4.8.0.76
ultralytics==8.0.196
pygame==2.5.2
```


## Demo 🎥
https://github.com/daud-shah/fire-smoke-detection/blob/main/for%20linkdin.mp4


## Contribution 🤝

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Future Roadmap 🔮

| Feature               | Status  |
|-----------------------|---------|
| IP Camera Support     | Planned |
| Cloud Storage         | Planned |
| Mobile Notifications  | Planned |

---
