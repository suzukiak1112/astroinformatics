import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import spectral_library

num_test = 100
batch_size = 32
num_epochs = 200
learning_rate = 1.0e-3

class star_net(nn.Module):

    def __init__(self, n_wave):

        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(n_wave, 1024),
            nn.ReLU(),
            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)
    
    
if __name__=='__main__':

    # read data
    spec = spectral_library.miles_data("./data/")
    spec.load_catalog("catalog.dat")
    fluxes, masks, labels, _ = spec.load_all()
    teff = labels[:, 0]

    # define and preprocess datasets
    ## normalization
    X = torch.tensor(fluxes, dtype=torch.float32)
    y = torch.tensor(teff, dtype=torch.float32)
    y_mean = y.mean(0)
    y_std = y.std(0)
    y = (y - y_mean)/y_std 
    ## shuffling
    perm = torch.randperm(len(spec))
    X = X[perm]
    y = y[perm]
    ## separating the data into traiing and test subsets
    X_train = X[num_test:,:]
    X_test = X[:num_test,:]
    y_train = y[num_test:]
    y_test = y[:num_test]
    
    # dataloader
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # model and parameters
    model = star_net(len(spec.wavelength))
    optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)
    criterion = nn.MSELoss()
    
    # training loop
    train_losses = []
    test_losses = []
    for epoch in range(num_epochs): 
        # training
        model.train()  
        train_loss = 0.0    
        for x, y_true in train_loader:  
            pred = model(x) 
            loss = criterion(pred,y_true)
            optimizer.zero_grad()   
            loss.backward() 
            optimizer.step()    
            train_loss += loss.item()   
        train_loss /= len(train_loader) 

        # evaluation
        model.eval()    
        test_loss = 0.0 
        with torch.no_grad():   
            for x, y_true in test_loader:   
                pred = model(x) 
                loss = criterion(pred,y_true)
                test_loss += loss.item()    
        test_loss /= len(test_loader)   

        print(
            f"Epoch {epoch:3d} | "
            f"Train: {train_loss:.4f} | "
            f"Test: {test_loss:.4f}"
        )
        train_losses.append(train_loss)
        test_losses.append(test_loss)
    
    # check
    model.eval()

    with torch.no_grad():
        pred = model(X)
    
    pred = pred * y_std + y_mean
    truth = y * y_std + y_mean
    
    # output
    np.savetxt(
        "loss_history.txt",
        np.column_stack([range(num_epochs), train_losses, test_losses]),
        header="epochs,train_loss,test_loss",
        comments=""
    )

    is_test = torch.zeros(len(truth),dtype=torch.bool)
    is_test[:num_test] = True
    np.savetxt(
        "prediction.txt",
        torch.stack([
            truth,
            pred,
            is_test
        ], dim=1).numpy(),
        header="truth,prediction,is_test",
        comments=""
    )
    
