import struct
from spf.spf_re import *


def main():
    file = 'C:/Users/chenyujie/Desktop/Test/new_spatial_1w.SPF'
    with open(file, 'rb') as ipt:
        DimPtr = searchDim(ipt, 'S')
        Data = searchData(ipt, DimPtr, '11-11')


if __name__ == '__main__':
    main()