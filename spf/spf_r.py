from spf.spf_class import SPF, SubChunk
from spf.spf_th import SPFThread, SPFSemaphore
from spf.spf_t import Tmp_read
from multiprocessing import process, Pool


def readAllTmps(N, tmpList, attr_isint, n_Pool=4):
    retArrayList = []
    keyList_List = []
    pool = Pool(n_Pool)
    queue = []
    for i in range(len(tmpList)):
        p = pool.apply_async(Tmp_read, args=(tmpList[i], attr_isint[i], N))
        queue.append(p)
    pool.close()
    pool.join()
    for i in queue:
        resArray, keyList = i.get()
        retArrayList.append(resArray)
        keyList_List.append(keyList)
    return retArrayList, keyList_List


