import ctypes

so = ctypes.CDLL('find_peak.so')

from scipy.misc import electrocardiogram
import numpy as np


x_np: np.ndarray = electrocardiogram()[2000:2500]
x_np = x_np.astype(np.float32)
c_float_p = ctypes.POINTER(ctypes.c_float)

x = x_np.ctypes.data_as(c_float_p)
xn = len(x_np)

t = ctypes.c_int
mid, left, right = (t*xn)(), (t*xn)(), (t*xn)()
m = ctypes.c_int()

mid_np = np.zeros(xn, dtype=np.int32)
mid = mid_np.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

so.local_maxima.argtypes = \
    ctypes.POINTER(ctypes.c_float), ctypes.c_int,\
    ctypes.POINTER(t), ctypes.POINTER(t), ctypes.POINTER(t), ctypes.POINTER(t)

so.local_maxima.restype = None

so.local_maxima(
    x, xn, 
    mid, left, right, m
)

print(m)
# mid = list(mid)[:m.value]
print(mid_np[:m.value])