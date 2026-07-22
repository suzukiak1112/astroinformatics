import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FixedLocator, FixedFormatter

if __name__=='__main__':

    # loading data    
    data = np.loadtxt("prediction.txt",skiprows=1)
    truth = data[:, 0]
    pred = data[:, 1]
    is_test = data[:, 2].astype(bool)
    truth_test = truth[:sum(is_test)]
    truth_train = truth[sum(is_test):]
    pred_test = pred[:sum(is_test)]
    pred_train = pred[sum(is_test):]
    error_test = np.abs(pred_test - truth_test)/truth_test
    error_train = np.abs(pred_train - truth_train)/truth_train
    print(error_test.mean(), error_train.mean())

    # plot
    plt.rcParams['figure.figsize']=[16.0/2.54, 20.0/2.54]
    plt.rcParams['font.size']=14
    gs1 = gridspec.GridSpec(4,1)
    gs1.update(left=0.2,right=0.9,top=0.9,bottom=0.10,wspace=0.1,hspace=0.1)
    ax = plt.subplot(gs1[1:,0], aspect="equal")
    ax1 = plt.subplot(gs1[:1,0])
    ax.plot(np.linspace(1800,50000,100),np.linspace(1800,50000,100),
            "--",color="gray",label="$T_{eff,pred}=T_{eff,true}$")
    ax.scatter(truth_train,pred_train, 
               color="blue", s=3, alpha=0.5, label="training data (N=846)")
    ax.scatter(truth_test,pred_test, 
               color="red", s=8, label="test data (N=100)")
    ax1.scatter(truth_train, np.abs(pred_train-truth_train)/truth_train, 
                color="blue", s=3, label="training data")
    ax1.scatter(truth_test, np.abs(pred_test-truth_test)/truth_test, 
                color="red", s=8, label="test data")
    ax.set_xlabel("$T_{eff,true}\ [K]$")
    ax.set_ylabel("$T_{eff,pred}\ [K]$")
    ax1.set_ylabel("$|\Delta T_{eff}/T_{eff,true}|$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([1800,50000])
    ax.set_ylim([1800,50000])
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim([1500,50000])
    ax1.set_yticks([1.0e-4,1.0e-3,1.0e-2,1.0e-1,1.0])
    ax1.set_ylim([0.5e-4,1.0])
    ax1.set_xticklabels([])
    ax.xaxis.set_major_locator(
        FixedLocator([2000, 5000, 10000, 20000, 50000])
    )
    ax.xaxis.set_major_formatter(
        FixedFormatter([r'$2\times 10^3$', 
                        r'$5\times 10^3$', 
                        r'$10^4$', 
                        r'$2\times10^4$', 
                        r'$5\times10^4$'])
    )
    ax.yaxis.set_major_locator(
        FixedLocator([2000, 5000, 10000, 20000, 50000])
    )
    ax.yaxis.set_major_formatter(
        FixedFormatter([r'$2\times 10^3$', 
                        r'$5\times 10^3$', 
                        r'$10^4$', 
                        r'$2\times10^4$', 
                        r'$5\times10^4$'])
    )
    ax.yaxis.set_label_coords(-0.2, 0.5)
    ax1.yaxis.set_label_coords(-0.2, 0.5)
    ax.legend(frameon=False, loc="upper left")
    plt.savefig("effective_temperature.pdf", dpi=400)
    plt.show()
