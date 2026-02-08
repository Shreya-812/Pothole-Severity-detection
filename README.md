# Pothole Severity Detection Using IMU and Decision Tree

## 🚧 Project Summary

This project detects pothole severity in real-time using IMU sensor data (pitch and roll) processed with a Decision Tree classifier. The classification results are visualized on an interactive map interface using color-coded markers, enabling users to monitor road conditions remotely.


---

## 🛠️ Technologies Used

- **ESP32 + MPU6050** for real-time IMU data
- **Python** for model training & prediction
- **Decision Tree Classifier (Scikit-learn)**
- **ThingSpeak API** for data logging and transmission
- **JavaScript + Leaflet.js** for map-based visualization

---

## 🔄 Workflow

1. **Data Collection**  
   The ESP32 board continuously reads pitch and roll values from the MPU6050 sensor and transmits them to a ThingSpeak channel.

2. **AI Prediction**  
   A Python script periodically fetches the IMU data from ThingSpeak, applies a trained Decision Tree model, classifies the road condition (Good/Moderate/Bad), and sends this classification to a second ThingSpeak channel.

3. **Visualization**  
   A web-based frontend (HTML + JavaScript) pulls the AI prediction results from ThingSpeak and displays them as color-coded markers on a Leaflet.js map:
   - 🟢 Green: Good
   - 🟠 Orange: Moderate
   - 🔴 Red: Bad

---

## 🧠 Model Details

- **Features**: `pitch`, `roll`
- **Labels**: 
  - `1`: Good  
  - `2`: Moderate  
  - `3`: Bad  
- **Model**: `DecisionTreeClassifier` from `scikit-learn`
- **Training**: Conducted offline on labeled pitch/roll datasets

---

## 📈 Future Enhancements

- Use GPS modules to geotag pothole locations
- Improve accuracy with ensemble models like Random Forest or XGBoost
- Migrate backend processing to a cloud platform for scalability
- Trigger real-time alerts to municipal dashboards
- Integrate video/image-based pothole validation for cross-check

---

## 🚀 Getting Started

### Prerequisites

- ESP32 board and MPU6050 sensor
- ThingSpeak account with two channels:
  - Channel 1: Raw IMU data
  - Channel 2: AI-predicted severity
- Python 3 environment with `requests`, `sklearn`, etc.
- Web browser to run the map interface (`index.html`)

### Instructions

1. Flash `imu_to_thingspeak.ino` to ESP32 with your Wi-Fi and API keys
2. Run `ai_predictor.py` script periodically (or use a scheduler like `cron`)
3. Open `index.html` in browser to view live road condition markers

---

## 🤝 Contributors

- Shreya Singh – Core Developer & Research Lead

---
