import torch

class CNNModel(torch.nn.Module):
  def __init__(self):
    super(CNNModel,self).__init__()
    self.layer1 = torch.nn.Conv2d(1,10,kernel_size=(4,3))
    self.batchnorm1 = torch.nn.LazyBatchNorm1d()
    self.maxpool1 = torch.nn.MaxPool2d(2)

    self.layer2 = torch.nn.Conv2d(10,32,kernel_size=3)
    self.batchnorm2 = torch.nn.LazyBatchNorm1d()
    self.maxpool2 = torch.nn.MaxPool2d(2)

    self.linear1 = torch.nn.LazyLinear(1000)
    self.linear2 = torch.nn.LazyLinear(250)
    self.linear3 = torch.nn.LazyLinear(50)
    self.linear4 = torch.nn.LazyLinear(7)

  def forward(self, feat):
    out = self.layer1(feat)
    out = self.maxpool1(out)
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