#encoding=utf-8
'''
用numpy验证一次N点长FFT计算两个实序列的FFT
'''
import numpy as np
from pprint import pprint
from numpy.fft import fft
x = [0,1,2,3,4,5,6,7]
y = [4,2,3,4,5,8,2,6]
z = x + 1j*np.array(y)
V = fft(z).tolist()
V.extend(fft(z).tolist())
Vy = np.zeros(8,dtype=np.complex)
for i in range(8):
    Vy[i] = (V[i] - V[8-i].conjugate())/(2j)
    # Vy[i] = (V[8-i] - V[i].conjugate())/(2j)
pprint(Vy)
pprint(fft(np.array(y)))
