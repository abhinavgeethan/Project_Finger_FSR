import serial
from models import CNNModel, LSTMModel
from torch_utils import *

NUM_SENSORS = 6
NUM_CLASSES = 6
NUM_TIMESTEPS = 64

CNN_model = CNNModel(num_classes=NUM_CLASSES)
CNN_model.load_state_dict(torch.load("demo/CNN_model.pth"))
LSTM_model = LSTMModel(num_classes=NUM_CLASSES)
LSTM_model.load_state_dict(torch.load("demo/LSTM_model.pth"))

# Establish serial connection with the Arduino
ser = serial.Serial('COM7', 9600)

prediction_lut = {0:"None", 1:"Thumb", 2:"Index", 3:"Middle", 4:"Ring", 5:"Little"}

# Initialize a buffer to store the incoming data
data_buffer = []

# Loop to read incoming data from the serial port
while True:
    # Read incoming data
    data = ser.readline().strip().decode('utf-8')
       # Append the incoming data to the buffer
    if data:
        sensor_data = [float(x) for x in data.split(',')]  # parse sensor data
        if len(sensor_data) != NUM_SENSORS:
            continue
    else:
        continue
    
    data_buffer.append(sensor_data)

    # If we have received NUM_TIMESTEPS lines of data, preprocess and make predictions
    if len(data_buffer) == NUM_TIMESTEPS:
        # Preprocess the data
        preprocessed_data = preprocess(data_buffer) # preprocess the data to match the input shape of the model
        
        # Make predictions using the model
        CNN_predictions = CNN_model.predict(to_CNN_reshaped_tensor(preprocessed_data,NUM_TIMESTEPS,NUM_SENSORS))
        LSTM_predictions = LSTM_model.predict(to_LSTM_reshaped_tensor(preprocessed_data,NUM_TIMESTEPS,NUM_SENSORS))

        # Get the predicted class
        CNN_predicted_class = torch_argmax(CNN_predictions)
        LSTM_predicted_class = torch_argmax(LSTM_predictions)

        # Print the predicted class
        print(f"CNN: Predicted class: {CNN_predicted_class} - {prediction_lut[CNN_predicted_class]}")
        print(f"LSTM: Predicted class: {LSTM_predicted_class} - {prediction_lut[LSTM_predicted_class]}")

        # Clear the buffer to start receiving new data
        data_buffer = []