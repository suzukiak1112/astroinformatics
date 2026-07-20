data = []

def read(filename):
    with open(filename, "r") as f:

        for line in f:

            filename = line[0:10].strip()
            teff = line[73:78].strip()
            logg = line[79:84].strip()
            feh = line[85:90].strip()

            # skipping inappropriate lines
            if filename == "" or teff == "----" or logg == "----" or feh == "----":
                continue

            data.append(
                {
                    "filename": filename,
                    "teff": float(teff),
                    "logg": float(logg),
                    "feh": float(feh),
                }
            )

if __name__=='__main__':
    # read catalog
    read("./data/catalog.dat")
    
    # showing first 10 objects
    for n in range(10):
        print(data[n]['filename'])
