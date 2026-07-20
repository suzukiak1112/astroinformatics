import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import numpy as np
from astropy.io import fits

class miles_data:

    def __init__(self, data_dir):

        self.catalog = []
        self.wavelength = None
        self.data_dir = Path(data_dir)

    def load_catalog(self, catalog_path):
        """
        load catalog.dat
        """

        with open(self.data_dir / catalog_path) as f:

            for line in f:

                filename = line[0:10].strip()
                teff = line[73:78].strip()
                logg = line[79:84].strip()
                feh = line[85:90].strip()

                # skipping inappropriate lines
                if filename == "" or teff == "----" or logg == "----" or feh == "----":
                    continue

                self.catalog.append (
                    {
                        "filename": filename,
                        "teff": float(teff),
                        "logg": float(logg),
                        "feh": float(feh),
                    }
                )


    def load_spectrum(self, filename):
        """
        load a single fits file
        """

        path = self.data_dir / filename

        with fits.open(path) as hdul:
            flux = np.asarray(
                hdul[0].data,
                dtype=np.float64,
            ).squeeze()

            header = hdul[0].header

            wavelength = (
                header["CRVAL1"]
                + header["CDELT1"]
                * np.arange(header["NAXIS1"])
            )

        mask = flux > 0

        return {
            "wavelength": wavelength,
            "flux": flux,
            "mask": mask,
        }
        

    def load_all(self):
        """
        load all spectra in the catalog
        """
        
        if len(self.catalog) == 0:
            raise RuntimeError(
                "Catalog is empty. Call load_catalog() first."
            )

        fluxes = []
        masks = []
        labels = []
        filenames = []

        for obj in self.catalog:

            spec = self.load_spectrum(obj['filename'])

            if self.wavelength is None:
                self.wavelength = spec["wavelength"]

            fluxes.append(spec["flux"])
            masks.append(spec["mask"])

            labels.append(
                [
                    obj["teff"],
                    obj["logg"],
                    obj["feh"],
                ]
            )

            filenames.append(obj['filename'])

        return (
            np.array(fluxes),
            np.array(masks),
            np.array(labels),
            filenames,
        )
 
    def __len__(self):
        return len(self.catalog)
    
    
    def __getitem__(self, idx):

        obj = self.catalog[idx]

        return {
            **obj,
            **self.load_spectrum(obj["filename"]),
        }



