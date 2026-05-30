import cv2
import os
import platform
from ultralytics import YOLO
import time

class PresenceEngine:
    def __init__(self, threshold=30, debounce=10, conf_threshold=0.5):
        self.model = YOLO('yolov8n.pt') 
        self.absent_counter = 0
        self.missed_frames = 0 # NEW: The "Debounce" counter
        self.debounce = debounce # Only go "ABSENT" if missed for 10 frames
        self.threshold = threshold 
        self.conf_threshold = conf_threshold
        
    def process_frame(self, frame):
        results = self.model(frame, classes=[0], verbose=False, conf=self.conf_threshold)
        
        if len(results[0].boxes) > 0:
            self.missed_frames = 0 # Reset the debounce
            self.absent_counter = 0
            
            # Visuals
            box = results[0].boxes[0].xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            return "PRESENT"
        else:
            self.missed_frames += 1
            
            # Only start the actual "Absent" counter if we've missed 10 frames
            if self.missed_frames >= self.debounce:
                self.absent_counter += 1
                
                if self.absent_counter >= self.threshold:
                    return "LOCKED: Locking system......." 
                
                return f"ABSENT ({self.absent_counter})"
            
            return "Checking..."

def trigger_lock():
    os_name = platform.system()
    print(f"Triggering lock for {os_name}...")
    
    if os_name == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif os_name == "Darwin":  # macOS
        os.system('pmset displaysleepnow')
    elif os_name == "Linux":
        os.system('xdg-screensaver lock')

def main():
    engine = PresenceEngine(threshold=30)
    cap = cv2.VideoCapture(0)

    print("System Started. Monitoring for presence...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        status = engine.process_frame(frame)
        
        color = (0, 255, 0) if "PRESENT" in status else (0, 0, 255)
        cv2.putText(frame, f"STATUS: {status}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        cv2.imshow("Presence Monitor", frame)

        if "LOCKED" in status:
            print("Locking system....")
            cv2.waitKey(1000)
            trigger_lock()
            break 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()