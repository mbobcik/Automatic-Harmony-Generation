import torch
from torch import nn
try:
    from harmonizer.dataset import Dataset
except:
    from dataset import Dataset

class Model(nn.Module):
    def __init__(self, dataset):
        super(Model, self).__init__()
        self.numNotes = 12
        self.lstm_size = 128
        self.embedding_dim = 128
        self.LSTMLayersCount = 2

        self.lstm = nn.LSTM(
            input_size=self.numNotes,
            hidden_size=self.lstm_size,
            num_layers=self.LSTMLayersCount,
            dropout=0.1,
        )
        self.linear = nn.Linear(
            in_features=self.lstm_size,
            out_features=self.numNotes)

    def forward(self, x, prev):
        lstmOut, hState = self.lstm(x, prev)
        linearIn = lstmOut.reshape(-1, self.lstm_size)
        linearOut = self.linear(linearIn)
        return linearOut, hState

    def init_state(self, sequence_length):
        return (torch.zeros(self.LSTMLayersCount,sequence_length,self.lstm_size),
                torch.zeros(self.LSTMLayersCount,sequence_length,self.lstm_size))

