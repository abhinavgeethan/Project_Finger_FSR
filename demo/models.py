import torch

NUM_SENSORS = 6
NUM_CLASSES = 6

class CNNModel(torch.nn.Module):
  def __init__(self,num_classes = NUM_CLASSES):
    super(CNNModel,self).__init__()
    self.layer1 = torch.nn.Conv2d(1,10,kernel_size=(4,3))
    self.batchnorm1 = torch.nn.LazyBatchNorm1d()
    # self.maxpool1 = torch.nn.MaxPool2d(2)

    self.layer2 = torch.nn.Conv2d(10,32,kernel_size=3)
    self.batchnorm2 = torch.nn.LazyBatchNorm1d()
    self.maxpool2 = torch.nn.MaxPool2d(2)

    self.linear1 = torch.nn.LazyLinear(1000)
    self.linear2 = torch.nn.LazyLinear(250)
    self.linear3 = torch.nn.LazyLinear(50)
    self.linear4 = torch.nn.LazyLinear(num_classes)

  def forward(self, feat):
    out = self.layer1(feat)
    # out = self.maxpool1(out)
    out = self.batchnorm1(out)
    out = torch.nn.functional.relu(out)
    
    out = self.layer2(out)
    out = self.maxpool2(out)
    out = self.batchnorm2(out)
    out = torch.nn.functional.relu(out)

    out = torch.flatten(out)
    out = self.linear1(out)
    out = torch.nn.functional.relu(out)
    out = self.linear2(out)
    out = torch.nn.functional.relu(out)
    out = self.linear3(out)
    out = torch.nn.functional.relu(out)
    out = self.linear4(out)
    return torch.nn.functional.softmax(out,dim=0)
  
class LSTMModel(torch.nn.Module):
  def __init__(self, hidden_size=32, num_classes=NUM_CLASSES):
    super().__init__()
    self.lstm = torch.nn.LSTM(
        input_size = NUM_SENSORS,
        hidden_size = hidden_size,
        num_layers = 4,
        dropout = 0.5
    )
    self.linear = torch.nn.Linear(hidden_size,num_classes)

  def forward(self,features):
    self.lstm.flatten_parameters()
    _, (hn, _) = self.lstm(features)
    out = hn[-1]
    return self.linear(out)