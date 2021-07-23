from re import search, IGNORECASE


def make_scalaDict(num: int, scalaList: list) -> dict:
    """
    FUNCTION: trans scalaList into scalaDict
    :param num: number of scala
    :param scalaList: scalaList
    :return: scalaDict
    """
    scalaDict = {}
    for i in range(num):
        scalaDict[i] = scalaList[i]
    return scalaDict


def infoList_update(infoList: list, infoList_insert: list = None) -> list:
    """
    FUNCTION:Merge 2 infoList in 1 infoList (use in Tmp_write)
    :param infoList:raw_infoList
    :param infoList_insert:infoList to insert
    :return:new_infoList
    """
    if not infoList_insert:
        for i in range(len(infoList)):
            infoList[i] += '\n'
    else:
        for i in range(len(infoList_insert)):
            infoList[i] += infoList_insert[i] + '\n'


def strListLower(strList):
    for i in range(len(strList)):
        strList[i] = strList[i].lower()


def find_PrimeKeyIdx(PrimeKey, attrList):
    PrimeKey = PrimeKey.lower()
    return attrList.index(PrimeKey)


def SPFName(file, optPath):
    prefix = file.split('/')[-1].split('.')[0]
    Name = optPath + '/' + prefix + '.SPF'
    return Name
