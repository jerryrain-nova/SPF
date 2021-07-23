from spf.spf_class import SPF, SubChunk


def index_simple(il, num):
    num = num
    index = []
    res = []
    last = 0
    for i in range(len(il)):
        if i % num == 0:
            index.append(il[i])
            if i != 0:
                res.append(il[last:i])
                last = i
    res.append(il[last:])
    return index, res


if __name__ == '__main__':
    a = list(range(10000))
    a_index, a = index_simple(a, 100)
    index = []
    for i in range(len(a)):
        i_index, i_data = index_simple(a[i], 10)
        index.append(i_index)
        a[i] = i_data
    print(a)
    Spf = SPF()
    Spf.updateHeader('N')

    Chunk = SubChunk()
    Chunk.m_Header.updateHeader('test')
    for i in range(len(a)):
        Chunk.m_Index.updateIndex(a_index[i])
        subChunk = Chunk()
        subChunk.m_Header.updateHeader(a_index[i])
        subChunk.m_Index.updateIndex(index[i])
        for j in range(len(a[i])):
            subChunk.m_Data.updateData(a[i][j])
        Chunk.m_Data.updateData(subChunk)
    Spf.ChunktoSPF(Chunk)
    print(Chunk)
    print(Spf)
    print(Spf.m_Index)
    print(Spf.m_Data.m_data[0])
