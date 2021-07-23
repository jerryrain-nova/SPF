from os import remove
import numpy as np
from threading import Semaphore


def Tmp_make(filename: str, attrList: list) -> list:
    """
    FUNCTION: create tmpFile_name List
    :param filename: rawData filename
    :param attrList: Dimensions List
    :return: tmpFile_name List
    """
    prefix = filename.split('.')[:-1]
    prefix = '.'.join(prefix)
    tmpList = []
    for attr in attrList:
        tmpList.append(prefix + '.' + attr + '_tmp')
    return tmpList


def Tmp_remove(tmpList: list) -> True:
    """
    FUNCTION: remove ALL tmpFiles
    :param tmpList: tmpFile List
    :return: True
    """
    for tmp in tmpList:
        remove(tmp)


def Tmp_open(tmpList: list) -> list:
    """
    FUNCTION: open ALL tmpFiles in IOStream_List
    :param tmpList: tmpFile List
    :return: IOStream List
    """
    iostream = []
    for tmp in tmpList:
        iostream.append(open(tmp, 'w'))
    return iostream


def Tmp_close(iosteam: list) -> True:
    """
    FUNCTION: close ALL tmpFile in OPEN
    :param iosteam: IOStream List
    :return: True
    """
    for tmp_io in iosteam:
        tmp_io.close()


def Tmp_write(tmpIO_List: list, infoList: list) -> True:
    """
    FUNCTION: write context in ALL tmpFile
    :param tmpIO_List: IOStream List
    :param infoList: context List
    :return: True
    """
    for i in range(len(infoList)):
        tmpIO_List[i].write(infoList[i])


# def Tmp_read_int(tmp_Int, num: int, bit: int = 32, Lock: Semaphore = None):
#     """
#     FUNCTION: read tmpFile context to numpy.array
#     :param tmp_Int: tmpFile path
#     :param num: number of lines in tmpFile
#     :param bit: code bit
#     :param Lock: Lock [multiThreading], default = None
#     :return: tmpData in np.array
#     """
#     nptypeDict = {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}
#     tmpIO = open(tmp_Int, 'r')
#     ret = np.zeros(num).astype(nptypeDict[bit])
#     i = 0
#     infoLine = tmpIO.readline()
#     while infoLine:
#         ret[i] = int(infoLine.strip())
#         i += 1
#         infoLine = tmpIO.readline()
#     tmpIO.close()
#     if Lock:
#         Lock.release()
#     return ret, None
#
#
# def Tmp_read_str(tmp_Str, num: int, bit: int = 32, Lock: Semaphore = None):
#     nptypeDict = {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}
#     tmpIO = open(tmp_Str, 'r')
#     ret = np.zeros(num).astype(nptypeDict[bit])
#     mapTable = {}
#     i = 0
#     value = 0
#     infoLine = tmpIO.readline()
#     while infoLine:
#         key = infoLine.strip()
#         if key not in mapTable:
#             mapTable[key] = value
#             value += 1
#         ret[i] = mapTable[key]
#         i += 1
#         infoLine = tmpIO.readline()
#     tmpIO.close()
#     if Lock:
#         Lock.release()
#     keyList = list(mapTable.keys())
#     return ret, keyList


def Tmp_read(tmp, isint, N, bit=32, Lock: Semaphore = None):
    nptypeDict = {8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64}
    keyList = None
    MapTable = None
    value = None
    if not isint:
        MapTable = {}
        value = 0
    retArray = np.zeros(N).astype(nptypeDict[bit])
    i = 0
    with open(tmp, 'r') as ipt:
        infoLine = ipt.readline()
        while infoLine:
            infoLine = infoLine.strip()
            if isint:
                retArray[i] = int(infoLine)
            else:
                if infoLine not in MapTable:
                    MapTable[infoLine] = value
                    value += 1
                retArray[i] = MapTable[infoLine]
            i += 1
            infoLine = ipt.readline()
    if Lock:
        Lock.release()
    if not isint:
        keyList = list(MapTable.keys())
    return retArray, keyList
