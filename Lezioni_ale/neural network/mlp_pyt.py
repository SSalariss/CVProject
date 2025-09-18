import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch import nn
#import matplotlib.pyplot as plt


# import training ad testing data
training_data = datasets.FashionMNIST(root='data', train=True, download=True, transform=ToTensor())
test_data = datasets.FashionMNIST(root='data', train=False, download=True, transform=ToTensor())

device = ('cuda' if torch.cuda.is_available() else 'cpu')


class OurMLP(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(28*28, 50),
            nn.Sigmoid(),
            nn.Linear(50, 50),
            nn.Sigmoid(),
            nn.Linear(50, 10) # couse we have 10 classes
        )
        self.flatten = nn.Flatten()
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.mlp(x)
        return logits
    

# model initialization
model = OurMLP().to(device)


######### train the model

# define hyperparameters
epochs = 2             # How many times our model should analise the dataset
batch_size = 64         # Number of samples we get each times 
learning_rate = 0.0001   # Amount of changes allowed

# define the loss function
loss_fn = nn.CrossEntropyLoss()

# define the optimizer
optimizer = torch.optim.SGD(model.parameters(), learning_rate)


# define the training loop
def train_loop(dataloader, model, loss_fn, optimizer):
    
    size = len(dataloader)

    # get the batch from the dataset
    for batch, (X, y) in enumerate(dataloader):

        # move data on gpu
        X_gpu = X.to(device)
        y_tensor = torch.tensor([y])
        y_gpu = y_tensor.to(device)

        # compute the prediction and loss
        pred = model(X_gpu)
        loss = loss_fn(pred, y_gpu)


        # backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # print loss during training
        if batch % 500 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss},  [{current}/{size}]")


# testing loop
def test_loop(dataloader, model, loss_fn):
    size = len(dataloader)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    # disable weight update
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            y_tensor = torch.tensor([y])
            test_loss += loss_fn(pred, y_tensor).item()
            correct += (pred.argmax(1)).type(torch.float).sum().item()

            # print the accuracy and the average loss
            test_loss = test_loss / num_batches
            correct = correct / size
            print(f"Accuracy: {correct * 100}, Average Loss: {test_loss}")




# train the model
for t in range(epochs):
    print(f"Epochs: {t}")
    train_loop(training_data, model, loss_fn, optimizer)
    test_loop(test_data, model, loss_fn)


# PRINTS ===========================================
import matplotlib.pyplot as plt

# prendiamo il primo layer della rete
first_layer = model.mlp[0]   # nn.Linear(784, 50)

# estraiamo i pesi come numpy array
weights = first_layer.weight.data.cpu().numpy()

# scegliamo 5 neuroni da visualizzare
fig, axes = plt.subplots(1, 7, figsize=(15, 3))

for i, ax in enumerate(axes):
    w = weights[i].reshape(28, 28)  # rimettiamo i 784 valori in formato immagine
    ax.imshow(w, cmap="seismic")    # rosso = pesi positivi, blu = negativi
    ax.set_title(f"Neurone {i}")
    ax.axis("off")

plt.show()

# PRINTS ===========================================

print("Done")


"""
# label of the dataset
labels_map = {
    0: 'tshirt',
    1: 'trouser',
    2: 'pullover',
    3: 'dress',
    4: 'coat',
    5: 'sandal',
    6: 'shirt',
    7: 'sneaker',
    8: 'bag',
    9: 'ankle boot'
}

figure = plt.figure(figsize=(8, 8))
cols, rows = 3,3
for i in range(1, cols*rows+1):
    sample_idx = torch.randint(len(training_data), size=(1,)).item()
    img, label = training_data[sample_idx]
    figure.add_subplot(rows, cols, i)
    plt.title(labels_map[label])
    plt.axis('off')
    plt.imshow(img.squeeze(), cmap='gray')
plt.show()
"""