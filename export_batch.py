class Config:
    database_path = '/Users/oliver/Desktop/rtms_software/db/hmscs.db'


import sqlite3

conn = sqlite3.connect(Config.database_path)

cq = conn.cursor()

cq.execute('''
    select HistoryWaveId, DataLength, SampleFreq, SampleTime, WaveData
    from T_HistoryWave where HistoryWaveId >= 209
    '''
)
import bz2 as z
import array

def ez(n):
    if n >= 1e6:
        return f'{n/1e6:.1f}M'
    if n >= 1e3:
        return f'{n/1e3:.1f}k'

for historywaveid, datalength, samplefreq, sampletime, bdata in cq.fetchall():
    bdata = z.decompress(bdata)
    farr = array.array('f')
    farr.frombytes(bdata)

    fname = f"{historywaveid}_{ez(samplefreq)}Hz_{ez(datalength)}pts_{sampletime}.csv"
    with open(fname, 'w') as f:
        for point in farr:
            f.write('%f\n' % point)