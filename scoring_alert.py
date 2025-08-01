import time
import winsound
import datetime
import csv

def count_closed_eyes(pred, names):
    """Count closed eyes from predictions"""
    closed_eyes = 0
    for det in pred:
        for *xyxy, conf, cls in det:
            label = names[int(cls)]
            if label.lower() == 'close_eyes':
                closed_eyes += 1
    return closed_eyes

def has_detections(pred):
    """Check if there are any detections"""
    return any(len(det) for det in pred)

class DrowsinessDetector:
    def __init__(self, threshold=15, max_closure_duration=2.0, log_file=None):
        self.score = 0
        self.threshold = threshold
        self.eye_closed_start = None
        self.max_closure_duration = max_closure_duration
        self.log_file = log_file
        
        if self.log_file:
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([f"Drowsiness Detection Log - {datetime.datetime.now()}"])
                writer.writerow(["Time", "Event", "Score", "Duration"])
    
    def process_detections(self, closed_eyes_count):
        if closed_eyes_count > 0:
            self.score += 1
            
            # Log eye detection
            if self.log_file:
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([datetime.datetime.now().strftime('%H:%M:%S'), "Eyes Closed", self.score, "-"])

            # Start or continue closure timing
            if self.eye_closed_start is None:
                self.eye_closed_start = time.time()
            else:
                elapsed = time.time() - self.eye_closed_start

                if elapsed >= self.max_closure_duration:
                    print("🚨 Eyes closed for too long! ({}s)".format(round(elapsed, 2)))
                    winsound.Beep(1200, 600)
                    
                    # Log time alert
                    if self.log_file:
                        with open(self.log_file, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([datetime.datetime.now().strftime('%H:%M:%S'), "Time Alert", self.score, f"{elapsed:.2f}s"])

        else:
            # Reset timer and reduce score
            if self.eye_closed_start is not None:
                elapsed = time.time() - self.eye_closed_start
                # Log eyes opened
                if self.log_file:
                    with open(self.log_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([datetime.datetime.now().strftime('%H:%M:%S'), "Eyes Opened", self.score, f"{elapsed:.2f}s"])
            
            self.eye_closed_start = None
            self.score = max(0, self.score - 1)

        # Score-based alert
        if self.score > self.threshold:
            print("⚠️ High drowsiness score: {}. Triggering alert!".format(self.score))
            winsound.Beep(1000, 500)
            
            # Log score alert
            if self.log_file:
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([datetime.datetime.now().strftime('%H:%M:%S'), "Score Alert", self.score, "-"])
    
    def handle_no_detections(self):
        self.score = max(0, self.score - 1)
        self.eye_closed_start = None