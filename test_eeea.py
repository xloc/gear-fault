from ctypes_util import T, ctypes, np
from typing import List

def eeea(wave, 
        fs: float = 12800, ts: float = 0.005, n_peak: int = 5, n_loop: int = 20
    ) -> List[float]:
    
    wave_np, wave = T.convert_float_array(wave)
    evlp_np, evlp = T.create_float_array(len(wave_np))

    so = ctypes.CDLL('eeea_c/eeea.so')
    so.eeea.argtypes = (
        T.float_p, T.int, T.float, T.float, T.int, T.int,
        T.float_p
    )
    so.eeea.restype = None

    so.eeea(wave, len(wave_np), fs, ts, n_peak, n_loop,    evlp)

    return evlp_np

samples = np.load('samples.npz')
w = samples.files[0]
w = samples[w]
print(type(w))
e = eeea(w, ts=0.008, fs=12800)

import eeea
f = eeea.eeea(w, ts=0.008, fs=12800)

import matplotlib.pyplot as plt
plt.plot(e)
plt.plot(f)
plt.savefig('a.png')
