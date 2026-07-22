import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import spectral_library

if __name__=='__main__':
    # read data
    spec = spectral_library.miles_data("./data/")
    spec.load_catalog("catalog.dat")
    fluxes, masks, labels, _ = spec.load_all()

    # plot parameters
    plt.rcParams['figure.figsize']=[32.0/2.54, 16.0/2.54]
    gs1 = gridspec.GridSpec(3,4)
    
    # plotting first 12 spectra
    for n in range(12):
        ax = plt.subplot(gs1[n])
        wave = spec.wavelength[masks[n]]
        flux = fluxes[n][masks[n]]
        ax.plot(wave, flux, "-", color="darkblue", linewidth=1.0)
        ax.set_xticks([4000,6000,8000])
        if n >= 8:
            ax.set_xlabel(r"$\lambda\ [\AA]$")
        if n%4 == 0:
            ax.set_ylabel(r"$F_\lambda/F_{5550\AA}$")
        ax.set_ylim(bottom=0.0)
    plt.savefig("miles_spectra.pdf",dpi=400)
    plt.show()


