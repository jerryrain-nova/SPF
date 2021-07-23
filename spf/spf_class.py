from spf.spf_base import *
import struct


class SubChunk:
    """
    Class Chunk
    """
    def __init__(self):
        self.m_Header = HeaderBase()
        self.m_Index = IndexBase()
        self.m_Data = DataBase()
        self.m_isdata = False
        self.m_MapTable = None
        self.m_CodeBit = 32
        self.m_Chunk_M = 256

    def __str__(self):
        print(self.m_Header)
        print(self.m_Index)
        print(self.m_Data)
        interval = '-'*20+'\n'*2
        return interval

    def initialiseChunk(self, ID, MapTable=None, CodeBit=32):
        self.m_Header.updateHeader(ID)
        self.m_MapTable = MapTable
        self.m_CodeBit = CodeBit

    def updateIndex(self, N, EleIdxList):
        self.m_Index.updateIndex(N, EleIdxList)

    def insertData(self, index, infoData):
        self.m_Index.insertIndex(index)
        self.m_Data.updateData(infoData)

    def writeIndex(self, iostream):
        iostream.write(struct.pack('I', self.m_Index.m_Length))


class DataChunk:
    def __init__(self):
        self.m_isdata = True
        self.m_last = True
        self.m_length = 0
        self.m_Num = 0
        self.m_data = None

    def insertData(self, N, infoData: list):
        self.m_Num += N
        if not self.m_data:
            self.m_data = infoData
        else:
            self.m_data.extend(infoData)


class SPFHeader(HeaderBase):
    def __init__(self):
        super(SPFHeader, self).__init__()
        self.m_ID = 'SPF#'


class SPFIndex(IndexBase):
    def __init__(self):
        super(SPFIndex, self).__init__()


class SPFData(DataBase):
    def __init__(self):
        super(SPFData, self).__init__()


class SPF:
    def __init__(self):
        self.m_Header = SPFHeader()
        self.m_Index = SPFIndex()
        self.m_Data = SPFData()

    def __str__(self):
        return f'SPF:\n  Info:\n\t  ID = {self.m_Header.m_ID}\n\t  BitLength = {self.m_Header.m_Length_Chunk}'

    def insertDim(self, chunk: SubChunk):
        self.m_Header.updateHeader(chunk.m_Header.m_ID)
        self.m_Index.insertIndex(chunk.m_Header.m_ID)
        self.m_Data.updateData(chunk)

    def insertChunk(self, chunk: SubChunk):
        self.m_Index.insertIndex(chunk.m_Header.m_ID)
        self.m_Data.updateData(chunk)

    def writeHeader(self, iostream):
        iostream.write(self.m_Header.m_ID.encode())
        # iostream.write(struct.pack('Q', self.m_Header.m_Length_Chunk))

    def writeIndex(self, iostream):
        iostream.write(struct.pack('B', self.m_Index.m_Num_Ele))
        iostream.write((''.join(self.m_Index.m_Name_Ele)).encode())
        iostream.write(struct.pack(str(self.m_Index.m_Num_Ele)+'I', *[0]*self.m_Index.m_Num_Ele))

