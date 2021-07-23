import struct


def searchDim(iostream, tDim):
    identify = iostream.read(4).decode()
    if identify != 'SPF#':
        print("Not SPF File")
        quit()
    N_Dim = struct.unpack('B', iostream.read(1))[0]
    DimList = iostream.read(8*N_Dim)
    DimNameList = iostream.read(N_Dim).decode()
    tDim = DimNameList.index(tDim)
    DimPtr = struct.unpack('Q', DimList[8*tDim:8*tDim+8])[0]
    return DimPtr


def searchData(iostream, DimPtr, key):
    iostream.seek(DimPtr)
