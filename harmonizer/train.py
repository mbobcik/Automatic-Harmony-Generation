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

def predict():
    pass

def train (trainDs, model, batch_size, max_epochs, validDs=None):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = model.to(device)
    model.float()
    model.train()

    dataLoader = DataLoader(trainDs, batch_size=batch_size, drop_last=True)
    #criterion=nn.CrossEntropyLoss()
    #criterion= nn.BCEWithLogitsLoss()
    criterion= nn.BCELoss()
    optimizer=optim.Adam(model.parameters(),lr=0.00004)

    for epoch in range(max_epochs):
        state_h, state_c = model.init_state(batch_size)
        state_h=state_h.to(device)
        state_c=state_c.to(device)
    
        for batch, (x, y) in enumerate(dataLoader):
            optimizer.zero_grad()
            x = x.float().to(device)
            y = y.to(device)
            # x/y.shape = (batchSize, Seq_size, numNotes/chords)
            #x/y.permute.shape = (seqSize, batchsize,numnotes/chords)
            y_predicted, (state_h, state_c) = model(x, (state_h,state_c))
            loss=criterion(torch.reshape(y_predicted, y.shape).squeeze(), y.squeeze().float())
            #loss = criterion(y_predicted, y.squeeze())

            state_h=state_h.detach()
            state_c=state_c.detach()

            loss.backward()
            optimizer.step()
            if batch%10==0:
                print({'epoch':epoch, 'batch':batch, 'loss':loss.item()})

def saveModel(model, filepath):
    checkpoint = {
        #'numNotes' : model.numNotes,
        'lstm_size' : model.lstm_size,
        'LSTMLayersCount' : model.LSTMLayersCount,
        'state' : model.state_dict()
    }
    with open(filepath, 'wb') as f:
        torch.save(checkpoint, f)

def loadModel(filepath):
    with open(filepath, 'rb') as f:
        checkpoint = torch.load(f)
    model = Model(checkpoint['lstm_size'],checkpoint['LSTMLayersCount'])
    model.load_state_dict(checkpoint['state'])
    return model

if __name__ == "__main__": 

    batch_size=32
    max_epochs=10
    sequence_length=44
    
    dataset = Dataset(sequence_length=sequence_length)
    model = Model(outCount=dataset.chordCount)
    model.float()
    train(dataset, model, 
            batch_size=batch_size, 
            sequence_length=sequence_length, 
            max_epochs=max_epochs)
    
    saveModel(model, f"saved/LSTM_{model.lstm_size}nodes_{max_epochs}epochs_old.net")