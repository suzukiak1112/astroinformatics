import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

if __name__=='__main__':

    # loading data    
    data = np.loadtxt("loss_history.txt",skiprows=1)
    epochs = data[:, 0]
    train_loss = data[:, 1]
    test_loss = data[:, 2]

    # plot
    plt.rcParams['figure.figsize']=[16.0/2.54, 12.0/2.54]
    plt.rcParams['font.size']=14
    gs1 = gridspec.GridSpec(1,1)
    ax = plt.subplot(gs1[0,0])
    ax.plot(epochs, test_loss, dashes=[4,2],color="red",label="test loss")
    ax.plot(epochs, train_loss, "-",color="blue",label="training loss")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_xlim(left=0.0)
    ax.set_ylim(bottom=0.0)
    ax.legend(frameon=False, loc="upper right")
    plt.savefig("loss.pdf", dpi=400)
    plt.show()
