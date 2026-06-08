# PresenceMonitor

An AI-powered security utility that leverages computer vision to provide automated, privacy-focused workstation security. 

## 💡 Why This Project?
In remote or open-office environments, workstation privacy is often compromised when a user leaves their desk unattended. Manual screen locking is easily forgotten, creating security gaps. This project transforms the workstation into an intelligent, autonomous agent that detects human presence and secures the system the moment the user steps away.

[Presence Monitor Demo](https://github.com/SanniIsimpa/PresenceMonitor/blob/main/Presence_monitor.gif)
---

## 🛠 Engineering Challenges & Solutions

### 1. The Stability Problem (Stochastic Detection)
* **Challenge:** Raw model outputs from YOLOv8 are inherently stochastic, they flicker due to lighting changes, movement, or occlusion, which would cause the system to trigger constant, annoying "Lock/Unlock" cycles.
* **Solution:** I implemented a **temporal debouncing algorithm**. The system requires the target to be "absent" for a configurable threshold (e.g., 3 seconds of continuous negative detection) before triggering a lock. This effectively filters out transient noise and ensures a smooth, reliable user experience.

### 2. UI Responsiveness
* **Challenge:** Standard OpenCV video processing loops often block the main thread, causing the window to freeze or become unresponsive.
* **Solution:** I refactored the processing pipeline into a non-blocking architecture, ensuring that visual feedback and system logic run independently of the inference process.

## 🚀 Key Features
* **Real-Time Detection:** Powered by YOLOv8 for high-accuracy human presence monitoring.
* **Logic-Based Filtering:** Signal debouncing to prevent false triggers.
* **Native Integration:** OS-level locking capabilities via `pyautogui`.

## 📋 Requirements
- Python 3.8+
- `ultralytics`
- `opencv-python`
- `pyautogui`

## ⚙️ Installation & Usage
1. Clone this repository:
   ```bash
   git clone [https://github.com/SanniIsimpa/PresenceMonitor.git](https://github.com/SanniIsimpa/PresenceMonitor.git)
