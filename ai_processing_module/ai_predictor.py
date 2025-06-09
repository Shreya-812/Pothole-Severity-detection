import requests
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# ThingSpeak Write API URL and Key
write_api_url = "https://api.thingspeak.com/update"
write_api_key = "MNVFJSAFSKLNVQIZ"  # Replace with your actual Write API Key

# Function to generate training data
def generate_training_data():
    data = []
    for roll in range(-10, 11):
        for pitch in range(-10, 11):
            if abs(roll) <= 3 and abs(pitch) <= 3:
                condition = "Good"
            elif 4 <= abs(roll) <= 6 or 4 <= abs(pitch) <= 6:
                condition = "Moderate"
            else:
                condition = "Bad"
            data.append({"Roll angle": roll, "Pitch angle": pitch, "Condition": condition})
    return pd.DataFrame(data)

# Function to train and save the model
def train_model():
    df = generate_training_data()
    X = df[["Roll angle", "Pitch angle"]]
    y = df["Condition"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    joblib.dump(model, "road_bump_model.pkl")
    print("Model saved as 'road_bump_model.pkl'.")

# Function to fetch data and predict conditions, then send output to ThingSpeak
def fetch_data_and_predict():
    model = joblib.load("road_bump_model.pkl")

    # ThingSpeak Read API URL
    read_api_url = "https://api.thingspeak.com/channels/2820814/feeds.json?results=2"

    while True:
        try:
            response = requests.get(read_api_url)
            if response.status_code == 200:
                data = response.json()
                feeds = data['feeds']

                if feeds:
                    for feed in feeds:
                        timestamp = feed['created_at']
                        roll = float(feed.get('field1', 0))
                        pitch = float(feed.get('field2', 0))
                        input_data = pd.DataFrame([[roll, pitch]], columns=["Roll angle", "Pitch angle"])
                        condition = model.predict(input_data)[0]

                        # Map condition to numeric values
                        condition_numeric = {"Good": 1, "Moderate": 2, "Bad": 3}
                        numeric_value = condition_numeric[condition]

                        # Send the numeric value to ThingSpeak
                        payload = {
                            "api_key": write_api_key,
                            "field1": numeric_value
                        }
                        write_response = requests.get(write_api_url, params=payload)

                        if write_response.status_code == 200 and write_response.text != "0":
                            print(f"Data sent successfully to ThingSpeak. Entry ID: {write_response.text}")
                        else:
                            print(f"Failed to send data. Response: {write_response.text}")

                        print(f"Timestamp: {timestamp}")
                        print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°")
                        print(f"Predicted Condition: {condition} ({numeric_value})")
                        print("-" * 30)

                else:
                    print("No new data available.")
            else:
                print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

            time.sleep(15)  # Wait to avoid exceeding ThingSpeak rate limits

        except KeyboardInterrupt:
            print("Monitoring stopped.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

# Train the model and start prediction
train_model()
fetch_data_and_predict()
