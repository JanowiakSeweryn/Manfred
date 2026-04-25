#make save the model and validation 
#visualise the model_>what is the hidden layer in there

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
from utility import LABELS,get_version
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import sys

EPOCHS = 20
BATCH_SIZE = 16
LEARNING_RATE = 0.001

LossHistory = []
ValHistory = []
epoch_history = []

features_shape = [64,32]

UPDATE_MODEL = False

MODEL_NAME = get_version()

HIDDEN_LAYER_SIZE = [128,48]


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.epochs = []
        self.LossHistory = []
        self.ValHistory = []
        self.output_number = len(LABELS)
        # ----- Convolutional blocks -----

        self.block1 = nn.Sequential(
            nn.Conv2d(1, 40, kernel_size=3, padding=1),
            nn.BatchNorm2d(40),
            nn.ReLU(),
            nn.MaxPool2d((2, 1))
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(40, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d((2, 2))
        )

        self.fc = []


        self.block3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d((2, 2))
        )

        #fully connected layer
        self._init_fc_layers()

    def predict(self, X, device="cpu"):
        """
        X: numpy array of shape [N, 128, 87] (Mel-spectrograms)
        Returns: predicted class indices
        """
        self.eval()
        X_tensor = torch.tensor(X, dtype=torch.float32).unsqueeze(1).to(device)  # [N,1,128,87]
        with torch.no_grad():
            outputs = self.forward(X_tensor)            # [N, num_classes]
            preds = outputs.argmax(dim=1).cpu().numpy() # convert to numpy

        return preds

    # def LoadModel(self):
        # state_dict = torch.load(MODEL_NAME)
        # self.load_state_dict(state_dict)

        # t_layer_key = list(state_dict.keys())[-2] # -2 because the very last is usually '.bias'
        # last_layer_weight = state_dict[last_layer_key]

        # The first dimension is the number of outputs
        # self.output_number = get_model_output_size(MODEL_NAME)

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        # x = self.block3(x)

        x = torch.flatten(x, 1)

        # for i in range(len(self.fc)-1):
        #     x = F.relu(self.fc[i](x))
        

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))

        return self.fc3(x)

    def _init_fc_layers(self):
        with torch.no_grad():
            dummy = torch.zeros(1, 1, features_shape[0], features_shape[1])  # your Mel shape
            x = self.block1(dummy)
            x = self.block2(x)
            # x = self.block3(x)
            self.flattened_size = x.numel()

        # for i in range(len(HIDDEN_LAYER_SIZE)):
        #     if i == 0:
        #         self.fc.append(nn.Linear(self.flattened_size, HIDDEN_LAYER_SIZE[0]))
        #     elif i != len(HIDDEN_LAYER_SIZE) :
        #         self.fc.append(nn.Linear(HIDDEN_LAYER_SIZE[i-1], HIDDEN_LAYER_SIZE[i]))
        #     else:
        #         self.fc.append(nn.Linear(HIDDEN_LAYER_SIZE[i-1], self.output_number))
        
        self.fc1 = nn.Linear(self.flattened_size,HIDDEN_LAYER_SIZE[0])
        self.fc2 = nn.Linear(HIDDEN_LAYER_SIZE[0],HIDDEN_LAYER_SIZE[1])
        self.fc3 = nn.Linear(HIDDEN_LAYER_SIZE[1],self.output_number)


        print(f" -- HIDDEN LAYER SIZE INITIALIZED -- ")
        # self.fc4 = nn.Linear(64, 6)

#converts data to more pytorch friendly format 
#return data -> torch format of data
#
def Convert2Torch(x_train,y_train,batch_size=BATCH_SIZE):
    x_train = torch.tensor(x_train, dtype=torch.float32).unsqueeze(1)
    # labes as vector of probability for all your classes
    label_to_index = {label: idx for idx, label in enumerate(LABELS)}
    # y_train_idx = np.array([label_to_index[y] for y in y_train])
    y_train_idx = torch.tensor([label_to_index[y] for y in y_train], dtype=torch.long)
    
    #this is my data but with torch
    data = TensorDataset(x_train, y_train_idx)
    train_loader = DataLoader(data, batch_size=batch_size, shuffle=True)

    return data,train_loader

def Train(x_train,y_train,x_val,y_val,batch_size=BATCH_SIZE):

    global epoch_history, LossHistory,ValHistory
    
    net = None

    if sys.platform == "win32":
        import torch_directml  
        print(" -- USING GPU -- ")
        device = torch_directml.device()
    else:
        print(" -- USING CPU -- ")
        device =torch.device("cpu")

    net = Net().to(device)

    criterion = nn.CrossEntropyLoss()
    loss_fn = nn.CrossEntropyLoss()
    # optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)
    optimizer = optim.SGD(net.parameters(), lr=LEARNING_RATE, momentum=0.5)
    train_data,train_loader = Convert2Torch(x_train,y_train)
    val_data,val_loader = Convert2Torch(x_val,y_val)

    for epoch in range(EPOCHS):  # loop over the dataset multiple times

        running_loss = 0.0
        running_vloss = 0.0

        net.train() #setting model to train mode

        for i,(inputs,labels) in enumerate(train_loader):

            inputs = inputs.to(device)
            labels = labels.to(device)
            # get the inputs; data is a list of [inputs, labels]
            # x_train_tensor = torch.from_numpy(x_train)
            # inputs = x_train[i].unsqueeze(1)
            # labels = torch.tensor(y_train_idx[i], dtype=torch.long).unsqueeze(0)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()

        
        net.eval() #setting model to validation mode

        # Disable gradient computation and reduce memory consumption.
        with torch.no_grad():
            for i, vdata in enumerate(val_loader):
                vinputs, vlabels = vdata

                vinputs = vinputs.to(device)
                vlabels = vlabels.to(device)
                voutputs = net(vinputs)
                vloss = loss_fn(voutputs, vlabels)
                running_vloss += vloss.item()

        net.epochs.append(epoch)
        net.LossHistory.append(running_loss/len(train_loader))
        net.ValHistory.append(running_vloss/len(val_loader))

        # if running_vloss/len(val_loader) < 0.14:
        #     break
        
        print(f"epoch {epoch} train loss = {running_loss/len(train_loader)} val: {running_vloss/len(val_loader)}")

    #early stopping
        # if net.ValHistory[-1] < 1e-4: break
        
    epoch_history = net.epochs
    LossHistory = net.LossHistory
    ValHistory = net.ValHistory

    # print(f"epoch: {len(epoch_history)}")
    # print(f"loss: {len(LossHistory)}")
    # print(f"validation: {len(ValHistory)}")


    torch.save(net.state_dict(), MODEL_NAME)

# def get_model_output_size(pth_path):
#     sd = torch.load(pth_path, map_location='cpu')
#     # We look for the bias of the last layer because its size is 1D 
#     # and directly represents the number of classes.
#     bias_keys = [k for k in sd.keys() if 'bias' in k]
#     return sd[bias_keys[-1]].shape[0]


