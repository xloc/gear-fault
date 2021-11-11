from find_peak_c.ctypes_util import ctypes, np, T

def find_peaks(
    x: np.ndarray, distance:float=None, prominence:float=None, wlen:int=None,
) -> np.ndarray:
    x_np, x = T.convert_float_array(x)

    distance = distance if distance is not None else 1
    prominence = prominence if prominence is not None else 0
    wlen = wlen if wlen is not None else -1

    out_peaks_np, out_peaks = T.create_int_array(len(x_np) // 2)
    out_peaks_len = T.int()

    so = ctypes.CDLL('find_peak_c/find_peak.so')
    so.find_peaks.argtypes = (
        T.float_p, T.int, T.float, T.float, T.int,
        T.int_p, T.int_p
    )
    so.find_peaks.restype = None

    so.find_peaks(
        x, len(x_np), distance, prominence, wlen,
        out_peaks, out_peaks_len
    )

    return out_peaks_np[:out_peaks_len.value]