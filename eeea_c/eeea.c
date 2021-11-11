#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

void iterative_search_of_maxima(
    float* wave, int wave_len, int* wi, int wi_len,
    int* wio, int* wio_len
){
    wio[0] = 0;
    *wio_len = 1;
    for (int ii = 1; ii < wi_len-1; ii++){
        bool cond = wave[wi[ii-1]] < wave[wi[ii]] && wave[wi[ii]] >= wave[wi[ii+1]];
        if(cond) {
            wio[*wio_len] = wi[ii];
            *wio_len += 1;
        }
    }
    if(wio[*wio_len-1] != wave_len-1){
        wio[*wio_len] = wave_len-1;
    }
    
}

void array_insert(int* arr, int* arr_len, int index, int value){
    memcpy(arr+index+1, arr+index, ((*arr_len)-index)*sizeof(int));
    arr[index] = value;
    *arr_len += 1;
}

void local_peak_processing(
    int ts_n, int* new, int* new_len, int* old, int old_len
){
    // the size of the array [new] will expand
    int ni=0, oi=0, si=0;
    while(ni < (*new_len)-1){
        int oim = oi;
        if(new[ni+1]-new[ni] > ts_n){
            int target_index = (new[ni] + new[ni+1])/2;
            while(true){
                if(old[oim]<=target_index && target_index<old[oim+1]){
                    break;
                }
                oim += 1;
            }
            if(old[oim] == new[ni]){
                oim += 1;
            }
            array_insert(new, new_len, ni+1, old[oim]);
        } else {
            ni += 1;
            oi = oim;
        }
    }
}

void eeea(
    float* wave, int wave_len, float fs, float ts, int n_peak, int n_loop, 
    float* envelop
){
    int ts_n = ts*fs;
    
    int *selected_indexes = malloc(wave_len * sizeof(int));
    for (int i = 0; i < wave_len; i++) selected_indexes[i] = i;
    int selected_indexes_len = wave_len;

    for (int i = 0; i < n_loop; i++){
        int* old_selected_indexes = malloc(wave_len * sizeof(int));
        memcpy(old_selected_indexes, selected_indexes, 
            selected_indexes_len*sizeof(int));
        int old_selected_indexes_len = selected_indexes_len;

        iterative_search_of_maxima(
            wave, wave_len, old_selected_indexes, old_selected_indexes_len,
            selected_indexes, &selected_indexes_len
        );

        if(selected_indexes_len < n_peak) break;

        local_peak_processing(
            ts_n, selected_indexes, &selected_indexes_len, 
            old_selected_indexes, old_selected_indexes_len
        );

        free(old_selected_indexes);
    }

    envelop = malloc(sizeof(float) * wave_len);
    for (int i = 0; i < selected_indexes_len; i++){
        int wi = selected_indexes[i];
        envelop[wi] = wave[wi];
    }
    envelop[selected_indexes[0]] = envelop[selected_indexes[1]];
    int last = selected_indexes_len -1;
    envelop[selected_indexes[last]] = envelop[selected_indexes[last-1]];
    
    // linear interpolation
    for (int i = 0; i < selected_indexes_len-1; i++){
        int l = selected_indexes[i], r = selected_indexes[i+1];
        int rl = r - l;
        for (int j = l+1; j < r; j++){
            envelop[j] = wave[l]*(j-l)/rl + wave[r]*(r-j)/rl;
        }
    }
}
