import ctypes
from ctypes import POINTER
import numpy as np

class T:
    @staticmethod
    def create_int_array(size):
        a = np.zeros(size, dtype=np.int32)
        a_ctype = a.ctypes.data_as(POINTER(ctypes.c_int))
        return a, a_ctype
    
    @staticmethod
    def create_float_array(size):
        a = np.zeros(size, dtype=np.float32)
        a_ctype = a.ctypes.data_as(POINTER(ctypes.c_float))
        return a, a_ctype

    @staticmethod
    def create_bool_array(size):
        a = np.zeros(size, dtype=np.bool)
        a_ctype = a.ctypes.data_as((POINTER(ctypes.c_bool)))
        return a, a_ctype

    @staticmethod
    def convert_int_array(a):
        a = np.array(a, dtype=np.int32)
        return a, a.ctypes.data_as(POINTER(ctypes.c_int))

    @staticmethod
    def convert_float_array(a):
        a = np.array(a, dtype=np.float32)
        return a, a.ctypes.data_as(POINTER(ctypes.c_float))

    int = ctypes.c_int
    int_p = POINTER(ctypes.c_int)

    float = ctypes.c_float
    float_p = POINTER(ctypes.c_float)

    bool = ctypes.c_bool
    bool_p = POINTER(ctypes.c_bool)