'''
Basic parameters for GOOSE that set the boundaries of possible sequences to make.
Can change parameters here and it will change paramters in GOOSE globally
'''

MINIMUM_LENGTH = 10
MAXIMUM_LENGTH = 10000
MINIMUM_FCR = 0
MAXIMUM_FCR = 1
MINIMUM_NCPR = -1
MAXIMUM_NCPR = 1
MINIMUM_HYDRO = 0
MAXIMUM_HYDRO = 6.1
MINIMUM_HYDRO_CHARGED = 0
MAXIMUM_HYDRO_CHARGED = 5.8
MAXIMUM_SIGMA = 1
MINIMUM_SIGMA = 0

# Empirically determined fcr threhsholds based on hydro values
#MAXIMUM_CHARGE_WITH_HYDRO_1 = 1.1907 + (-0.2050 * mean_hydro)
#MAXIMUM_CHARGE_WITH_HYDRO_2 = 1.2756 + (-0.2289 * mean_hydro)

DISORDER_THRESHOLD = 0.6

HYDRO_ERROR = 0.05

MAXIMUM_DISORDER = 1.0
MINIMUM_DISORDER = 0

# maximums for fractions of amino acids
MAX_FRACTION_A = 0.9
MAX_FRACTION_R = 1.0
MAX_FRACTION_N = 1.0
MAX_FRACTION_D = 1.0
MAX_FRACTION_C = 0.16
MAX_FRACTION_Q = 0.72
MAX_FRACTION_E = 1.0
MAX_FRACTION_G = 1.0
MAX_FRACTION_H = 1.0
MAX_FRACTION_I = 0.2
MAX_FRACTION_L = 0.26
MAX_FRACTION_K = 1.0
MAX_FRACTION_M = 0.26
MAX_FRACTION_F = 0.18
MAX_FRACTION_P = 0.94
MAX_FRACTION_S = 0.88
MAX_FRACTION_T = 0.76
MAX_FRACTION_W = 0.22
MAX_FRACTION_Y = 0.22
MAX_FRACTION_V = 0.3


# dict of max fractions
MAX_FRACTION_DICT = {'A' : MAX_FRACTION_A, 'R' : MAX_FRACTION_R, 'N' : MAX_FRACTION_N, 'D' : MAX_FRACTION_D, 'C' : MAX_FRACTION_C, 'Q' : MAX_FRACTION_Q, 'E' : MAX_FRACTION_E, 'G' : MAX_FRACTION_G, 'H' : MAX_FRACTION_H, 'I' : MAX_FRACTION_I, 'L' : MAX_FRACTION_L, 'K' : MAX_FRACTION_K, 'M' : MAX_FRACTION_M, 'F' : MAX_FRACTION_F, 'P' : MAX_FRACTION_P, 'S' : MAX_FRACTION_S, 'T' : MAX_FRACTION_T, 'W' : MAX_FRACTION_W, 'Y' : MAX_FRACTION_Y, 'V' : MAX_FRACTION_V}

