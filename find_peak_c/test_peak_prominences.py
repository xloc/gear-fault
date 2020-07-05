from scipy.signal._peak_finding import _arg_wlen_as_expected
from ctypes_util import ctypes, np, T


def peak_prominences(x, peaks, wlen: int) -> (
    np.ndarray, np.ndarray, np.ndarray
):
    x_np, x = T.convert_float_array(x)
    peaks_np, peaks = T.convert_int_array(peaks)

    prominences_np, prominences = T.create_float_array(len(peaks_np))
    left_bases_np, left_bases = T.create_int_array(len(peaks_np))
    right_bases_np, right_bases = T.create_int_array(len(peaks_np))

    so = ctypes.CDLL('/Users/oliver/workspace/gear_fault/find_peak_c/find_peak.so')
    so.peak_prominences.argtypes = (
        T.float_p, T.int, T.int_p, T.int, T.int,
        T.float_p, T.int_p, T.int_p
    )
    so.peak_prominences.restype = None

    so.peak_prominences(
        x, len(x_np), peaks, len(peaks_np), wlen,
        prominences, left_bases, right_bases
    )

    # del(so)
    return prominences_np, left_bases_np, right_bases_np


from scipy.misc import electrocardiogram
x = electrocardiogram()[2000:2500]

from scipy.signal import find_peaks
peaks, _ = find_peaks(x, distance=10)

wlen = None
wlen = _arg_wlen_as_expected(wlen)

p, l, r = peak_prominences(x, peaks, wlen)

from scipy.signal._peak_finding_utils \
    import _peak_prominences as scipy_peak_prominences
pp, ll, rr = scipy_peak_prominences(x, peaks, wlen)

# print(l)
# print(ll)
# print()
# print(r)
# print(rr)
print(np.array_equal(l, ll))
print(np.array_equal(r, rr))
print(np.mean(p - pp) < 1e-6)



