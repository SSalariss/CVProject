import os
import pandas as pd
from torch.utils.data import  Dataset
from torchvision import read_image

class MyDatasetLoader(Dataset):
    
    def __init__(self, labels, img_dir, transform=None) -> None:
        #super().__init__() we don't need the super function
        self.img_dir = img_dir
        self.transform = transform
        self.labels = pd.read_csv(labels)


    def __len__(self) -> int:
        return len(self.labels)

    
    def __getitem__(self, index):
        # return super().__getitem__(index)

        # create the images path
        # e.g. img_dir = 'data\' + 'img1.jpg' with index = 0
        # index, 0: row: index and column 0.
        imgs_path = os.join(self.img_dir, self.labels.iloc[index, 0])

        # read the image through its path
        image = read_image(imgs_path)

        # read the label
        label = self.labels.iloc[index, 1]

        # apply the transformations
        if self.transform:
            image = self.transform(image)
            label = self.transform(label)

        return image, label

"""
Create a Dataloader class

Label example

img1.jpg, 0
img2.jpg, 1
img3.jpg, 2
img4.jpg, 0
"""
