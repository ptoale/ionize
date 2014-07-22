from scipy import interpolate


def load_nightingale(name):
    namedict = {
        'hydrochloric acid': 'Nightingale_Cl_data.txt',
        'sodium': 'Nightingale_Na.txt',
        'potassium': 'Nightingale_K_data.txt',
        'lithium': 'Nightingale_Li_data.txt',
        'magnesium': 'Nightingale_Mg_data.txt',
        'perchloric acid': 'Nightingale_Perchlorate_data.txt',
        'rubidium': 'Nightingale_Rb and Cs _data.txt',
        'cesium': 'Nightingale_Rb and Cs _data.txt',
        'calcium': 'Nightingale_Rb and Cs _data.txt',
        'silver': 'Nightingale_Ag_data.txt',
        'sulfate': 'Nightingale_Sulfate_data.txt'
    }

    if name in namedict:
        temp = []
        state = []
        datafile = open('./STEEP_files/'+namedict[name])
        print datafile.readline()
        for line in datafile:
            entries = line.strip().split(',')
            entries = map(float, entries)
            temp.append(entries[0])
            # state.append(entries[1]*10.35e-21/abs(z)/x(4)*10^10)
            state.append(entries[1])
        statefunc = interpolate.interp1d(temp, state)
        return statefunc
    else:
        return None

if __name__ == "__main__":
    print load_nightingale('silver')(88)
