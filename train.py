#implement model loading and visualisation

import librosa
import json 
import numpy as np
from pathlib import Path
from utility import split_data, extract_features,LABELS,spec_reverse,SaveData,LoadData
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
from CNN import Train,Net,torch,LossHistory,epoch_history,MODEL_NAME
from convert_data import sample_rate,FILENAME
import json

MODEL = "CNN"

DATA = np.load(FILENAME,allow_pickle=True)
x_train = DATA["x_train"]
y_train = DATA["y_train"]
x_val = DATA["x_val"] 
y_val = DATA["y_val"] 
x_test = DATA["x_test"]
y_test = DATA["y_test"]


print(f"\nfinal training samples: {len(x_train)}")
print(f"each sample has {len(x_train[0])} features")
print("split data successfully")

if MODEL == "CNN":
    Train(x_train,y_train,x_val,y_val)
    from CNN import LossHistory,epoch_history,ValHistory

print(" -- saved model -- ")
net = Net()
net.load_state_dict(torch.load(MODEL_NAME))
net.eval()

if MODEL=="CNN":

    label_to_index = {label: idx for idx, label in enumerate(LABELS)}
    y_test_idx = np.array([label_to_index[y] for y in y_test])

    pred = net.predict(x_test)
    y_true = y_test_idx
    y_pred = pred

    tp = 0
    for i in range(len(pred)):
        if y_true[i] == y_pred[i]: tp = tp + 1
    
    acc = tp/(len(y_test))
    print(f"accuracy on test: {acc*100}")

    cm = confusion_matrix(y_true,y_pred,labels=list(range(len(LABELS))) )

    disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=LABELS)
    disp.plot()
    
    plt.figure()
    plt.plot(epoch_history, LossHistory)
    plt.plot(epoch_history, ValHistory)
    plt.legend(["train","validation"])

    plt.show()
