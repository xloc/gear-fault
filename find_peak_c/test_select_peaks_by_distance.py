from ctypes_util import ctypes, np, T

def select_by_peak_distance(
    peaks, priority, distance: float
) -> np.ndarray:
    peaks_np, peaks = T.convert_int_array(peaks)
    priority_np, priority = T.convert_float_array(priority)

    keep_np, keep = T.create_bool_array(len(peaks_np))
    keep_np[:] = 1

    so = ctypes.CDLL('find_peak.so')
    so.select_by_peak_distance.argtypes = (
        T.int_p, T.int, T.float_p, T.float,
        T.bool_p
    )
    so.select_by_peak_distance.restype = None

    so.select_by_peak_distance(
        peaks, len(peaks_np), priority, distance,
        keep
    )

    del(so)
    return keep_np


from scipy.misc import electrocardiogram
x = electrocardiogram()[2000:4000]

from scipy.signal._peak_finding_utils import _local_maxima_1d
peaks, _, _ = _local_maxima_1d(x)

distance = 5

keep = select_by_peak_distance(peaks, x[peaks], distance)

from scipy.signal._peak_finding_utils import \
    _select_by_peak_distance as scipy_select_by_peak_distance

keep_groundtrue = scipy_select_by_peak_distance(peaks, x[peaks], distance)
# print(np.argsort(x[peaks]))

print((keep))
print((keep_groundtrue))
print(((keep^keep_groundtrue)))
print(np.count_nonzero(keep))
print(np.count_nonzero(keep_groundtrue))
# print(np.count_nonzero((keep^keep_groundtrue)))
print(x[peaks][(keep^keep_groundtrue)])
assert np.array_equal(keep, keep_groundtrue)


keep[0] ^= keep[0]
try:
    assert np.array_equal(keep, keep_groundtrue)
except AssertionError:
    print('correct')
