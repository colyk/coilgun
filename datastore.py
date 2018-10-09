import pandas as pd
import numpy
import atexit
from shutil import copyfile

# ==== METHODS


def populate_coils(coils):
    lp = 20
    rp = 4
    lb = numpy.linspace(20, 100, 81)
    rbi = 5
    rbo = numpy.linspace(6, 11, 6)
    temp_id = 0
    phi = 1
    for l in lb:
        for rb in rbo:
            coil = pd.Series([temp_id, lp, rp, l, rbi, rb, 100, False, phi, numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan, numpy.nan],
                             index=['id', 'Lp', 'Rp', 'Lb', 'Rbi', 'Rbo', 'mu', 'mu_approx_valid', 'phi', 'resistance', 'n_points', 'dLz_z', 'dLz', 'L0', 'splinify'])
            coils = coils.append(coil, ignore_index=True)
            temp_id += 1
    return coils


def populate_setups(setups):
    E = 400
    C = 0.0024
    R = 0.07
    setup = pd.Series([0, C, E, R],
                      index=['id', 'C', 'E', 'R'])
    setups = setups.append(setup, ignore_index=True)
    setup = pd.Series([0, C, E / 2, R],
                      index=['id', 'C', 'E', 'R'])
    setups = setups.append(setup, ignore_index=True)
    setup = pd.Series([0, C / 2, E, R],
                      index=['id', 'C', 'E', 'R'])
    setups = setups.append(setup, ignore_index=True)
    return setups


def save_all():
    store.put('coils', coils)


def update_coil(coil):
    print(coil)
    coils.loc[coil.name] = coil


def backup():
    copyfile('store.h5', 'store_backup.h5')

# ==== MAIN


store = pd.HDFStore('store.h5')


# ==== COILS CHECK
if '/coils' not in store.keys():
    print("coils store empty")
    dtypes = {
        'id': 'int64',
        'Lp': float,
        'Rp': float,
        'Lb': float,
        'Rbi': float,
        'Rbo': float,
        'mu': float,
        'phi': float,
        'resistance': float,
        'n_points': float,
        'dLz_z': object,
        'dLz': object,
        'L0': float,
        'mu_points': object,
        'mu_dLz_0': object,
        'mu_approx_valid': bool,
    }

    coils = pd.DataFrame({
        'id': [],
        'Lp': [],
        'Rp': [],
        'Lb': [],
        'Rbi': [],
        'Rbo': [],
        'mu': [],
        'phi': [],
        'mu_approx_valid': [],
        'resistance': [],
        'n_points': [],
        'dLz_z': [],
        'dLz': [],
        'L0': [],
        'mu_points': [],
        'mu_dLz_0': [],
        'mu_approx_valid': bool,
    })

    coils = populate_coils(coils)
    for col, dtype in dtypes.items():
        coils[col] = coils[col].astype(dtype)
    coils.set_index(['id'], inplace=True)
    store.put('coils', coils)


coils = store['coils']

# ==== SETUP CHECK
if '/setups' not in store.keys():
    print("setups store empty")
    dtypes = {
        'id': 'int64',
        'C': float,
        'E': float,
        'R': float,
    }

    setups = pd.DataFrame({
        'id': [],
        'C': [],
        'E': [],
        'R': [],
    })

    setups = populate_setups(setups)
    for setup, dtype in dtypes.items():
        setups[setup] = setups[setup].astype(dtype)
    setups.set_index(['id'], inplace=True)
    store.put('setups', setups)


setups = store['setups']

# ==== EXIT
atexit.register(backup)
atexit.register(store.close)
atexit.register(save_all)
