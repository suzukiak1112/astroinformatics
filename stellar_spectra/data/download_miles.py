import urllib.request
import tarfile
from pathlib import Path


#
# spectral library download
#

lib_url = "https://research.iac.es/proyecto/miles/media/tarfiles/Stellar_Libraries/MILES_library_v9.1_FITS.tar.gz"

archive_path = Path("MILES_library_v9.1_FITS.tar.gz")

print(f"Downloading {lib_url} ...")
urllib.request.urlretrieve(lib_url, archive_path)
print(f"Saved to {archive_path}")

print("Extracting...")
with tarfile.open(archive_path, mode="r:gz") as tar:
    tar.extractall(path=".")

print("library downloaded.")


#
# catalog download
#

URL = (
    "https://cdsarc.cds.unistra.fr/"
    "ftp/J/MNRAS/371/703/catalog.dat"
)

path = Path("catalog.dat")

if not path.exists():
    urllib.request.urlretrieve(URL, path)

print("catalog.dat lownloaded.")
