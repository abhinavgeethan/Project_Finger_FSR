import serial
from model import CNNModel
from torch_utils import *

model = CNNModel()
model.load_state_dict(torch.load("reached56NewModel.pth"))

# Establish serial connection with the Arduino
ser = serial.Serial('COM3', 9600, timeout=1) # Replace 'COM3' with the actual port name

prediction_lut = {0:"None", 1:"Thumb Rot", 2:"Thumb Addc", 3:"Index", 4:"Middle", 5:"Ring", 6:"Little"}

# Initialize a buffer to store the incoming data
data_buffer = []

# Loop to read incoming data from the serial port
while True:
    # Read incoming data
    data = ser.readline().strip().decode('utf-8')
       # Append the incoming data to the buffer
    if data:
        sensor_data = [float(x) for x in data.split(',')]  # parse sensor data
    else:
        continue
    
    data_buffer.append(sensor_data)

    # If we have received 311 lines of data, preprocess and make predictions
    if len(data_buffer) == 311:
        # Preprocess the data
        preprocessed_data = preprocess(data_buffer) # preprocess the data to match the input shape of the model
        break
        # Make predictions using the model
        predictions = model.predict(to_reshaped_tensor(preprocessed_data))

        # Get the predicted class
        predicted_class = torch_argmax(predictions[0])

        # Print the predicted class
        print(f"Predicted class: {predicted_class} - {prediction_lut[predicted_class]}")

        # Clear the buffer to start receiving new data
        data_buffer = []