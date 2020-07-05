from ctypes_util import T
import numpy as np
import ctypes


so = ctypes.CDLL('find_peak.so')

from scipy.misc import electrocardiogram
x_np = electrocardiogram()[2000:2500]
x_np, x = T.convert_float_array(x_np)

print(x_np[:10])
xn = len(x_np)

mid_np, mid = T.create_int_array(xn)
left_np, left = T.create_int_array(xn)
right_np, right = T.create_int_array(xn)
m = T.int()

so.local_maxima.argtypes = \
    T.float_p, T.int,\
    T.int_p, T.int_p, T.int_p, T.int_p
so.local_maxima.restype = None

so.local_maxima(
    x, xn, 
    mid, left, right, m
)

print(m)
mid_np = mid_np[:m.value]
print(mid_np)