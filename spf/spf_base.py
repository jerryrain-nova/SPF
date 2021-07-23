from utils.common import make_scalaDict


class HeaderBase:
    """
    Class HeaderBase
    """
    def __init__(self):
        self.m_ID = ''
        self.m_Length_Chunk = 0

    def __str__(self):
        return "Chunk['%s'] Info:\n  Header:\n\t  BitLength = %d" % (self.m_ID, self.m_Length_Chunk)

    def updateHeader(self, ID):
        self.m_ID = ID

    def print_scalaDict(self) -> None:
        print(make_scalaDict(len(self.__dict__), list(self.__dict__)))


class IndexBase:
    """
    Class IndexBase
    """
    def __init__(self):
        self.m_Length = 0
        self.m_Num_Ele = 0
        self.m_Name_Ele = []
        self.m_First_Ptr = []

    def __str__(self):
        return f'  Index: \n\t  Num_Ele = {self.m_Num_Ele}\n\t  Name_Ele = {self.m_Name_Ele}\n\t  ' \
               f'BitLength = {self.m_Length}\n\t  First_Ptr = {self.m_First_Ptr}'

    def updateIndex(self, N, EleIdxList):
        self.m_Num_Ele += N
        self.m_Name_Ele.append(EleIdxList)

    def insertIndex(self, EleIdx):
        self.m_Num_Ele += 1
        self.m_Name_Ele.append(EleIdx)


class DataBase:
    """
    Class DataBase
    """
    def __init__(self):
        self.m_Length = 0
        self.m_data = []

    def __str__(self):
        return f'  Data:\n\t  Data = {self.m_data}\n\t  BitLength = {self.m_Length}'

    def updateData(self, infoData):
        self.m_data.append(infoData)







