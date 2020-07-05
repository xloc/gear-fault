class Config:
    table_field_widths = [13, 10, 10, 10]

    database_path = '/Users/oliver/Desktop/rtms_software/db/hmscs.db'

    ylim = None
    ylim = 15

    inspect = True
    # interactive = True

    # history_id = 212
    # history_id = 282

import sqlite3

conn = sqlite3.connect(Config.database_path)

if hasattr(Config, 'inspect') and Config.inspect == True:
    cq = conn.cursor()
    cq.execute('''
        select HistoryWaveId, DataLength, SampleFreq, SampleTime
        from T_HistoryWave 
        order by SampleTime desc
        limit 50
        '''
    )

    cols =  'HistoryWaveId DataLength SampleFreq SampleTime'.split()

    print('%{}s %{}s %{}s %{}s'.format(*Config.table_field_widths) % tuple(cols))
    
    for row in cq.fetchall():
        # print([type(i) for i in row])
        print('%{}d %{}d %{}.0f %{}s'.format(*Config.table_field_widths) % tuple(row))

    
if hasattr(Config, 'interactive') and Config.interactive == True:
    print('(Enter to confirm, Ctrl-C to exit)')
    i = input('History Wave Id = ')
    Config.history_id = int(i)

c = conn.cursor()
c.execute('''
    select DataLength, SampleFreq, SampleTime, WaveData 
    from T_HistoryWave 
    where HistoryWaveId=?
    ''', (str(Config.history_id),)
)

datalength, samplefreq, sampletime, bdata = c.fetchone()
print(len(bdata))


import bz2 as z
bdata = z.decompress(bdata)

print(len(bdata))
import array

farr = array.array('f')
farr.frombytes(bdata)

def ez(n):
    if n >= 1e6:
        return f'{n/1e6:.1f}M'
    if n >= 1e3:
        return f'{n/1e3:.1f}k'

fname = f"{Config.history_id}_{ez(samplefreq)}Hz_{ez(datalength)}pts_{sampletime}.csv"
with open(fname, 'w') as f:
    for point in farr:
        f.write('%f\n' % point)

# print(farr[:10])

import matplotlib.pyplot as plt

plt.plot(farr)
plt.grid(True)
if Config.ylim is not None:
    yy = Config.ylim
    plt.ylim(yy, -yy)
plt.show()
