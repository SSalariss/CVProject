import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch import nn


import torchmetrics

#import matplotlib.pyplot as plt


# import training ad testing data
training_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=ToTensor())
test_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=ToTensor())

device = ('cuda' if torch.cuda.is_available() else 'cpu')

# define our cnn
class OurCNN(nn.Module):
    
    def __init__(self):
        super().__init__()
        
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 5, 3), # 1: one channel = gray images      (64, 1, 28, 28)
            nn.ReLU(),
            nn.Conv2d(5, 10, 3), # (64, 5, 26, 26)
            nn.ReLU()
        )

        self.mlp = nn.Sequential(
            nn.Linear(24*24*10, 10),
            nn.ReLU(),
            nn.Linear(10, 10)
        )

    def forward(self, x):
        x = self.cnn(x)

        x = torch.flatten(x, 1)

        x = self.mlp(x)
        return x


# shape of the tensor
# (B, C, W, H)


# Model initialization

model = OurCNN()
######### train the model


# define hyperparameters
epochs = 2             # How many times our model should analise the dataset
batch_size = 64         # Number of samples we get each times 
learning_rate = 0.001   # Amount of changes allowed


# create the dataloader
train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)


# define the loss function
loss_fn = nn.CrossEntropyLoss()

# define the optimizer
#optimizer = torch.optim.SGD(model.parameters(), learning_rate)
optimizer = torch.optim.AdamW(model.parameters(), learning_rate)

# create the accuracy metric 
metric = torchmetrics.Accuracy(task='multiclass', num_classes=10) 

# define the training loop
def train_loop(dataloader, model, loss_fn, optimizer):

    # get the batch from the dataset
    for batch, (X, y) in enumerate(dataloader):

        # move data on gpu
        #X_gpu = X.to(device)
        #y_tensor = torch.tensor([y])
        #y_gpu = y_tensor.to(device)

        # compute the prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)


        # backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # print loss during training
        if batch % 100 == 0:
            acc = metric(pred, y)
            print(f"[Training] Accuracy on current batch: {acc}")
    
    # print the final training accuracy
    acc = metric.compute()
    print(f"[Training] Accuracy at the end of the epoch: {acc}")
    metric.reset()  # for each epoch otherwise we will sum the accuracy

# testing loop
def test_loop(dataloader, model, loss_fn):

    # disable weight update
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            acc = metric(pred, y)

    # print the final training accuracy
    acc = metric.compute()
    print(f"[Testing] Accuracy at the end of the epoch: {acc}")
    metric.reset()  # for each epoch otherwise we will sum the accuracy



# train the model
for t in range(epochs):
    print(f"Epochs: {t}")
    #train_loop(training_data, model, loss_fn, optimizer)
    #test_loop(test_data, model, loss_fn)
    train_loop(train_dataloader, model, loss_fn, optimizer)
    test_loop(test_dataloader, model, loss_fn)

print("Done")
