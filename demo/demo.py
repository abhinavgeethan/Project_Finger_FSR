import os
import time
import serial
from models import CNNModel, LSTMModel
from torch_utils import *

NUM_SENSORS = 6
NUM_CLASSES = 6
NUM_TIMESTEPS = 64

print("Loading CNN Model")
CNN_model = CNNModel(num_classes=NUM_CLASSES)
CNN_model.load_state_dict(torch.load("demo/CNN_model.pth",map_location=torch.device('cpu')))
print("Successfully Loaded CNN Model")
print("Loading LSTM Model")
LSTM_model = LSTMModel(num_classes=NUM_CLASSES)
LSTM_model.load_state_dict(torch.load("demo/LSTM_model.pth",map_location=torch.device('cpu')))
print("Successfully Loaded LSTM Model")
# Establish serial connection with the Arduino
ser = serial.Serial('COM7', 9600)
print("Connected to Arduino",flush=True)

prediction_lut = {0:"None", 1:"Thumb", 2:"Index", 3:"Middle", 4:"Ring", 5:"Little"}

# Initialize a buffer to store the incoming data
data_buffer = []

# Loop to read incoming data from the serial port
timer = time.perf_counter()
while True:
    # Read incoming data
    data = ser.readline().strip().decode('utf-8')
       # Append the incoming data to the buffer
    if data:
        try:
            # sensor_data = [float(x) for x in data.split(',')]  # parse sensor data
            if not len(data.split(',')) != NUM_SENSORS:
                data_buffer.append(data)
        except ValueError:
            continue
    else:
        continue
    
    # If we have received NUM_TIMESTEPS lines of data, preprocess and make predictions
    if len(data_buffer) == NUM_TIMESTEPS:
        # Preprocess the data
        preprocessed_data = preprocess(data_buffer,NUM_TIMESTEPS,NUM_SENSORS) # preprocess the data to match the input shape of the model
        
        with torch.no_grad():
            # Make predictions using the model
            CNN_predictions = CNN_model(to_CNN_reshaped_tensor(preprocessed_data,NUM_TIMESTEPS,NUM_SENSORS))
            LSTM_predictions = LSTM_model(to_LSTM_reshaped_tensor(preprocessed_data,NUM_TIMESTEPS,NUM_SENSORS))

        # Get the predicted class
        CNN_predicted_class = torch_argmax(CNN_predictions)
        LSTM_predicted_class = torch_argmax(LSTM_predictions)

        # Print the predicted class
        os.system('cls')
        print(f"CNN: Predicted class: {CNN_predicted_class} - {prediction_lut[CNN_predicted_class]} | LSTM: Predicted class: {LSTM_predicted_class} - {prediction_lut[LSTM_predicted_class]} | Time: {round(time.perf_counter()-timer,4)}s")

        # Clear the buffer to start receiving new data
        data_buffer = []
        timer = time.perf_counter()