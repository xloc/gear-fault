from scipy.interpolate import interp1d
from typing import List


def eeea(wave: List[float], 
        fs: float = 12800, ts: float = 0.005, n_peak: int = 5, n_loop: int = 20
    ) -> List[float]:
    """the Empirical Envelope Estimation Algorithm.

    The [wave] will be enveloped with smoothness defined by [ts]. The shorter 
    the [ts], the more fine-grained the envelope; the longer the [ts], the 
    smoother the envelope (though details might be lost). [fs] is the sampling 
    frequency. At least [n_peaks] points will be selected from the [wave] to 
    form the envelope. And the algorithm will iterate [n_loop] times before 
    ending. You can keep [n_loop] unchanged for most of the cases, the result 
    is not sensitive to it.
    """
    def iterative_search_of_maxima(wi):
        wio = [0]
        for ii in range(1, len(wi)-1):
            cond = wave[wi[ii-1]] < wave[wi[ii]] >= wave[wi[ii+1]]
            if cond:
                wio.append(wi[ii])
        if wio[-1] != len(wave)-1:
            wio.append(len(wave)-1)
        return wio

    ts_n = int(ts*fs)

    def local_peaks_processing(new, old):
        ni = 0
        oi = 0
        while ni < len(new)-1:
            oim = oi  # oi lamdmark
            if new[ni+1]-new[ni] > ts_n:
                target_index = (new[ni] + new[ni+1])//2
                while True:
                    if old[oim] <= target_index < old[oim+1]:
                        break
                    oim += 1
                if old[oim] == new[ni]:
                    oim += 1

                # notice the ni+1, it took a long time to debug
                new.insert(ni+1, old[oim])
            else:
                ni += 1
                oi = oim

    selected_indexes = range(len(wave))
    for i in range(n_loop):
        old_selected_indexes = selected_indexes
        selected_indexes = iterative_search_of_maxima(selected_indexes)
        if len(selected_indexes) < n_peak:
            break
        local_peaks_processing(selected_indexes, old_selected_indexes)

    wave_selected = [wave[i] for i in selected_indexes]
    wave_selected[0] = wave_selected[1]
    wave_selected[-1] = wave_selected[-2]
    f = interp1d(selected_indexes, wave_selected, 'cubic')
    envelope = f(range(len(wave)))

    return envelope
