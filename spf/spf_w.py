from spf.spf_class import SubChunk, SPF, DataChunk
from os import remove
import struct


def writeSPF(optFile, *args):
    print(optFile)
    with open(optFile, 'wb+') as opt:
        Spf = SPF()
        for subchunk in args:
            Spf.insertChunk(subchunk)

        seekPos = 0
        opt.write(Spf.m_Header.m_ID.encode())
        seekPos += 4
        opt.write(struct.pack('B', Spf.m_Index.m_Num_Ele))
        seekPos += 1
        opt.write(struct.pack(str(Spf.m_Index.m_Num_Ele) + 'Q', *[0] * Spf.m_Index.m_Num_Ele))
        seekPos += 8*Spf.m_Index.m_Num_Ele
        Name_Ele = ''.join(Spf.m_Index.m_Name_Ele).encode()
        opt.write(Name_Ele)
        seekPos += len(Name_Ele)

        for i in range(Spf.m_Index.m_Num_Ele):
            subchunk = Spf.m_Data.m_data[i]
            BitLength = writeSubChunk(subchunk, opt, seekPos)
            opt.seek(5+4*i)
            opt.write(struct.pack('Q', seekPos))
            seekPos += BitLength
            opt.seek(0)


def writeSubChunk(chunk: SubChunk, iostream, seekPos):
    seekPosRaw = seekPos

    iostream.write(struct.pack('I', 0))  ##SubChunk_Length
    seekPos += 4
    iostream.write(struct.pack('I', 0))  ##SubChunk.Index_Length
    seekPos += 4
    iostream.write(struct.pack('I', chunk.m_Index.m_Num_Ele))
    seekPos += 4
    iostream.write(struct.pack(str(chunk.m_Index.m_Num_Ele) + 'I', *[0] * chunk.m_Index.m_Num_Ele))
    seekPos += 4*chunk.m_Index.m_Num_Ele
    Name_Ele = ','.join(chunk.m_Index.m_Name_Ele).encode()
    iostream.write(Name_Ele)
    seekPos += len(Name_Ele)

    for i in range(chunk.m_Index.m_Num_Ele):
        subchunk = chunk.m_Data.m_data[i]
        if subchunk.m_isdata:
            BitLength = writeDataChunk(subchunk, iostream, seekPos)
        else:
            BitLength = writeSubChunk(subchunk, iostream, seekPos)

        iostream.seek(seekPosRaw+12+i*4)
        iostream.write(struct.pack('I', seekPos))
        seekPos += BitLength
        iostream.seek(0, 2)
    iostream.seek(seekPosRaw)
    iostream.write(struct.pack('I', seekPos - seekPosRaw - 4))
    iostream.seek(0, 2)
    return seekPos-seekPosRaw


def writeDataChunk(chunk: DataChunk, iostream, seekPos):
    iostream.write(struct.pack('I', 0))  ##DataChunk_Length

    BitLength = 0
    iostream.write(struct.pack('I', chunk.m_Num))
    BitLength += 4
    iostream.write(struct.pack(str(4*chunk.m_Num) + 'I', *chunk.m_data))
    BitLength += 4 * len(chunk.m_data)

    chunk.m_length = BitLength
    iostream.seek(seekPos)
    iostream.write(struct.pack('I', chunk.m_length))
    iostream.seek(0, 2)

    return BitLength+4


def clear(tmpList):
    for tmp in tmpList:
        remove(tmp)
