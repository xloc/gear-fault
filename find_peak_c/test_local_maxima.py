from ctypes_util import T, np, ctypes

ctypes.CDLL('/Users/oliver/workspace/gear_fault/find_peak_c/find_peak.so')

def local_maxima(x):
    x_np, x = T.convert_float_array(x)
    xn = len(x_np)

    mid_np, mid = T.create_int_array(xn)
    left_np, left = T.create_int_array(xn)
    right_np, right = T.create_int_array(xn)
    m = T.int()

    so = ctypes.CDLL('find_peak.so')
    so.local_maxima.argtypes = (
        T.float_p, T.int,
        T.int_p, T.int_p, T.int_p, T.int_p,
    )
    so.local_maxima.restype = None

    so.local_maxima(
        x, xn, 
        mid, left, right, m
    )
    m = m.value

    return mid_np[:m], left_np[:m], right_np[:m], 

from scipy.misc import electrocardiogram
x = electrocardiogram()[2000:2500]

m,l,r = local_maxima(x)

from scipy.signal._peak_finding_utils import _local_maxima_1d as scipy_local_maxima
mm, ll, rr = scipy_local_maxima(x)

assert np.array_equal(m, mm)
assert np.array_equal(l, ll)
assert np.array_equal(r, rr)