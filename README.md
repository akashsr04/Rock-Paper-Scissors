# Rock-Paper-Scissors Game 🎮

A Python-based Rock-Paper-Scissors game that uses YOLO for object recognition and OpenCV for real-time camera input. 
Play against the computer and see who wins!

---

## 🚀 Features
- Real-time object detection using YOLO.
- Interactive camera-based gameplay.

---

## 📖 Table of Contents
- [Installation](#installation)
    - Install requirements
##  *Change data.yaml file's train val and test fields to the train/images, valid/images and test\images locations (as their absolute path).
   - Train your own model :  yolo detect train data=path-to-your-data.yaml-file model=model-of-your-choice epochs=your-choice imgsz=preferably-640
   - Run Detector.py


---

## 💻 Installation

1. Clone the repository, Install requirements and run Detector.py file :
   ```bash
   git clone https://github.com/akashsr04/Rock-Paper-Scissors.git
   pip install -r requirements.txt
   python3 Detector.py
