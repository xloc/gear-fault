# trying =================================
%matplotlib inline 
from scipy.interpolate import interp1d

def around(prompt, arr, i, l, r):
    ll = max(i-l, 0)
    rr = min(i+r, len(arr))
    print(prompt, end=' ')
    for ii in range(ll, rr):
        if ii != i:
            print(arr[ii], end=', ')
        else:
            print(f'<{arr[ii]}>', end=', ')
    print()
    
added_point = []

def eeea(wave):
    n_peak = 5
    n_loop = 20
    fs = 12800
    ts = 0.01
    tsl = 0.25 * ts
    duration = len(wave) / fs
    
    tsl_n = int(tsl*fs)
    ts_n = int(ts*fs)
#     print(f'tsl_n = {tsl_n}; ts_n = {ts_n}')
    
    def iterative_search_of_maxima(wi):
        wio = [0]
        for ii in range(1, len(wi)-1):
            cond = wave[wi[ii-1]] < wave[wi[ii]] >= wave[wi[ii+1]]
            if cond:
                wio.append(wi[ii])
        if wio[-1] != len(wave)-1:
            wio.append(len(wave)-1)
        return wio

    i=0
    def local_peaks_processing(new, old):
        ni = 0
        oi = 0
        while ni < len(new)-1:
            oim = oi # oi lamdmark
            if new[ni+1]-new[ni] > ts_n:
                target_index = (new[ni] + new[ni+1])//2
                while True:
                    if old[oim] <= target_index < old[oim+1]:
                        break
                    oim += 1
                
                if old[oim] == new[ni]:
                    oim += 1
                    
                new.insert(ni+1, old[oim]) # notice the ni+1, it took a long time to debug
                if i == 6:
                    added_point.append(old[oim])
            else:
                ni += 1
                oi = oim
            
    selected_indexes = range(len(wave))
    while True:
        if i == n_loop:
            break
        else:
            i += 1
#     for i in range(n_loop):
        old_selected_indexes = selected_indexes
        selected_indexes = iterative_search_of_maxima(selected_indexes)
        if len(selected_indexes) < n_peak:
            break
        local_peaks_processing(selected_indexes, old_selected_indexes)
        
        if i not in [0] and i%3==0:
            plt.scatter(selected_indexes, [wave[ii] for ii in selected_indexes], s=100, label=f'{i}')
        
    plt.legend()

    
    plt.scatter(selected_indexes, [wave[i] for i in selected_indexes], s=100, color='orange')
    
    wave_selected = [wave[i] for i in selected_indexes]
    f = interp1d(selected_indexes, wave_selected, 'cubic')
    envelope = f(np.arange(len(wave)))
        
    return envelope
    
@contextlib.contextmanager
def plot(title):
    plt.figure(figsize=(20,5))
    plt.title(title)
    yield
#     plt.xlim(0, 8192)
    y_range = 35
    plt.ylim(-y_range,y_range)
    plt.grid(True)
    plt.show()

w = samples[info_to_index(1, 'L', False)]
signal = w.wave
with plot(title='EEEA enveloping'):
    plt.plot(signal, color='gray')
    envelope = eeea(signal)
    plt.plot(envelope)
    plt.stem(added_point, np.ones_like(added_point)*30)