from spf.spf_t import Tmp_read
from spf.spf_th import SPFThread, SPFSemaphore
from threading import Semaphore
from spf.spf_class import SubChunk, DataChunk
from multiprocessing import Pool
import numpy as np


def sort_byChunk(Array, Chunk_M=256):
    ret = []
    for i in range(0, len(Array), Chunk_M):
        return 0


def sort_bySite_traversal(attrList: list, retArrayList: list, KeyList_List: list, Size=500):
    FirstKey = 'y'
    SecondKey = 'x'
    FirstKey = attrList.index(FirstKey)
    SecondKey = attrList.index(SecondKey)
    MapKey = 0
    N = len(retArrayList[FirstKey])

    FirstMax = int(np.max(retArrayList[FirstKey])/Size)
    FirstMin = int(np.min(retArrayList[FirstKey])/Size)
    SecondMax = int(np.max(retArrayList[SecondKey])/Size)
    SecondMin = int(np.min(retArrayList[SecondKey])/Size)

    DataDict = {}
    for fst in range(FirstMin, FirstMax+1):
        for sed in range(SecondMin, SecondMax+1):
            SiteKey = str(fst)+'-'+str(sed)
            DataDict[SiteKey] = [[] for i in range(len(attrList))]
    for i in range(N):
        SiteKey = str(int(retArrayList[FirstKey][i]/Size))+'-'+str(int(retArrayList[SecondKey][i]/Size))
        for j in range(len(attrList)):
            DataDict[SiteKey][j].append(retArrayList[j][i])
    ChunkList = []
    for key in DataDict.keys():
        num = len(DataDict[key][MapKey])
        if num > 0:
            chunk = SubChunk()
            chunk.initialiseChunk(key, num, None)
            MapCountDict = {}.fromkeys(range(len(KeyList_List[MapKey])), 0)
            for i in range(num):
                MapCountDict[DataDict[key][MapKey][i]] += 1
            for i in range(num):
                insertData = []
                for j in range(1, len(attrList)):
                    insertData.append(DataDict[key][j][i])
                insertData.append(MapCountDict[DataDict[key][MapKey][i]])
                chunk.insertData(key, insertData)
            ChunkList.append(chunk)
    return ChunkList


def sort_bySite_multiprocess(attrList: list, retArrayList: list, keyList_List, Size=500, n_Pool=4):
    YKey = 'y'
    XKey = 'x'
    GeneKey = 'geneid'
    VKey = 'umicount'

    YKey = attrList.index(YKey)
    XKey = attrList.index(XKey)
    GeneKey = attrList.index(GeneKey)
    VKey = attrList.index(VKey)

    N = len(retArrayList[YKey])
    ArgSortY = retArrayList[YKey].argsort()
    for i in range(len(attrList)):
        retArrayList[i] = retArrayList[i][ArgSortY]
    Ymin = np.min(retArrayList[YKey])

    partIdx = int(Ymin/Size)
    left = 0
    pool = Pool(n_Pool)
    queue = []
    for i in range(N):
        now_partIdx = int(retArrayList[YKey][i]/Size)
        if now_partIdx > partIdx:
            p = pool.apply_async(sort_bySite_single, args=(partIdx, Size, retArrayList[GeneKey][left:i],
                                                           retArrayList[XKey][left:i], retArrayList[YKey][left:i],
                                                           retArrayList[VKey][left:i]))
            queue.append(p)
            left = i
            partIdx = now_partIdx
        if i == N-1:
            p = pool.apply_async(sort_bySite_single, args=(now_partIdx, Size, retArrayList[GeneKey][left:],
                                                           retArrayList[XKey][left:], retArrayList[YKey][left:],
                                                           retArrayList[VKey][left:]))
            queue.append(p)
    pool.close()
    pool.join()

    chunkTotal = SubChunk()
    chunkTotal.initialiseChunk('S', MapTable=keyList_List[GeneKey])
    for p in queue:
        subchunk = p.get()
        chunkTotal.insertData(subchunk.m_Header.m_ID, subchunk)
    return chunkTotal


def sort_bySite_single(key_Y, Size, *args):
    dataDict = {}
    geneCountDict = {}
    for i in range(len(args[0])):
        key = str(key_Y)+'-'+str(int(args[1][i]/Size))
        geneCountKey = key+str(args[0][i])
        if key not in dataDict:
            dataDict[key] = []
        if geneCountKey not in geneCountDict:
            geneCountDict[geneCountKey] = 0
        dataDict[key].append(args[1][i])
        dataDict[key].append(args[2][i])
        dataDict[key].append(args[3][i])
        dataDict[key].append(args[0][i])
        geneCountDict[geneCountKey] += 1
    for key in dataDict.keys():
        for i in range(0, len(dataDict[key]), 4):
            j = i + 3
            dataDict[key][j] = geneCountDict[key+str(dataDict[key][j])]
    subchunk = SubChunk()
    subchunk.initialiseChunk(str(key_Y))
    for key in dataDict.keys():
        chunk = DataChunk()
        chunk.insertData(int(len(dataDict[key])/4), dataDict[key])
        subchunk.insertData(key, chunk)
    return subchunk


def sort_byPrimeKey(PrimeKeyIdx: int, retArrayList: list):
    PrimeArray = retArrayList[PrimeKeyIdx]
    PrimeArgsort = PrimeArray.argsort()
    for i in range(len(retArrayList)):
        retArrayList[i] = retArrayList[i][PrimeArgsort]


def sort_byTree(PrimeKeyIdx, retArrayList, PrimeKeyRange=1, Chunk_M=256):
    return 0

