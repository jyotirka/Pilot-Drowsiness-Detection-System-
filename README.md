 # Pilot Drowsiness Detection System   
 
 This project is a **real-time drowsiness detection system** developed for flight simulators to **monitor pilot alertness** and **trigger alerts** if signs of fatigue are detected. It uses a **YOLOv5-based custom-trained model** to detect **open and closed eyes** and raises an alarm when prolonged eye closure is detected to prevent accidents caused by driver fatigue. 

## Features

- **Real-time Detection**: Live monitoring through webcam or video feed
- **Dual Alert System**: 
  - Time-based alerts (eyes closed >2 seconds)
  - Score-based alerts (accumulated drowsiness)
- **Visual Feedback**: Live score bar on video feed
- **Audio Alerts**: Windows system beeps for immediate attention
- **Comprehensive Logging**: CSV logs for performance analysis
- **Easy Setup**: Simple command-line interface

## Requirements

- Windows OS (for audio alerts)
- Python 3.8+
- Webcam or video source
- Trained YOLOv5 model for eye detection

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd driver-drowsiness-detector
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Ensure you have:**
   - `best.pt` - Your trained model weights
   - Working webcam or video file

## Usage

### Basic Webcam Detection
```bash
python detect.py --source 0 --weights best.pt --view-img
```

### Video File Detection
```bash
python detect.py --source video.mp4 --weights best.pt --view-img
```

### Save Results
```bash
python detect.py --source 0 --weights best.pt --view-img --save-csv
```

### With Custom Confidence Threshold
```bash
python detect.py --weights best.pt --source 0 --conf 0.4
```

## Key Parameters

- `--source 0` - Use webcam (or path to video file)
- `--weights best.pt` - Path to trained model
- `--view-img` - Display live video feed
- `--save-csv` - Save detection results to CSV
- `--conf-thres 0.25` - Confidence threshold for detections

## Model Requirements

The system requires a YOLOv5 model trained to detect:
- `close_eyes` class - For closed eye detection

## Output Files

- `drowsiness_log.csv` - Drowsiness events and timing
- `predictions.csv` - All detection results (if --save-csv used)
- Saved images/videos with detections

## System Configuration

### Drowsiness Parameters
- **Score Threshold**: 15 (adjustable in code)
- **Max Closure Duration**: 2.0 seconds
- **Alert Frequencies**: 1000Hz (score), 1200Hz (time)

### Customization
Edit `scoring_alert.py` to modify:
- Alert thresholds
- Timing parameters
- Audio alert settings

### Improving the Model (Transfer Learning on More Data)
If you want to improve the detection by adding more eye images:

**1. Download YOLOv5 Repository**
YOLOv5 repo is required to access training scripts and architecture files.

git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt

**2. Collect More Labeled Data**
Capture additional images of open and closed eyes from various angles and lighting conditions.

Annotate using tools like:LabelImg , Roboflow Annotate

Make sure to label them with the same classes:
0: close_eyes
1: open_eyes

**3. Reorganize Dataset**
Structure it like this:

```
data/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/

```

**4. Update data.yaml**

Create a data.yaml file like:

train: ./data/images/train
val: ./data/images/val
nc: 2
names: ['close_eyes', 'open_eyes']

**5. Resume Training from best.pt**

python train.py --img 640 --batch 16 --epochs 50 --data data.yaml --weights best.pt --cache
This will fine-tune your existing model on the new data without retraining from scratch 

## Future Improvements

- Add PERCLOS (percentage eye closure over time)
-Multimodal fatigue detection (yawn + head pose)
-Real-time pilot performance logging in simulator
-Escalating alert system

## Project Structure

```
driver-drowsiness-detector/
├── detect.py              # Main detection script
├── scoring_alert.py       # Drowsiness detection logic
├── requirements.txt       # Dependencies
├── best.pt               # Trained model weights
├── models/               # YOLOv5 model architecture
└── utils/                # YOLOv5 utilities
```

## Troubleshooting

**No audio alerts:**
- Ensure Windows OS with working speakers
- Check system volume settings

**Model not loading:**
- Verify `best.pt` file exists
- Check model was trained for eye detection

**Poor detection:**
- Adjust `--conf-thres` parameter
- Ensure good lighting conditions
- Check webcam positioning

## License

This project is based on YOLOv5 by Ultralytics.

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request

## Support

For issues and questions, please create an issue in the repository.