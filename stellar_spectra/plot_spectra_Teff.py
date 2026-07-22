import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import spectral_library


class_list = [
    {"spec_type": "M", "teff_min": 0,    "teff_max": 3700},
    {"spec_type": "K", "teff_min": 3700, "teff_max": 4200},
    {"spec_type": "K", "teff_min": 4200, "teff_max": 4500},
    {"spec_type": "K", "teff_min": 4500, "teff_max": 4700},
    {"spec_type": "K", "teff_min": 4700, "teff_max": 5000},
    {"spec_type": "K", "teff_min": 5000, "teff_max": 5200},
    {"spec_type": "G", "teff_min": 5200, "teff_max": 5600},
    {"spec_type": "G", "teff_min": 5600, "teff_max": 6000},
    {"spec_type": "F", "teff_min": 6000, "teff_max": 6500},
    {"spec_type": "F", "teff_min": 6500, "teff_max": 7500},
    {"spec_type": "A", "teff_min": 7500, "teff_max": 10000},
    {"spec_type": "OB", "teff_min": 10000, "teff_max": 100000},
]


if __name__=='__main__':
    # read data
    spec = spectral_library.miles_data("./data/")
    spec.load_catalog("catalog.dat")
    fluxes, masks, labels, _ = spec.load_all()
    
    # ordering according to Teff
    teffs = labels[:,0]
    sorted_teff = np.argsort(teffs)
    rank = np.empty(len(spec), dtype=int)
    rank[sorted_teff] = np.arange(len(spec))
    norm = Normalize(vmin=3000, vmax=10000)
    print(np.max(teffs),np.min(teffs))


    # plot
    plt.rcParams['figure.figsize']=[24/2.54, 20.0/2.54]
    fig=plt.figure()
    gs1 = gridspec.GridSpec(4,15+1)
    axs=[]
    for n in range(len(class_list)):
        ax=plt.subplot(gs1[(int)((len(class_list)-n-1)/3),5*(n%3):5*(n%3)+5])  
        axs.append(ax)
    for n in range(len(class_list)):
        indices = np.where((teffs >= class_list[n]["teff_min"])&\
                            (teffs < class_list[n]["teff_max"]))[0]
        for idx in indices:
            wave = spec.wavelength[masks[idx]]
            flux = fluxes[idx][masks[idx]]
            axs[n].plot(wave,flux,
                        color=plt.cm.plasma_r(norm(teffs[idx])),
                        linewidth=0.5,alpha=0.2)
        axs[n].set_yscale("log")
        axs[n].set_ylim([1.0e-1,20.0])
        axs[n].set_xlim([3500.0,7420.94])
        axs[n].set_xticks([4000,5000,6000,7000])
        if n%3>0: axs[n].set_yticklabels([])
        else: axs[n].set_ylabel(r"$F_\lambda/F_{5440}$")
        if n>2: axs[n].set_xticklabels([])
        else: axs[n].set_xlabel(r"$\lambda[\AA]$")
        axs[n].annotate(str(class_list[n]["teff_min"])+"$\leq T_{eff}<$"
                        +str(class_list[n]["teff_max"])+"\n"
                        +class_list[n]["spec_type"]
                        +r" star, $N="+str(len(indices))+r"$",
                        xy=(0.05,0.97),xycoords="axes fraction",fontsize=12,
                        verticalalignment="top",horizontalalignment="left")
    # colorbar
    cax = plt.subplot(gs1[:,15])
    sm = ScalarMappable(
        norm=norm,
        cmap="plasma_r"
    )
    cbar = fig.colorbar(
        sm,
        cax=cax,
        fraction=0.03,
        pad=0.04
    )
    cbar.set_ticks([3000,4000,5000,6000,7000,8000,9000,10000])
    cbar.set_ticklabels([3000,4000,5000,6000,7000,8000,9000,10000])
    cax.set_title(r"$T_{eff}[K]$")
    plt.savefig("miles_spectra_Teff.png",dpi=400)
    plt.show()


