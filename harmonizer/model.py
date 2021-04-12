import torch
from torch import nn


class Model(nn.Module):
    def __init__(self, lstm_size=512, LSTMLayersCount=2, outCount=26):
        super(Model, self).__init__()
        self.numNotes = 12
        self.lstm_size = lstm_size
        self.LSTMLayersCount = LSTMLayersCount
        self.outCount=outCount
        self.lstm = nn.LSTM(
            input_size=self.numNotes,
            hidden_size=self.lstm_size,
            num_layers=self.LSTMLayersCount,
            dropout=0.10,
            batch_first = True
        )
        self.linear = nn.Linear(
            in_features=self.lstm_size,
            out_features=self.lstm_size*4
            )

        self.relu = nn.ReLU()

        self.linear2=nn.Linear(
            in_features=self.lstm_size*4,
            out_features=self.outCount
        )

        self.sigmoid = nn.Sigmoid()

    def forward(self, x, prev):
        lstmOut, hState = self.lstm(x, prev)
        linearIn = lstmOut.reshape(-1, self.lstm_size)

        linearOut = self.linear(linearIn)
        reluOut = self.relu(linearOut)

        lin2out=self.linear2(reluOut)
        sigmoidOut = self.sigmoid(lin2out)
        
        return sigmoidOut, hState

    def init_state(self, batch_size):
        return (torch.zeros(self.LSTMLayersCount, batch_size, self.lstm_size),
                torch.zeros(self.LSTMLayersCount, batch_size, self.lstm_size))

