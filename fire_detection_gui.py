import sys
import cv2
from ultralytics import YOLO
import pygame
import threading
import datetime
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, 
                            QWidget, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap, QColor, QPalette
from PyQt5.QtCore import QTimer, Qt

class FireDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fire/Smoke Detection System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Load model and setup video
        self.model = YOLO("best.pt")  # Update path to your model
        self.alarm_sound = "alarm.wav"  # Update path to your sound file
        self.cap = None
        self.recording = False
        self.out = None
        self.frames = []
        
        # Setup UI
        self.init_ui()
        
        # Timer for video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def init_ui(self):
        # Main widgets
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        
        # Buttons
        self.camera_btn = QPushButton("Start Camera")
        self.camera_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.camera_btn.clicked.connect(self.toggle_camera)
        
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f44336;
                border: none;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            """
        )
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setEnabled(False)
        
        # Status label
        self.status_label = QLabel("Status: Camera Off")
        self.status_label.setStyleSheet("font-size: 14px; color: #666;")
        
        # Layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.camera_btn)
        control_layout.addWidget(self.record_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.status_label)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
    def toggle_camera(self):
        if self.cap is None:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.setText("Status: Error opening camera")
            return
            
        self.camera_btn.setText("Stop Camera")
        self.record_btn.setEnabled(True)
        self.status_label.setText("Status: Camera On")
        self.timer.start(20)  # Update every 20ms
    
    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.recording:
            self.stop_recording()
            
        self.video_label.clear()
        self.video_label.setStyleSheet("background-color: black;")
        self.camera_btn.setText("Start Camera")
        self.record_btn.setText("Start Recording")
        self.record_btn.setEnabled(False)
        self.status_label.setText("Status: Camera Off")
    
    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        # Get save location
        options = QFileDialog.Options()
        save_dir = QFileDialog.getExistingDirectory(
            self, 
            "Select Save Directory", 
            os.path.expanduser("~"), 
            options=options
        )
        if not save_dir:
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_path = os.path.join(save_dir, f"detection_{timestamp}.avi")
        
        # Get video properties
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # Initialize VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(
            self.save_path, 
            fourcc, 
            fps if fps > 0 else 20.0, 
            (width, height)
        )
        
        self.recording = True
        self.record_btn.setText("Stop Recording")
        self.status_label.setText(f"Status: Recording to {os.path.basename(self.save_path)}")
    
    def stop_recording(self):
        if self.out:
            self.out.release()
            self.out = None
        self.recording = False
        self.record_btn.setText("Start Recording")
        if self.cap:
            self.status_label.setText("Status: Camera On")
        else:
            self.status_label.setText("Status: Camera Off")
    
    def play_alarm(self):
        pygame.mixer.music.load(self.alarm_sound)
        pygame.mixer.music.play()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("Status: Error reading frame")
            return
            
        # Perform detection
        results = self.model(frame, conf=0.25, iou=0.25, device='cpu')
        
        # Process results
        fire_detected = False
        for r in results:
            for box in r.boxes:
                cls = int(box.cls)
                conf = float(box.conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_name = r.names[cls]
                
                if class_name in ['fire', 'smoke']:
                    fire_detected = True
                    color = (0, 0, 255)  # Red
                else:
                    color = (255, 255, 0)  # Yellow
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                label = f"{class_name} {conf:.2f}"
                cv2.putText(
                    frame, 
                    label, 
                    (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    color, 
                    2
                )
        
        # Trigger alarm if fire detected
        if fire_detected:
            self.status_label.setText("ALERT: Fire/Smoke Detected!")
            threading.Thread(target=self.play_alarm, daemon=True).start()
            cv2.putText(
                frame, 
                "ALERT: FIRE/SMOKE DETECTED!", 
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 0, 255), 
                3
            )
        
        # Save frame if recording
        if self.recording and self.out:
            self.out.write(frame)
        
        # Display frame in GUI
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))
    
    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

def set_dark_theme(app):
    """Apply a dark theme to the application"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set dark theme
    set_dark_theme(app)
    
    window = FireDetectionApp()
    window.show()
    sys.exit(app.exec_())