import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader, dataloader
try:
    from harmonizer.model import Model
except:
    from model import Model
try:
    from harmonizer.dataset import Dataset
except:
    from dataset import Dataset


def train (dataset, model, batch_size, max_epochs, sequence_length):
    model.float()
    model.train()
    dataLoader = DataLoader(dataset, batch_size=batch_size)
    #criterion=nn.CrossEntropyLoss()
    criterion= nn.BCEWithLogitsLoss()
    optimizer=optim.Adam(model.parameters(),lr=0.001)
    
    for epoch in range(max_epochs):
        state_h, state_c = model.init_state(sequence_length)

        for batch, (x, y) in enumerate(dataLoader):
            optimizer.zero_grad()

            y_predicted, (state_h, state_c) = model(x.float(), (state_h,state_c))
            #ypred.shape == batchsize*sequenceLength,12
            loss=criterion(torch.reshape(y_predicted, y.shape), y)
            #target= torch.argmax(y, 1)
            #loss=criterion(y_predicted, target)

            state_h=state_h.detach()
            state_c=state_c.detach()

            loss.backward()
            optimizer.step()

            print({'epoch':epoch, 'batch':batch, 'loss':loss.item()})


batch_size=1024
max_epochs=10
sequence_length=4

dataset = Dataset(sequence_length=sequence_length)
model = Model(dataset)
model.float()
train(dataset, model, 
        batch_size=batch_size, 
        sequence_length=sequence_length, 
        max_epochs=max_epochs)