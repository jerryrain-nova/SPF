import gzip
from spf.spf_t import *
from utils.common import *
from time import time


def load_rawData(file: str, n_loop: int = 32):
    """
    FUNCITON: Split rawData to n[n=n_dimensions] tmp_files
    :param file: rawData filename
    :param n_loop: loop of circle to opt
    :return: 3 results: N, attrList, tmpList
    """
    N = 0
    if '.gz' in file:
        f = gzip.open(file, 'rt')
    else:
        f = open(file, 'r')
    header = f.readline()
    while header:
        if '#' in header:
            header = f.readline()
        else:
            break
    attrList = header.strip().split('\t')
    strListLower(attrList)

    tmpList = Tmp_make(file, attrList)
    iostream = Tmp_open(tmpList)
    infoList = None
    now_loop = 0

    point = f.readline()
    while point:
        infoList_insert = point.strip().split('\t')
        if now_loop == 0:
            infoList = infoList_insert
            infoList_update(infoList)
        else:
            infoList_update(infoList, infoList_insert)
        now_loop += 1
        if now_loop == n_loop:
            Tmp_write(iostream, infoList)
            now_loop = 0
        N += 1
        point = f.readline()
        if not point and now_loop != 0:
            Tmp_write(iostream, infoList)
    f.close()
    Tmp_close(iostream)
    return N, attrList, tmpList

