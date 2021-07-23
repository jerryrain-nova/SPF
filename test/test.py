# import sys
# sys.path.append(r"/mnt/e/Python_Project/SPF/")
from os import remove
from spf.spf_l import *
from spf.spf_t import *
from spf.spf_s import *
from spf.spf_r import *
from spf.spf_w import *


def main():
    st = time()

    file = 'C:/Users/chenyujie/Desktop/Test/new_spatial_1w.txt'
    # file = '/mnt/c/Users/chenyujie/Desktop/Test/new_spatial_1kw.txt'
    # file = 'C:/Users/chenyujie/Desktop/Test/Cell_sample_1M.txt'
    attr_isint = [False, True, True, True]
    # attr_isint = [False, True, True, True, True]
    PrimeKey = 'geneID'

    N, attrList, tmpList = load_rawData(file)
    print("load time = ", time()-st, 's')

    PrimeKeyIdx = find_PrimeKeyIdx(PrimeKey, attrList)
    retArrayList, KeyList_List = readAllTmps(N, tmpList, attr_isint, 4)
    # sort_byPrimeKey(PrimeKeyIdx, retArrayList)
    # sort_bySite_traversal(attrList, retArrayList, KeyList_List)
    ChunkTotal = sort_bySite_multiprocess(attrList, retArrayList, KeyList_List, 500, 4)
    print("run time = ", time()-st, 's')

    optFile = SPFName(file, optPath='C:/Users/chenyujie/Desktop/Test')
    writeSPF(optFile, ChunkTotal)
    clear(tmpList)


if __name__ == '__main__':
    main()
